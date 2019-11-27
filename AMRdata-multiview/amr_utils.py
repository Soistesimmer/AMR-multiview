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

def get_concepts(amr_lst):
    '''
        get concepts from a amr_lst
    '''
    assert sum(x=='(' for x in amr_lst) == sum(x==')' for x in amr_lst), ' '.join(amr_lst)
    res = [item for item in amr_lst if not item.startswith(':') and item not in ['(',')'] or item == ':']
    return res

# 递归 统计node（id==list_index） 与 edge（首、尾）
def read_anonymized(amr_lst, amr_node, amr_edge):
    assert sum(x=='(' for x in amr_lst) == sum(x==')' for x in amr_lst), ' '.join(amr_lst)
    cur_str = amr_lst[0]
    cur_id = len(amr_node)
    amr_node.append(cur_str)

    i = 1
    while i < len(amr_lst):
        if amr_lst[i].startswith(':') == False: ## cur cur-num_0
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print('A relation with Dulplicated Values!!!!!!!!!!!!!!!!!!!!!!!'+' '.join(amr_lst))
            exit()
        elif amr_lst[i].startswith(':') and len(amr_lst) == 2: ## cur :edge
            nxt_str = 'num_unk'
            nxt_id = len(amr_node)
            amr_node.append(nxt_str)
            amr_edge.append((cur_id, nxt_id, amr_lst[i]))
            i = i + 1
        elif amr_lst[i].startswith(':') and amr_lst[i+1] != '(': ## cur :edge nxt
            nxt_str = amr_lst[i+1]
            nxt_id = len(amr_node)
            amr_node.append(nxt_str)
            amr_edge.append((cur_id, nxt_id, amr_lst[i]))
            i = i + 2
        elif amr_lst[i].startswith(':') and amr_lst[i+1] == '(': ## cur :edge ( ... )
            number = 1
            j = i+2
            while j < len(amr_lst):
                number += (amr_lst[j] == '(')
                number -= (amr_lst[j] == ')')
                if number == 0:
                    break
                j += 1
            assert number == 0 and amr_lst[j] == ')', ' '.join(amr_lst[i+2:j])
            nxt_id = read_anonymized(amr_lst[i+2:j], amr_node, amr_edge)
            amr_edge.append((cur_id, nxt_id, amr_lst[i]))
            i = j + 1
        else:
            assert False, ' '.join(amr_lst)
    return cur_id

def replace_bpe(amr_lst, concept_lst):
    res = []
    bpe_lst = concept_lst
    for item in amr_lst:
        if (item.startswith(':') and len(item)>1) or item in ['(',')']:
            res.append(item)
        else:
            idx = 0
            flag = 0
            while bpe_lst[idx].endswith('@@'):
                idx += 1
                flag = 1
            idx += 1
            if flag:
                word = (''.join(bpe_lst[:idx])).replace('@@','')
                assert word==item, 'Inconsistent bpe {}->{}'.format(word, item)
                new_str = ' '.join(bpe_lst[:idx])
            else:
                new_str = bpe_lst[0]
                assert new_str==item, 'Inconsistent bpe {}->{}'.format(new_str, item)
                idx = 1
            bpe_lst = bpe_lst[idx:]
            res.append(new_str)

    assert len(bpe_lst)==0, 'Error, there still are bpes unused {}'.format(bpe_lst)
    return res

if __name__ == '__main__':
    for path in ['data/dev-dfs-linear_src.txt', 'data/test-dfs-linear_src.txt', 'data/training-dfs-linear_src.txt', ]:
        print(path)
        for i, line in enumerate(open(path, 'rU')):
            amr_node = []
            amr_edge = []
            read_anonymized(line.strip().split(), amr_node, amr_edge)

