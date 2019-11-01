#!/bin/bash
base_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015'
ori_dir='/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/alignments/split'

echo "Shuffling ..."
python reconstruct_amr_structure.py $base_dir/train.amr $base_dir/train.concept $base_dir/rtrain.concept 10
python reconstruct_amr_structure.py $base_dir/dev.amr $base_dir/dev.concept $base_dir/rdev.concept 10

#:<<!
rtrain_concept=$base_dir/rtrain.concept
rvalid_concept=$base_dir/rdev.concept
freq=0
if [ ! -d "$base_dir/$freq" ]; then mkdir -p "$base_dir/$freq"; fi

rtrain_concept_bpe=$base_dir/$freq/rtrain.concept.bpe

rvalid_concept_bpe=$base_dir/$freq/rdev.concept.bpe

codes_file=$base_dir/$freq/train.codes

vocab_concept=$base_dir/$freq/vocab.concept
vocab_sent=$base_dir/$freq/vocab.tok.sent

# relation不做bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $rtrain_concept > $rtrain_concept_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --vocabulary-threshold $freq < $rvalid_concept > $rvalid_concept_bpe

#!
#!
