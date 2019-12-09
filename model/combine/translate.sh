#!/bin/bash

total_step=300000
gap=10000

tag=combine
target=dev

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/0'
model_file='./workspace/model27/_step_'
reference="/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/${target}.reference"
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/test_target.tran
bleu_result="./workspace/${tag}.${target}"

for((step=210000;step<=total_step;step+=gap))
do
CUDA_VISIBLE_DEVICES=3  python3  ./translate.py  -model      $model_file$step.pt \
                                                 -src        $train_test_data_dir/$target.concept.bpe \
                                                 -structure  $train_test_data_dir/$target.path  \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$step," >> $bleu_result
perl ../multi-bleu.perl $reference < $hypothesis >> $bleu_result
done
