#!/bin/bash

total_step=36000
gap=3000

cate=test
tag='webnlg'

train_test_data_dir=/home/wangante/work-code-20190910/webnlg_challenge_2017/${cate}_dir
model_file='./workspace/webnlg_model/_step_'
reference_prefix=/home/wangante/work-code-20190910/webnlg_challenge_2017/${cate}_dir/reference
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/tran.${cate}.${tag}
bleu_result="./workspace/${cate}.${tag}"

for((step=3000;step<=total_step;step+=gap))
do
CUDA_VISIBLE_DEVICES=0  python3  ./translate.py  -model      $model_file$step.pt \
                                                 -src        $train_test_data_dir/reference.kb \
                                                 -structure  $train_test_data_dir/reference.path  \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$step," >> $bleu_result
perl ../multi-bleu.perl ${reference_prefix} < $hypothesis >> $bleu_result
done