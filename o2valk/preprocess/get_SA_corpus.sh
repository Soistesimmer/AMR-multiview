#!/usr/bin/env bash
#sed -i 's/\r$//' get_SA_corpus.sh

data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

SA_data_dir='./workspace/data/'
if [ ! -d "$data_dir" ]; then mkdir -p "$data_dir"; fi

python3 ./get_ori_corpus.py -input $data_dir/train15.json \
                         -src $data_dir/train_src_15 \
                         -tgt $data_dir/train_tgt_15

python3 ./get_ori_corpus.py -input $data_dir/dev15.json \
                         -src $data_dir/dev_src_15 \
                         -tgt $data_dir/dev_tgt_15

python3 ./get_ori_corpus.py -input $data_dir/test15.json \
                         -src $data_dir/test_src_15 \
                         -tgt $data_dir/test_tgt_15

python3 ./tokenize_before_bpe.py -input $data_dir/train_tgt_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/dev_tgt_15 \

python3 ./tokenize_before_bpe.py -input $data_dir/test_tgt_15 \

python3 ./break_down_amr.py -input $data_dir/train_src_15 \
                            -output $data_dir/bpe_src_corpus \
                            -vocab $data_dir/train_src_vocab

python3 ./break_down_amr.py -input $data_dir/dev_src_15 \
                            -vocab $data_dir/dev_src_vocab

python3 ./break_down_amr.py -input $data_dir/test_src_15 \
                            -vocab $data_dir/test_src_vocab

subword-nmt learn-bpe -s 10000 < $data_dir/train_src_15 > $data_dir/bpe_src_model
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/train_src_15> $data_dir/train_source_15
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/dev_src_15> $data_dir/dev_source_15
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/test_src_15> $data_dir/test_source_15

python3 ./break_concept.py -vocab $data_dir/train_src_vocab \
                            -vocab_bpe $data_dir/train_vocab_bpe \
                            -input $data_dir/train_src_15 \
                            -output $data_dir/train_src_15

python3 ./break_concept.py -vocab $data_dir/dev_src_vocab \
                            -vocab_bpe $data_dir/dev_vocab_bpe \
                            -input $data_dir/dev_src_15 \
                            -output $data_dir/dev_src_15

python3 ./break_concept.py -vocab $data_dir/test_src_vocab \
                            -vocab_bpe $data_dir/test_vocab_bpe \
                            -input $data_dir/test_src_15 \
                            -output $data_dir/test_src_15

subword-nmt learn-bpe -s 10000 < $data_dir/train_tgt_15 > $data_dir/bpe_tgt_model
subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/train_tgt_15 > $data_dir/train_target_15
subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/dev_tgt_15 > $data_dir/dev_target_15
subword-nmt apply-bpe -c $data_dir/bpe_tgt_model < $data_dir/test_tgt_15 > $data_dir/test_target_15