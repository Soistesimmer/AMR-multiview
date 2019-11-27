#/usr/bin/python
# coding:utf-8
import sys
import json
import os
from stanfordcorenlp import StanfordCoreNLP


def read_json(input_file):
    # 读取存储于json文件中的列表
    assert os.path.isfile(input_file)
    with open(input_file, 'r') as f_obj:
        jlist = json.load(f_obj)
        return jlist

def remove_wiki(amr_lst):
    assert sum(x=='(' for x in amr_lst) == sum(x==')' for x in amr_lst), ' '.join(amr_lst)
    res = []
    if len(amr_lst) ==0:
        return []
    i = 0
    while i<len(amr_lst):
        if amr_lst[i].startswith(':wiki'):                            # :wiki + concept
            if i+2 < len(amr_lst):
                assert (amr_lst[i+2].startswith(':') and len(amr_lst[i+2])>1) or amr_lst[i+2].startswith(')'), "Index {} of {}".format(i+2, ' '.join(amr_lst))
            i += 2
        else:
            res.append(amr_lst[i])
            i += 1
    return res

if __name__ == '__main__':
    
    nlp = StanfordCoreNLP(r'/home/xfbai/tools/stanford-corenlp-full-2018-10-05',lang='en')
    in_file, o_file1, o_file2 = sys.argv[1], sys.argv[2], sys.argv[3]
    
    input_list = read_json(in_file)
    num_items = len(input_list[0])
    if num_items in [2,3]:
        amrs,text = [], []
        for item in input_list:
            simplified_amr = ' '.join(remove_wiki(item['amr'].strip().split()))
            amrs.append(simplified_amr)
            #amrs.append(item['amr'])
            sent = item['sent']
            text.append(' '.join(nlp.word_tokenize(sent)))
        with open(o_file1, 'w') as f1:
            f1.write('\n'.join(amrs))
        with open(o_file2, 'w') as f2:
            f2.write('\n'.join(text))
