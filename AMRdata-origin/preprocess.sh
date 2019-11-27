#!/bin/bash
base_dir='/home/wangante/work-code-20190910/AMRdata-origin/LDC2015'

echo "Spliting files ..."
python preprocess.py $base_dir/train.json $base_dir/train.amr $base_dir/train.tok.sent $base_dir/train.concept
python preprocess.py $base_dir/dev.json $base_dir/dev.amr $base_dir/dev.tok.sent $base_dir/dev.concept
python preprocess.py $base_dir/test.json $base_dir/test.amr $base_dir/test.tok.sent $base_dir/test.concept

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

echo "Start learning BPE ..."
subword-nmt learn-joint-bpe-and-vocab --input $train_concept $train_sent -s $num_operations -o $codes_file --write-vocabulary $vocab_concept $vocab_sent

subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $train_amr > $train_amr_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $train_concept > $train_concept_bpe_tmp
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $train_sent > $train_sent_bpe

#:<<!
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $dev_amr > $dev_amr_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $dev_concept > $dev_concept_bpe_tmp
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $dev_sent > $dev_sent_bpe

subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $test_amr > $test_amr_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq  < $test_concept > $test_concept_bpe_tmp
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $test_sent > $test_sent_bpe

python postprocess_concept_bpe.py $train_concept_bpe_tmp $train_concept_bpe 
python postprocess_concept_bpe.py $dev_concept_bpe_tmp $dev_concept_bpe 
python postprocess_concept_bpe.py $test_concept_bpe_tmp $test_concept_bpe 

echo "Start generating Label paths ..."
python generate_path.py $train_amr $train_concept_bpe $train_concept_path
python generate_path.py $dev_amr $dev_concept_bpe $dev_concept_path
python generate_path.py $test_amr $test_concept_bpe $test_concept_path
#!
#!
