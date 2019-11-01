#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/webnlg_challenge_2017'

data_dir='./workspace/webnlg_data/'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src $train_test_data_dir/train-webnlg-all-notdelex.triple \
                        -train_tgt $train_test_data_dir/train-webnlg-all-notdelex-tgt.txt \
                        -valid_src $train_test_data_dir/dev-webnlg-all-notdelex.triple  \
                        -valid_tgt $train_test_data_dir/dev-webnlg-all-notdelex-tgt.txt \
                        -save_data $data_prefix \
                        -src_vocab_size 10000  \
                        -tgt_vocab_size 10000 \
                        -src_seq_length 10000 \
                        -tgt_seq_length 10000 \
                        -share_vocab





