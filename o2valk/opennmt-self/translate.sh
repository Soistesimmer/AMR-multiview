#!/bin/bash
# best result BLEU 31.5 at 30k step

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model2015/_step_200000.pt'
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

CUDA_VISIBLE_DEVICES=0  python3  ./translate.py  -model       $model_file   \
                                                 -src         $train_test_data_dir/test.concept.bpe \
                                                 -structure1  $train_test_data_dir/test.path_1  \
                                                 -structure2  $train_test_data_dir/test.path_2  \
                                                 -structure3  $train_test_data_dir/test.path_3  \
                                                 -structure4  $train_test_data_dir/test.path_4  \
                                                 -structure5  $train_test_data_dir/test.path_5  \
                                                 -structure6  $train_test_data_dir/test.path_6  \
                                                 -structure7  $train_test_data_dir/test.path_7  \
                                                 -structure8  $train_test_data_dir/test.path_8  \
                                                 -output      $output_dir/test_target.tran \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0   

hypothesis=$output_dir/test_target.tran
reference=$train_test_data_dir/test.tok.sent

python3 ./back_together.py -input $hypothesis -output $hypothesis

perl ../multi-bleu.perl $reference < $hypothesis


