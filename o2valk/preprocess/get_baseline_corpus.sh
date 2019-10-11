#!/usr/bin/env bash
#sed -i 's/\r$//' get_baseline_corpus.sh

data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

python3 ./get_ori_corpus.py -input $data_dir/train15.json \
                         -src $data_dir/train_src_15 \
                         -tgt $data_dir/train_tgt_15 \
                         -combine $data_dir/combine_15

python3 ./get_ori_corpus.py -input $data_dir/dev15.json \
                         -src $data_dir/dev_src_15 \
                         -tgt $data_dir/dev_tgt_15

python3 ./get_ori_corpus.py -input $data_dir/test15.json \
                         -src $data_dir/test_src_15 \
                         -tgt $data_dir/test_tgt_15

python3 ./tokenize_before_bpe.py -input $data_dir/combine_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/train_src_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/dev_src_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/test_src_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/train_tgt_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/dev_tgt_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/test_tgt_15 \

subword-nmt learn-bpe -s 10000 < $data_dir/combine_15 > $data_dir/bpe_model
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/train_src_15> $data_dir/train_source_15
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/dev_src_15> $data_dir/dev_source_15
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/test_src_15> $data_dir/test_source_15
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/train_tgt_15 > $data_dir/train_target_15
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/dev_tgt_15 > $data_dir/dev_target_15
subword-nmt apply-bpe -c $data_dir/bpe_model < $data_dir/test_tgt_15 > $data_dir/test_target_15

#subword-nmt learn-bpe -s 10000 < $data_dir/train_src_15 > $data_dir/bpe_src_model
#subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/train_src_15> $data_dir/train_source_15
#subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/dev_src_15> $data_dir/dev_source_15
#subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/test_src_15> $data_dir/test_source_15

#subword-nmt learn-bpe -s 10000 < $data_dir/train_tgt_15 > $data_dir/bpe_tgt_model
#subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/train_tgt_15 > $data_dir/train_target_15
#subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/dev_tgt_15 > $data_dir/dev_target_15
#subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/test_tgt_15 > $data_dir/test_target_15