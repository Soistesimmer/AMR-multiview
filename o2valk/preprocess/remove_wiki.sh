#!/usr/bin/env bash
#sed -i 's/\r$//' remove_wiki.sh

data_dir="/home/wangante/work-code-20190910/o2valk/corpus/"

python3 ./remove_wiki.py -input $data_dir/training.json -output $data_dir/train15.json
python3 ./remove_wiki.py -input $data_dir/dev.json -output $data_dir/dev15.json
python3 ./remove_wiki.py -input $data_dir/test.json -output $data_dir/test15.json
