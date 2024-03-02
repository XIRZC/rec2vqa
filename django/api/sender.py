from django.conf import settings
from api.utils import log_to_terminal

import os
import pika
import sys
import json

def sender_rec(image_path, referring_expression, socket_id):

  connection = pika.BlockingConnection()
  channel = connection.channel()
  channel.queue_declare(queue='rec_task_queue', durable=True)

  message = {'image_path': image_path, 
             'referring_expression': referring_expression,
             'socket_id': socket_id,
             }
  log_to_terminal(socket_id, {'terminal': 'Sender: publishing a REC job to Queue.'})
  channel.basic_publish(exchange='',
                        routing_key='rec_task_queue',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode = 2), # make message persistent
                        )

  print(' [x] Sent %r' % message)
  log_to_terminal(socket_id, {'terminal': 'Sender: published a REC job successfully.'})
  connection.close()


def sender_vqa(question, rec, socket_id):

  connection = pika.BlockingConnection()
  channel = connection.channel()
  channel.queue_declare(queue='vqa_task_queue', durable=True)

  message = {'question': question, 
             'rec': rec,
             'socket_id': socket_id,
             }
  log_to_terminal(socket_id, {'terminal': 'Sender: publishing a VQA job to Queue.'})
  channel.basic_publish(exchange='',
                        routing_key='vqa_task_queue',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode = 2), # make message persistent
                        )

  print(' [x] Sent %r' % message)
  log_to_terminal(socket_id, {'terminal': 'Sender: published a VQA job successfully.'})
  connection.close()


def sender_det(image_path, referring_expression, socket_id):

  connection = pika.BlockingConnection()
  channel = connection.channel()
  channel.queue_declare(queue='det_task_queue', durable=True)

  message = {'image_path': image_path, 
             'referring_expression': referring_expression,
             'socket_id': socket_id,
             }
  log_to_terminal(socket_id, {'terminal': 'Sender: publishing a detection job to Queue.'})
  channel.basic_publish(exchange='',
                        routing_key='det_task_queue',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode = 2), # make message persistent
                        )

  print(' [x] Sent %r' % message)
  log_to_terminal(socket_id, {'terminal': 'Sender: published a detection job successfully.'})
  connection.close()
