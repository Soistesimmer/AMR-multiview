#!/bin/bash

total_step=300000
gap=10000

cate=test
tag='test'

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model_test/_step_'
reference="/home/wangante/work-code-20190910/AMRdata-master/LDC2015/${cate}.reference"
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/${cate}.${tag}
bleu_result="./workspace/${cate}.${tag}"

if [ ! -d "$bleu_result" ]; then touch "$bleu_result"; fi

for((step=280000;step<=total_step;step+=gap))
do
CUDA_VISIBLE_DEVICES=3  python3  ./translate.py  -model      $model_file$step.pt \
                                                 -src        $train_test_data_dir/${cate}.concept.bpe \
                                                 -structure  $train_test_data_dir/${cate}.path  \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$step," >> $bleu_result
perl ../multi-bleu.perl $reference < $hypothesis >> $bleu_result
done

# 24k 30.77
# 23k 30.35
# 22k 30.92
# 21k 30.83
# 20k 30.57
# 19k 30.31
# 18k 30.37
# 17k 30.43
