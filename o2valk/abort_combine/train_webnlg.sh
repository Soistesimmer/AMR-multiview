#!/bin/bash

data_prefix='./workspace/webnlg_data/gq'
model_dir='./workspace/webnlg_model/'
if [ ! -d "$model_dir" ]; then mkdir -p "$model_dir"; fi

CUDA_VISIBLE_DEVICES=3  nohup python3 train.py \
                        -data $data_prefix \
                        -save_model $model_dir \
                        -world_size 1 \
                        -gpu_ranks 0 \
                        -save_checkpoint_steps 3000 \
                        -valid_steps 3000 \
                        -report_every 3000 \
                        -keep_checkpoint 50 \
                        -seed 3435 \
                        -train_steps 36000 \
                        -warmup_steps 9000 \
                        --share_decoder_embeddings \
                        -share_embeddings \
                        --position_encoding \
                        --optim adam \
                        -adam_beta1 0.9 \
                        -adam_beta2 0.98 \
                        -decay_method noam \
                        -learning_rate 0.5 \
                        -max_grad_norm 0.0 \
                        -batch_size 2048 \
                        -batch_type tokens \
                        -normalization tokens \
                        -dropout 0.3 \
                        -label_smoothing 0.1 \
                        -max_generator_batches 100 \
                        -param_init 0.0 \
                        -param_init_glorot \
                        -valid_batch_size 8 \
                        -ratio 0.15 \
                        -ratio2 0.05 > b2048r15p5p_webnlg.log 2>&1 &


