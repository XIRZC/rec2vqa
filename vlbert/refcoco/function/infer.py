import os
import pprint

import json
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

from common.utils.load import smart_load_model_state_dict
from common.trainer import to_cuda
from refcoco.modules import *
from external.pytorch_pretrained_bert import BertTokenizer

@torch.no_grad()
def infer_net(args, config, image_path, referring_expression):
    # config preparation
    print('infer just one sample...')
    pprint.pprint(args)
    pprint.pprint(config)
    device_ids = [int(d) for d in config.GPUS.split(',')]
    config.DATASET.TEST_IMAGE_SET = args.split
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

    # data preprocess: image, referring_expression => image, boxes, exp_ids
    image = Image.open(image_path).convert('RGB')
    im_info = torch.as_tensor([image.width, image.height, 1.0, 1.0])

    # expression
    exp = referring_expression
    exp = exp[:-1] if exp[-1] == '?' else exp
    exp_tokens = [token for token in exp.split(' ')]
    tokenizer = BertTokenizer.from_pretrained(config.BERT_MODEL_NAME)
    exp_retokens = tokenizer.tokenize(' '.join(exp_tokens))
    exp_ids = tokenizer.convert_tokens_to_ids(exp_retokens)

    boxes = torch.as_tensor([[0, 0, 0, 0]])
    # boxes[:, [2, 3]] += boxes[:, [0, 1]]
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
    print(pred_boxes)
