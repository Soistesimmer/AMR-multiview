#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/webnlg_challenge_2017'

data_dir='./workspace/webnlg_data/'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src $train_test_data_dir/train-webnlg-all-notdelex-src-nodes.txt \
                        -train_tgt $train_test_data_dir/train-tokenized-tgt.txt \
                        -train_structure  $train_test_data_dir/train.path  \
                        -train_mask $train_test_data_dir/train.oneway.mask \
                        -valid_src $train_test_data_dir/dev-webnlg-all-notdelex-src-nodes.txt \
                        -valid_tgt $train_test_data_dir/dev-tokenized-tgt.txt \
                        -valid_structure $train_test_data_dir/dev.path   \
                        -valid_mask $train_test_data_dir/dev.oneway.mask   \
                        -save_data $data_prefix \
                        -src_vocab_size 10000  \
                        -tgt_vocab_size 10000 \
                        -structure_vocab_size 5000 \
                        -src_seq_length 10000 \
                        -tgt_seq_length 10000 \
                        -share_vocab





