import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.conf import settings

import sys
sys.path.insert(0, '../vlbert')
sys.path.insert(0, '../vlbert/refcoco')
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

from PIL import Image, ImageDraw
import torch
import torch.nn.functional as F

from function.config import config, update_config
from modules import *

from utils.load import smart_load_model_state_dict
from trainer import to_cuda

from pytorch_pretrained_bert import BertTokenizer

parser = argparse.ArgumentParser('')
args = parser.parse_args()
args.cfg = '../vlbert/cfgs/refcoco/base_detected_regions_1x32G.yaml'
args.ckpt = '../vlbert/ckpts/ref/vl-bert_base_res101_refcoco-best.model'
args.gpus = [0]
update_config(args.cfg)
config.GPUS = ','.join([str(index) for index in args.gpus])
# args and config is okay util here

print('infer just one sample...')
pprint.pprint(args)
pprint.pprint(config)
device_ids = [int(d) for d in config.GPUS.split(',')]
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

@torch.no_grad()
def model_forward(image_path, boxes, referring_expression):
    # data preprocess: image, referring_expression => image, boxes, exp_ids
    result_image = str(REC_CONFIG['image_dir'] / image_path.split('/')[-1])
    image = Image.open(image_path).convert('RGB')
    im_info = torch.as_tensor([image.width, image.height, 1.0, 1.0])

    # expression
    exp_tokens = referring_expression
    tokenizer = BertTokenizer.from_pretrained(config.NETWORK.BERT_MODEL_NAME)
    exp_retokens = tokenizer.tokenize(' '.join(exp_tokens))
    exp_ids = tokenizer.convert_tokens_to_ids(exp_retokens)

    # boxes to tensor
    boxes = torch.as_tensor(boxes)

    # clamp boxes
    w = im_info[0].item()
    h = im_info[1].item()
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clamp(min=0, max=w - 1)
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clamp(min=0, max=h - 1)
    batch = [image, boxes, im_info, exp_ids]
    batch = to_cuda(batch)

    # infer
    model.eval()
    output = model(*batch)
    pred_boxes = output['pred_boxes'].detach().cpu().tolist()

    draw = ImageDraw.Draw(image)
    draw.rectangle(pred_boxes, outline='red')
    image.save(result_image)

    output = {
        'result', pred_boxes,
        'result_image', result_image
    }
    return output

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='rec_task_queue', durable=True)
print(' [*] Waiting for REC requests. To exit press CTRL+C')
def callback(ch, method, properties, body):
    try:
        print(' [x] Received %r' % body)  # body is {'image_path', 'expression', 'socket_id'}
        body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value

        boxes = [[]]
        result = model_forward(body['image_path'], boxes, body['referring_expression'])

        img = IMG.objects.filter(img__endswith=body['image_path'].split('/')[-1])[0]

        REC.objects.create(socket_id=body['socket_id'],
                                    img=img,
                                    referring_expression=body['referring_expression'],
                                    result=result['result'],
                                    result_image=result['result_image']
                                    )

        # Close the database connection in order to make sure that MYSQL Timeout doesn't occur
        django.db.close_old_connections()

        log_to_terminal(body['socket_id'], {'result': json.dumps(result)})
        log_to_terminal(body['socket_id'], {'terminal': 'Receiver: Completed the REC job.'})

        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(' [x] Worker: Completed the REC job.')
        print(" [x] Done")

    except:
        log_to_terminal(body['socket_id'], {"terminal": json.dumps({"Traceback": str(traceback.print_exc())})})


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rec_task_queue', on_message_callback=callback)

channel.start_consuming()

