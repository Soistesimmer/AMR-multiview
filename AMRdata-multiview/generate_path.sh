#!/bin/bash
#sed -i 's/\r$//' generate_path.sh
base_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015'
freq=0

train_amr=$base_dir/train.amr
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


echo "Start generating Label paths ..."
python generate_path_.py $train_amr $train_concept_bpe $train_concept_path
python generate_path_.py $dev_amr $dev_concept_bpe $dev_concept_path
python generate_path_.py $test_amr $test_concept_bpe $test_concept_path