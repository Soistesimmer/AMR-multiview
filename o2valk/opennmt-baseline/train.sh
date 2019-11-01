#!/bin/bash

data_prefix='./workspace/data_proxy/gq'
model_dir='./workspace/model_proxy/'
if [ ! -d "$model_dir" ]; then mkdir -p "$model_dir"; fi

CUDA_VISIBLE_DEVICES=3  nohup python3 train.py \
                        -data $data_prefix \
                        -save_model $model_dir \
                        -world_size 1 \
                        -gpu_ranks 0 \
                        -save_checkpoint_steps 10000 \
                        -valid_steps 10000 \
                        -report_every 10000 \
                        -keep_checkpoint 1000 \
                        -seed 3435 \
                        -train_steps 250000 \
                        -warmup_steps 16000 \
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
                        -valid_batch_size 8 > b2048_proxy.log 2>&1 &
