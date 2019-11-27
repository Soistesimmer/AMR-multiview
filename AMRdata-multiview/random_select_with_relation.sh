#!/bin/bash
base_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015'
ori_dir='/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/alignments/split'

echo "Shuffling ..."
python reconstruct_amr_structure.py $base_dir/train.amr $base_dir/rtrain.amr 1
python reconstruct_amr_structure.py $base_dir/dev.amr $base_dir/rdev.amr 1

#:<<!
rtrain_amr=$base_dir/rtrain.amr
rvalid_amr=$base_dir/rdev.amr
freq=0
if [ ! -d "$base_dir/$freq" ]; then mkdir -p "$base_dir/$freq"; fi

rtrain_amr_bpe=$base_dir/$freq/rtrain.amr.bpe

rvalid_amr_bpe=$base_dir/$freq/rdev.amr.bpe

codes_file=$base_dir/$freq/train.codes

vocab_concept=$base_dir/$freq/vocab.concept

# relation不做bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --glossaries "^:[A-Za-z\-0-9]+" --vocabulary-threshold $freq < $rtrain_amr > $rtrain_amr_bpe
subword-nmt apply-bpe -c $codes_file --vocabulary $vocab_concept --glossaries "^:[A-Za-z\-0-9]+" --vocabulary-threshold $freq < $rvalid_amr > $rvalid_amr_bpe

#!
#!
