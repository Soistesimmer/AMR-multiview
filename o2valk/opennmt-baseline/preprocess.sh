#!/bin/bash

train_test_data_dir=/home/wangante/work-code-20190910/AMRdata-master/liu/my_data/proxy
data_dir='./workspace/data_proxy'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src $train_test_data_dir/train.amr.bpe \
                       -train_tgt $train_test_data_dir/train.tok.sent.bpe \
                       -valid_src $train_test_data_dir/dev.amr.bpe  \
                       -valid_tgt $train_test_data_dir/dev.tok.sent.bpe \
                       -save_data $data_prefix \
                       -src_vocab_size 30000  \
                       -tgt_vocab_size 30000 \
                       -src_seq_length 10000 \
                       -tgt_seq_length 10000 \
                       -share_vocab
