import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from django.conf import settings

import pika
import json
import yaml
import traceback

from api.utils import log_to_terminal
from api.constants import REC_CONFIG
from api.models import REC, VQA, IMG

from mmdet.apis import init_detector, inference_detector
import mmcv

# IMG = 'demo.jpg'
CONF_THRESHOLD = 0.5
BOXES_ROUND = (10, 100)
CONFIG = '../mmdetection/configs/mask_rcnn/mask_rcnn_r101_fpn_mstrain-poly_3x_coco.py'
CHECKPOINT = '../mmdetection/checkpoints/mask_rcnn_r101_fpn_mstrain-poly_3x_coco_20210524_200244-5675c317.pth'
# CONFIG = '../configs/faster_rcnn/faster_rcnn_r101_fpn_1x_coco.py'
# CHECKPOINT = '../checkpoints/faster_rcnn_r101_fpn_1x_coco_20200130-f513f705.pth'
# build the model from a config file and a checkpoint file
model = init_detector(CONFIG, CHECKPOINT, device='cuda:0')

def img2bbox(img, conf_threshold, boxes_round):
    
    # test a single image and show the results
    result = inference_detector(model, img)[0]
    result_image = str(REC_CONFIG['image_dir'] / img.split('/')[-1])
    model.show_result(img, result, out_file=result_image)
    boxes = []
    for cat_id, cat_boxes in enumerate(result):
        for box in cat_boxes:
            box = box.tolist()
            boxes.append(box)
    boxes.sort(reverse=True, key=lambda box: box[4])
    n_boxes = []
    for i, box in enumerate(boxes[:min(boxes_round[1], len(boxes))]):
        if i < boxes_round[0] or box[4] > conf_threshold:
            n_boxes.append(box[:4])
    output = {
        'result': n_boxes[0],
        'result_image': settings.HOST + 'media' + result_image.replace(str(settings.MEDIA_ROOT), ''),
    }
    return output

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='det_task_queue', durable=True)
print(' [*] Waiting for detection requests. To exit press CTRL+C')


def callback(ch, method, properties, body):
    try:
        #print(" [x] Received detection request for image path: %r" % body.decode())
        print(' [x] Received %r' % body)  # body is {'image_path', 'expression', 'socket_id'}
        body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value
    
        # time.sleep(body.count(b'.'))
        # result = model_forward(body['image_path'])
        result = img2bbox(body['image_path'], CONF_THRESHOLD, BOXES_ROUND)
        print('boxes_result', result)

        print('handled_img', body['image_path'].split('/')[-1])
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
        log_to_terminal(body['socket_id'], {'terminal': 'Receiver: Completed the detection job.'})

        ch.basic_ack(delivery_tag = method.delivery_tag)
        print(' [x] Worker: Completed the detection job.')
        print(" [x] Done")
  
    except:
        log_to_terminal(body['socket_id'], {"terminal": json.dumps({"Traceback": str(traceback.print_exc())})})



channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='det_task_queue', on_message_callback=callback)

channel.start_consuming()
