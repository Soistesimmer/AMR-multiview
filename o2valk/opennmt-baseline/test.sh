#!/usr/bin/env bash
#sed -i 's/\r$//' test.sh

hypothesis="/home/wangante/work-code-20190910/o2valk/opennmt-baseline/workspace/translate-result/test_target.tran"
reference="/home/wangante/work-code-20190910/o2valk/corpus/test_target_15"

perl ../multi-bleu.perl $reference < $hypothesis

