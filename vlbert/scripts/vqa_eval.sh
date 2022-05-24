python vqa/test.py \
  --cfg cfgs/vqa/base_1x32G_fp32_infer.yaml \
  --ckpt ckpts/vqa/sec/vl-bert_base_res101_vqa-0001.model \
  --gpus 0\
  --result-path output/vqa --result-name base_1X32_fp32_epoch3
