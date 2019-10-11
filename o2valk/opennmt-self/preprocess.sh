#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'

data_dir='./workspace/data/'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi
data_prefix="$data_dir/gq"

python3 ./preprocess.py -train_src              $train_test_data_dir/train.concept.bpe \
                       -train_tgt               $train_test_data_dir/train.tok.sent.bpe \
                       -train_structure1        $train_test_data_dir/train.path_1  \
                       -train_structure2        $train_test_data_dir/train.path_2  \
                       -train_structure3        $train_test_data_dir/train.path_3  \
                       -train_structure4        $train_test_data_dir/train.path_4  \
                       -train_structure5        $train_test_data_dir/train.path_5  \
                       -train_structure6        $train_test_data_dir/train.path_6  \
                       -train_structure7        $train_test_data_dir/train.path_7  \
                       -train_structure8        $train_test_data_dir/train.path_8  \
                       -valid_src               $train_test_data_dir/dev.concept.bpe  \
                       -valid_tgt               $train_test_data_dir/dev.tok.sent.bpe \
                       -valid_structure1        $train_test_data_dir/dev.path_1   \
                       -valid_structure2        $train_test_data_dir/dev.path_2   \
                       -valid_structure3        $train_test_data_dir/dev.path_3   \
                       -valid_structure4        $train_test_data_dir/dev.path_4   \
                       -valid_structure5        $train_test_data_dir/dev.path_5   \
                       -valid_structure6        $train_test_data_dir/dev.path_6   \
                       -valid_structure7        $train_test_data_dir/dev.path_7   \
                       -valid_structure8        $train_test_data_dir/dev.path_8   \
                       -save_data $data_prefix \
                       -src_vocab_size 20000  \
                       -tgt_vocab_size 20000 \
                       -structure_vocab_size 20000 \
                       -src_seq_length 10000 \
                       -tgt_seq_length 10000 \
                       -share_vocab





