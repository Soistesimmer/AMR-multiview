#!/bin/bash

total_step=50000
gap=5000

tag='webnlg'

train_test_data_dir=/home/wangante/work-code-20190910/webnlg_challenge_2017/test_dir
model_file='./workspace/webnlg_model/_step_'
reference_prefix=/home/wangante/work-code-20190910/webnlg_challenge_2017/test_dir/reference
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/test_target.tran
bleu_result="./workspace/bleu_result_${tag}"

for((step=5000;step<=total_step;step+=gap))
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