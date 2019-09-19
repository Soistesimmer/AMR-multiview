#!/usr/bin/env bash
#sed -i 's/\r$//' get_bpe_corpus.sh

data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

python3 ./get_bpe_corpus.py -train $data_dir/training.json \
                         -target $data_dir/target.en

python3 ./tokenize_before_bpe.py -target $data_dir/target.en

python3 ./break_down_amr.py -input $data_dir/training.json \
                            -output $data_dir/concept.en \
                            -vocab $data_dir/vocab.en

subword-nmt learn-bpe -s 6000 < $data_dir/concept.en > $data_dir/bpe_model_concept.en
subword-nmt apply-bpe -c $data_dir/bpe_model_concept.en < $data_dir/vocab.en > $data_dir/vocab_bpe.en

subword-nmt learn-bpe -s 10000 < $data_dir/target.en > $data_dir/bpe_model.en
subword-nmt apply-bpe -c $data_dir/bpe_model.en < $data_dir/target.en > $data_dir/target_bpe.en