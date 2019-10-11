#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model85/_step_300000.pt'
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi



CUDA_VISIBLE_DEVICES=2  python3  ./translate.py  -model      $model_file \
                                                 -src        $train_test_data_dir/test.concept.bpe \
                                                 -structure  $train_test_data_dir/test.path  \
                                                 -output     $output_dir/test_target.tran \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0
hypothesis=$output_dir/test_target.tran
reference="/home/wangante/work-code-20190910/AMRdata-master/LDC2015/test.tok.sent"

python3 ../back_together.py -input $hypothesis -output $hypothesis

perl ../multi-bleu.perl $reference < $hypothesis



