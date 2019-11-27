#!/bin/bash

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model8/_step_'
output_dir='./workspace/translate-result'
reference="/home/wangante/work-code-20190910/AMRdata-master/LDC2015/test.tok.sent"
hypothesis=$output_dir/test_target.tran
bleu_result="./workspace/bleu_result_8.txt"

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi
if [ ! -d "$bleu_result" ]; then touch "$bleu_result"; fi

for((total_step=10000;total_step<=300000;total_step+=10000))
do
CUDA_VISIBLE_DEVICES=3  python3  ./translate.py  -model      $model_file$total_step.pt \
                                                 -src        $train_test_data_dir/test.concept.bpe \
                                                 -structure  $train_test_data_dir/test.path  \
                                                 -output     $output_dir/test_target.tran \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$total_step," >> $bleu_result
perl ../multi-bleu.perl $reference < $hypothesis >> $bleu_result
done


