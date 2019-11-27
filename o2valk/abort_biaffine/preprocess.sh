#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'

data_dir='./workspace/data_wr/'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src $train_test_data_dir/train.concept.bpe \
                        -train_tgt $train_test_data_dir/train.tok.sent.bpe \
                        -train_structure  $train_test_data_dir/train.path  \
                        -train_mask $train_test_data_dir/train.align \
                        -valid_src $train_test_data_dir/dev.concept.bpe  \
                        -valid_tgt $train_test_data_dir/dev.tok.sent.bpe \
                        -valid_structure $train_test_data_dir/dev.path   \
                        -valid_mask $train_test_data_dir/dev.align   \
                        -save_data $data_prefix \
                        -src_vocab_size 10000  \
                        -tgt_vocab_size 10000 \
                        -structure_vocab_size 5000 \
                        -src_seq_length 10000 \
                        -tgt_seq_length 10000 \
                        -share_vocab





