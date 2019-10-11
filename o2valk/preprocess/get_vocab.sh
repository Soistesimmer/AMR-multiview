#!/usr/bin/env bash
#sed -i 's/\r$//' get_vocab.sh

data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

python3 ./break_down_amr.py -input $data_dir/train_src_15 \
                            -output $data_dir/bpe_src_corpus \
                            -vocab $data_dir/train_src_vocab

python3 ./break_down_amr.py -input $data_dir/dev_src_15 \
                            -vocab $data_dir/dev_src_vocab

python3 ./break_down_amr.py -input $data_dir/test_src_15 \
                            -vocab $data_dir/test_src_vocab

subword-nmt learn-bpe -s 10000 < $data_dir/bpe_src_corpus > $data_dir/bpe_src_model
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/train_src_vocab> $data_dir/train_vocab_bpe
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/dev_src_vocab> $data_dir/dev_vocab_bpe
subword-nmt apply-bpe -c $data_dir/bpe_src_model < $data_dir/test_src_vocab> $data_dir/test_vocab_bpe