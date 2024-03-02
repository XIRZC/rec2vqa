from __future__ import print_function
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.conf import settings
import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.insert(0, '../vlbert')
sys.path.insert(0, '../vlbert/vqa')
sys.path.insert(0, '../vlbert/common')
sys.path.insert(0, '../vlbert/external')

from fcos import FCOS
import cv2
import skimage.io as io

import pika
import json
import pprint
import yaml
import traceback
import argparse
import re
import time

from api.utils import log_to_terminal
from api.constants import REC_CONFIG
from api.models import REC, VQA, IMG

from PIL import Image, ImageDraw
import torch
import torch.nn.functional as F

from function.config import config, update_config
from data.transforms import transforms as T
from modules import *

from utils.load import smart_load_model_state_dict
from trainer import to_cuda

from pytorch_pretrained_bert import BertTokenizer

parser = argparse.ArgumentParser('')
args = parser.parse_args()
args.cfg = '../vlbert/cfgs/vqa/base_1x32G_fp32.yaml'
args.ckpt = '../vlbert/ckpts/vqa/vl-bert_base_res101_vqa-best.model'
args.gpus = [0]
update_config(args.cfg)
config.GPUS = ','.join([str(index) for index in args.gpus])
# args and config is okay util here

print('infer just one sample...')
pprint.pprint(args)
pprint.pprint(config)
device_ids = [int(d) for d in config.GPUS.split(',')]
answer_vocab_file = config.DATASET.ANSWER_VOCAB_FILE
ckpt_path = args.ckpt
torch.backends.cudnn.enabled = False
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# get network
model = eval(config.MODULE)(config)
if len(device_ids) > 1:
    model = torch.nn.DataParallel(model, device_ids=device_ids).cuda()
else:
    torch.cuda.set_device(device_ids[0])
    model = model.cuda()
checkpoint = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
smart_load_model_state_dict(model, checkpoint['state_dict'])

# get transform
transform = T.Compose(
    [
        T.Resize(config.SCALES[0], config.SCALES[1]),
        T.ToTensor(),
        T.Normalize(
            mean=config.NETWORK.PIXEL_MEANS, std=config.NETWORK.PIXEL_STDS, to_bgr255=True
        )
    ]
)

# get answer vocabulary
with open(answer_vocab_file, 'r', encoding='utf8') as f:
    def processPunctuation(inText):
        periodStrip = re.compile("(?!<=\d)(\.)(?!\d)")
        commaStrip = re.compile("(\d)(\,)(\d)")
        punct = [';', r"/", '[', ']', '"', '{', '}',
                      '(', ')', '=', '+', '\\', '_', '-',
                      '>', '<', '@', '`', ',', '?', '!']
        if inText == '<unk>':
            return inText

        outText = inText
        for p in punct:
            if (p + ' ' in inText or ' ' + p in inText) or (re.search(commaStrip, inText) != None):
                outText = outText.replace(p, '')
            else:
                outText = outText.replace(p, ' ')
        outText = periodStrip.sub("", outText, re.UNICODE)
        return outText
    answer_vocab = [w.lower().strip().strip('\r').strip('\n').strip('\r') for w in f.readlines()]
    answer_vocab = list(filter(lambda x: x != '', answer_vocab))
    answer_vocab = [processPunctuation(w) for w in answer_vocab]

def pretty_print(bbox_results):
    max_label_name_len = max([len(_["label_name"]) for _ in bbox_results])
    for item in bbox_results:
        print("{}    confidence: {:.2f}    ".format(
            item["label_name"].ljust(max_label_name_len),
            item["score"],
        ), end="")
        print("bbox: {:.1f} {:.1f} {:.1f} {:.1f}".format(
            item["box"][0],
            item["box"][1],
            item["box"][2],
            item["box"][3],
        ))
fcos = FCOS(
    model_name="fcos_syncbn_bs32_c128_MNV2_FPN_1x",
    nms_thresh=0.6,
    cpu_only=not torch.cuda.is_available()  # if you do not have GPUs, please set cpu_only as True
)
CONF_THRESHOLD = 0.5
BOXES_ROUND = (10, 100)
def img2bbox(image_path, conf_threshold, boxes_round):
    # test a single image and show the results
    im = io.imread(image_path)
    print('img origin shape', im.shape)
    assert im.shape[-1] == 3, "only 3-channel images are supported"

    # convert from RGB to BGR because fcos assumes the BRG input image
    im = im[..., ::-1].copy()

    print('img BGR shape', im.shape)
    # resize image to have its shorter size == 800
    #f = 800.0 / float(min(im.shape[:2]))
    #print('min(im.shape[:2])', f)
    #im = cv2.resize(im, (0, 0), fx=f, fy=f)
    #print('resize image shape', im.shape)

    bbox_results = fcos.detect(im)

    pretty_print(bbox_results)

    boxes = []
    for box in bbox_results:
        bbox = box['box']
        bbox.append(box['score'])
        boxes.append(bbox)
    boxes.sort(reverse=True, key=lambda box: box[4])
    n_boxes = []
    for i, box in enumerate(boxes[:min(boxes_round[1], len(boxes))]):
        if i < boxes_round[0] or box[4] > conf_threshold:
            n_boxes.append(box[:4])
    return n_boxes

@torch.no_grad()
def model_forward(image_path, question):
    # data preprocess: image, question => image, boxes, q_ids
    # get boxes
    all_time = 0.
    tic = time.time()
    boxes = img2bbox(image_path, CONF_THRESHOLD, BOXES_ROUND)
    boxes = torch.as_tensor(boxes).float()
    get_boxes_time = time.time() - tic

    tic = time.time()
    result_image = str(REC_CONFIG['image_dir'] / image_path.split('/')[-1])
    image = Image.open(image_path).convert('RGB')
    ori_image = image.copy()
    w, h = image.width, image.height
    im_info = [w, h, 1.0, 1.0]

    # add image as a box: default true
    image_box = torch.as_tensor([[0.0, 0.0, w - 1, h - 1]])
    boxes = torch.cat((image_box, boxes), dim=0)
    load_img_time = time.time() - tic
    print('boxes', boxes.tolist())

    # question
    tic = time.time()
    q_tokens = question
    tokenizer = BertTokenizer.from_pretrained(config.NETWORK.BERT_MODEL_NAME)
    print('q_tokens', q_tokens)
    q_retokens = tokenizer.tokenize(q_tokens)
    print('q_retokens', q_retokens)
    q_ids = tokenizer.convert_tokens_to_ids(q_retokens)
    q_ids = torch.as_tensor(q_ids).unsqueeze(0)
    print('q_ids', q_ids)
    load_exp_time = time.time() - tic

    # transform
    tic = time.time()
    flipped = False
    image, boxes, _, im_info, flipped = transform(image, boxes, None, im_info, flipped)
    # clamp boxes
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clamp(min=0, max=w - 1)
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clamp(min=0, max=h - 1)
    image = image.unsqueeze(0)
    boxes = boxes.unsqueeze(0)
    im_info = torch.as_tensor(im_info).unsqueeze(0)
    print(image.shape, boxes.shape, im_info.shape, q_ids.shape)
    batch = [image, boxes, im_info, q_ids]
    batch = to_cuda(batch)
    to_batch_time = time.time() - tic

    # infer
    tic = time.time()
    model.eval()
    output = model(*batch)
    logit = output['label_logits'].argmax(dim=1).detach().cpu().tolist()[0]
    answer = answer_vocab[logit]
    print('logit', logit)
    print('answer', answer)
    vlbert_time = time.time() - tic

    all_time += get_boxes_time + load_img_time + load_exp_time + to_batch_time + vlbert_time

    print('get boxes took %.2fs, load image took %.2fs, load exp took %.2fs, to batch took %.2fs, vlbert took %.2fs, all took %.2fs' % (get_boxes_time, load_img_time, load_exp_time, to_batch_time, vlbert_time, all_time))

    output = {
        'answer': answer,
    }
    return output

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='vqa_task_queue', durable=True)
print(' [*] Waiting for VQA requests. To exit press CTRL+C')
def callback(ch, method, properties, body):
    try:
        print(' [x] Received %r' % body)  # body is {'question', 'rec', 'socket_id'}
        body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value

        rec_id = body['rec'].split('_')[0]
        rec = REC.objects.get(pk=rec_id)
        image_path = str(settings.MEDIA_ROOT / rec.img.img.name)

        referring_expression = rec.referring_expression
        replace_list = ['it', 'he', 'she']
        question = body['question']
        for item in replace_list:
            question = question.replace(item, referring_expression)
        result = model_forward(image_path, question)

        VQA.objects.create(socket_id=body['socket_id'],
                                    question=body['question'],
                                    answer=result['answer'],
                                    rec=rec
                                    )

        # Close the database connection in order to make sure that MYSQL Timeout doesn't occur
        django.db.close_old_connections()

        log_to_terminal(body['socket_id'], {'result': json.dumps(result)})
        log_to_terminal(body['socket_id'], {'terminal': 'Receiver: Completed the VQA job.'})

        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(' [x] Worker: Completed the VQA job.')
        print(" [x] Done")

    except:
        log_to_terminal(body['socket_id'], {"terminal": json.dumps({"Traceback": str(traceback.print_exc())})})


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='vqa_task_queue', on_message_callback=callback)

channel.start_consuming()
