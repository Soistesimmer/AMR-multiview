#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model_wb/_step_300000.pt'
output_dir='./workspace/translate-result'
reference="/home/wangante/work-code-20190910/AMRdata-master/LDC2015/test.reference"
hypothesis=$output_dir/1115.tran

python3 ../back_together2.py -input $hypothesis -output $hypothesis
perl ../multi-bleu.perl $reference < $hypothesis
exit

CUDA_VISIBLE_DEVICES=1  python3  ./translate.py  -model      $model_file \
                                                 -src        $train_test_data_dir/test.concept.bpe \
                                                 -structure  $train_test_data_dir/test.path  \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together2.py -input $hypothesis -output $hypothesis
perl ../multi-bleu.perl $reference < $hypothesis

