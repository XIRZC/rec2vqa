import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.conf import settings

import sys
sys.path.insert(0, '../vlbert')
sys.path.insert(0, '../vlbert/vqa')
sys.path.insert(0, '../vlbert/common')
sys.path.insert(0, '../vlbert/external')

import pika
import json
import pprint
import yaml
import traceback
import argparse

from api.utils import log_to_terminal
from api.constants import REC_CONFIG
from api.models import REC, VQA, IMG

import PIL
import torch
import torch.nn.functional as F

from function.config import config, update_config
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

with open(answer_vocab_file, 'r', encoding='utf8') as f:
    answer_vocab = [w.lower().strip().strip('\r').strip('\n').strip('\r') for w in f.readlines()]
    answer_vocab = list(filter(lambda x: x != '', answer_vocab))
    answer_vocab = [processPunctuation(w) for w in answer_vocab]
def processPunctuation(self, inText):
    if inText == '<unk>':
        return inText

    outText = inText
    for p in self.punct:
        if (p + ' ' in inText or ' ' + p in inText) or (re.search(self.commaStrip, inText) != None):
            outText = outText.replace(p, '')
        else:
            outText = outText.replace(p, ' ')
    outText = self.periodStrip.sub("", outText, re.UNICODE)
    return outText

# get network
model = eval(config.MODULE)(config)
if len(device_ids) > 1:
    model = torch.nn.DataParallel(model, device_ids=device_ids).cuda()
else:
    torch.cuda.set_device(device_ids[0])
    model = model.cuda()
checkpoint = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
smart_load_model_state_dict(model, checkpoint['state_dict'])

@torch.no_grad()
def model_forward(image_path, boxes, question):
    # data preprocess: image, question => image, boxes, q_ids
    image = Image.open(image_path).convert('RGB')
    im_info = torch.as_tensor([image.width, image.height, 1.0, 1.0])

    # question
    tokenizer = BertTokenizer.from_pretrained(config.NETWORK.BERT_MODEL_NAME)
    q_tokens = tokenizer.tokenize(question)
    q_ids = tokenizer.convert_tokens_to_ids(q_tokens)

    # boxes to tensor
    boxes = torch.as_tensor(boxes)
    # add image as a box: default true
    image_box = torch.as_tensor([[0.0, 0.0, image.width - 1, image.height - 1]])
    boxes = torch.cat((image_box, boxes), dim=0)

    # clamp boxes
    w = im_info[0].item()
    h = im_info[1].item()
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clamp(min=0, max=w - 1)
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clamp(min=0, max=h - 1)

    batch = [image, boxes, im_info, q_ids]
    batch = to_cuda(batch)

    # infer
    model.eval()
    output = model(*batch)
    logit = output['label_logits'].argmax(dim=1).detach().cpu().tolist()[0]
    answer = answer_vocab[logit]

    output = {
        'answer', answer,
    }
    return output

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='vqa_task_queue', durable=True)
print(' [*] Waiting for VQA requests. To exit press CTRL+C')
def callback(ch, method, properties, body):
    try:
        print(' [x] Received %r' % body)  # body is {'image_path', 'expression', 'socket_id'}
        body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value

        rec = REC.objects.get(pk=body['rec'])
        image_path = str(settings.MEDIA_ROOT / rec.img)

        boxes = [[]]
        result = model_forward(image_path, boxes, body['question'])


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

