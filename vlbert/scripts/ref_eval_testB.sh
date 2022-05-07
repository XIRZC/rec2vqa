python ../refcoco/test.py \
	--split testB \
	--cfg ../cfgs/refcoco/base_detected_regions_1x32G.yaml \
	--ckpt ../ckpts/ref/vl-bert_base_res101_refcoco-best.model \
	--gpus 0 \
	--result-path ../output/ref --result-name base_detected_regions_1x32G_epoch6  > ../eval_logs/ref_eval_testB.log
