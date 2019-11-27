#/usr/bin/python
# coding:utf-8
import sys
import json
import os
import argparse
from stanfordcorenlp import StanfordCoreNLP
from amr_utils import read_json, remove_wiki, read_anonymized, get_concepts


if __name__ == '__main__':
    
    nlp = StanfordCoreNLP(r'/home/wangante/stanford-corenlp-full-2018-10-05',lang='en')
    in_file, o_file1, o_file2,o_file3 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    
    input_list = read_json(in_file)
    num_items = len(input_list[0])
    if num_items in [2,3]:
        amrs,text,concepts = [], [], []
        for item in input_list:
            simplified_amr = remove_wiki(item['amr'].strip().split())
            amrs.append(' '.join(simplified_amr))
            
            sent = item['sent']
            text.append(' '.join(nlp.word_tokenize(sent)))
            #text.append(sent)
            concepts.append(' '.join(get_concepts(simplified_amr)))
        
        with open(o_file1, 'w') as f1:
            f1.write('\n'.join(amrs))
        with open(o_file2, 'w') as f2:
            f2.write('\n'.join(text))
        with open(o_file3, 'w') as f3:
            f3.write('\n'.join(concepts))
