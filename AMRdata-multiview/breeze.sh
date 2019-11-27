#!/bin/bash
base_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015'
ori_dir='/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/alignments/split'

#:<<!
train_amr=$base_dir/train.amr
train_concept=$base_dir/train.concept
train_sent=$base_dir/train.tok.sent
num_operations=10000
freq=0
if [ ! -d "$base_dir/$freq" ]; then mkdir -p "$base_dir/$freq"; fi

train_amr_bpe=$base_dir/$freq/train.amr.bpe
train_concept_bpe=$base_dir/$freq/train.concept.bpe
train_concept_bpe_tmp=$base_dir/$freq/train.concept.bpe.tmp
train_concept_path=$base_dir/$freq/train.path
train_sent_bpe=$base_dir/$freq/train.tok.sent.bpe

dev_amr=$base_dir/dev.amr
dev_concept=$base_dir/dev.concept
dev_sent=$base_dir/dev.tok.sent
dev_amr_bpe=$base_dir/$freq/dev.amr.bpe
dev_concept_bpe=$base_dir/$freq/dev.concept.bpe
dev_concept_bpe_tmp=$base_dir/$freq/dev.concept.bpe.tmp
dev_concept_path=$base_dir/$freq/dev.path
dev_sent_bpe=$base_dir/$freq/dev.tok.sent.bpe

test_amr=$base_dir/test.amr
test_concept=$base_dir/test.concept
test_sent=$base_dir/test.tok.sent
test_amr_bpe=$base_dir/$freq/test.amr.bpe
test_concept_bpe=$base_dir/$freq/test.concept.bpe
test_concept_bpe_tmp=$base_dir/$freq/test.concept.bpe.tmp
test_concept_path=$base_dir/$freq/test.path
test_sent_bpe=$base_dir/$freq/test.tok.sent.bpe

codes_file=$base_dir/$freq/train.codes

vocab_concept=$base_dir/$freq/vocab.concept
vocab_sent=$base_dir/$freq/vocab.tok.sent

python a2b.py $base_dir/train.tok.sent $base_dir/$freq/train.tok.sent.bpe $base_dir/train.align $base_dir/$freq/train.align False
python a2b.py $base_dir/dev.tok.sent $base_dir/$freq/dev.tok.sent.bpe $base_dir/dev.align $base_dir/$freq/dev.align False
python a2b.py $base_dir/test.tok.sent $base_dir/$freq/test.tok.sent.bpe $base_dir/test.align $base_dir/$freq/test.align False

python a2b.py $base_dir/train.tok.sent $base_dir/$freq/train.tok.sent.bpe $base_dir/train.align $base_dir/$freq/train.align_wr True
python a2b.py $base_dir/dev.tok.sent $base_dir/$freq/dev.tok.sent.bpe $base_dir/dev.align $base_dir/$freq/dev.align_wr True
python a2b.py $base_dir/test.tok.sent $base_dir/$freq/test.tok.sent.bpe $base_dir/test.align $base_dir/$freq/test.align_wr True

#!
#!
