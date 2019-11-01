#!/bin/bash

total_step=270000
gap=10000

tag='o1'

train_test_data_dir='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/0'
model_file='./workspace/model/_step_'
reference="/home/wangante/work-code-20190910/AMRdata-master/LDC2015/test.tok.sent"
output_dir='./workspace/translate-result'

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/test_target.tran_${tag}
bleu_result="./workspace/bleu_result_${tag}"

for((step=10000;step<=total_step;step+=gap))
do
CUDA_VISIBLE_DEVICES=3  python3  ./translate.py  -model      $model_file$step.pt \
                                                 -src        $train_test_data_dir/test.concept.bpe \
                                                 -structure  $train_test_data_dir/test.path  \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$step," >> $bleu_result
perl ../multi-bleu.perl $reference < $hypothesis >> $bleu_result
done

# 27k 29.11
# 26k 28.62
# 25k 28.76
# 24k 28.60
# 23k 28.71
# 22k 28.41
# 21k 28.55
# 20k 28.64