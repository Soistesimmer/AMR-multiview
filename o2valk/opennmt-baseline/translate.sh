#!/bin/bash
# best result BLEU 26.04 at 25k step

model_file='/home/wangante/work-code-20190910/o2valk/opennmt-baseline/workspace/model_vt/_step_230000.pt'
source="/home/wangante/work-code-20190910/o2valk/corpus/test_source_15"
hypothesis="/home/wangante/work-code-20190910/o2valk/opennmt-baseline/workspace/translate-result/test_target.tran"
reference="/home/wangante/work-code-20190910/o2valk/corpus/test_tgt_15"
#result_dir=./workspace/translate-result
#if [ ! -d "$result_dir" ]; then mkdir -p "$result_dir"; fi

CUDA_VISIBLE_DEVICES=0  python3 ./translate.py \
                        -model $model_file  -src $source \
                        -output $hypothesis \
                        -beam_size 5 \
                        -share_vocab \
                        -gpu 0

python3 ./back_together.py -input $hypothesis -output $hypothesis

perl ../multi-bleu.perl $reference < $hypothesis