python ../vqa/test.py \
  --cfg ../cfgs/vqa/base_1x32G_fp32.yaml \
  --ckpt ../ckpts/vqa/vl-bert_base_res101_vqa-best.model \
  --gpus 0\
  --result-path ../output/vqa --result-name base_1X16_fp32_epoch5
