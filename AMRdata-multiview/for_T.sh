#!/bin/bash
#python for_F.py $ori_dir/training $base_dir/train.json $base_dir/train.align $base_dir/train.sent &
base_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015'
ori_dir='/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/alignments/split'

#echo "Spliting files ..."
#python preprocess.py $base_dir/amr_ldc2015_training_withid.json $ori_dir/training $base_dir/train.amr $base_dir/train.tok.sent $base_dir/train.concept $base_dir/train.align
#python preprocess.py $base_dir/dev.json $ori_dir/dev $base_dir/dev.amr $base_dir/dev.tok.sent $base_dir/dev.concept $base_dir/dev.align
#python preprocess.py $base_dir/test.json $ori_dir/test $base_dir/test.amr $base_dir/test.tok.sent $base_dir/test.concept $base_dir/test.align
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

#echo "Start learning BPE ..."
#subword-nmt learn-joint-bpe-and-vocab --input $train_concept $train_sent -s $num_operations -o $codes_file --write-vocabulary $vocab_concept $vocab_sent
#
## relation不做bpe
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $train_amr > $train_amr_bpe
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $train_concept > $train_concept_bpe_tmp
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $train_sent > $train_sent_bpe
#
##:<<!
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $dev_amr > $dev_amr_bpe
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $dev_concept > $dev_concept_bpe_tmp
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $dev_sent > $dev_sent_bpe
#
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq --glossaries "^:[A-Za-z\-0-9]+"  < $test_amr > $test_amr_bpe
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq  < $test_concept > $test_concept_bpe_tmp
#subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_sent --vocabulary-threshold $freq < $test_sent > $test_sent_bpe

#python a2b.py $base_dir/train.tok.sent $base_dir/$freq/train.tok.sent.bpe $base_dir/train.align $base_dir/$freq/train.align
#python a2b.py $base_dir/dev.tok.sent $base_dir/$freq/dev.tok.sent.bpe $base_dir/dev.align $base_dir/$freq/dev.align
#python a2b.py $base_dir/test.tok.sent $base_dir/$freq/test.tok.sent.bpe $base_dir/test.align $base_dir/$freq/test.align
echo "Start generating Label paths ..."
python generate_path.py $train_amr $train_concept_bpe $train_concept_path
python generate_path.py $dev_amr $dev_concept_bpe $dev_concept_path
python generate_path.py $test_amr $test_concept_bpe $test_concept_path