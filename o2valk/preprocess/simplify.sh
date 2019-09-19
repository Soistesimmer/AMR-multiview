#!/bin/bash
#sed -i 's/\r$//' simplify.sh

data_dir="/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/amrs/split/"

preprocessed_data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

python3 ./AMR_multiline_to_singleline.py -data $data_dir/training -src $preprocessed_data_dir/train_src.amr -tgt $preprocessed_data_dir/train_tgt.tgt
python3 ./AMR_multiline_to_singleline.py -data $data_dir/training15 -src $preprocessed_data_dir/train_src_15.amr -tgt $preprocessed_data_dir/train_tgt_15.tgt
python3 ./AMR_multiline_to_singleline.py -data $data_dir/dev -src $preprocessed_data_dir/dev_src.amr -tgt $preprocessed_data_dir/dev_tgt.tgt
python3 ./AMR_multiline_to_singleline.py -data $data_dir/test -src $preprocessed_data_dir/test_src.amr -tgt $preprocessed_data_dir/test_tgt.tgt




