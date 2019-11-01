#!/bin/bash

total_step=250000
gap=20000

tag='dfb'

train_test_data_dir=/home/wangante/work-code-20190910/AMRdata-master/liu/my_data/${tag}
model_file="./workspace/model_${tag}/_step_"
reference=/home/wangante/work-code-20190910/AMRdata-master/liu/my_data/${tag}-test.tok.sent
output_dir="./workspace/translate-result"

if [ ! -d "$output_dir" ]; then mkdir -p "$output_dir"; fi

hypothesis=$output_dir/test_target.tran.${tag}
bleu_result="./workspace/bleu_result_${tag}"

for((step=100000;step<=total_step;step+=gap))
do
CUDA_VISIBLE_DEVICES=1  python3  ./translate.py  -model      $model_file$step.pt \
                                                 -src        $train_test_data_dir/test.amr.bpe \
                                                 -output     $hypothesis \
                                                 -beam_size 5 \
                                                 -share_vocab  \
                                                 -gpu 0

python3 ../back_together.py -input $hypothesis -output $hypothesis
echo "$step," >> $bleu_result
perl ../multi-bleu.perl $reference < $hypothesis >> $bleu_result
done