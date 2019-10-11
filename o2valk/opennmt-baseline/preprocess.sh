#!/bin/bash

train_test_data_dir='../corpus'
data_dir='./workspace/data_vt'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src $train_test_data_dir/train_source_15 \
                       -train_tgt $train_test_data_dir/train_target_15 \
                       -valid_src $train_test_data_dir/dev_source_15  \
                       -valid_tgt $train_test_data_dir/dev_target_15 \
                       -save_data $data_prefix \
                       -src_vocab_size 30000  \
                       -tgt_vocab_size 30000 \
                       -src_seq_length 10000 \
                       -tgt_seq_length 10000 \
                       -share_vocab
