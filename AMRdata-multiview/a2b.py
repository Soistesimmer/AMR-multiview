# 让alignments对齐到bpe后sentence
import pickle
import sys

from generate_parent_index import gen_par_index_seq
import re
from sys import exit

def a2b(sent, bpe_sent, ori_ali, with_r, al2):
    bpe_sent=re.sub(r'@@','',bpe_sent)
    tokens = sent.split()
    bpe_tokens=bpe_sent.split()
    length=len(bpe_tokens)
    # bpe后 当前句子中词在原句中位置
    transform_A = []
    # bpe后 原句中词在当前句中最后的位置
    transform_B = {}
    ori_index = 0
    tmp_token = ''
    for index, token in enumerate(bpe_tokens):
        tmp_token += token
        transform_A.append(ori_index)
        transform_B[ori_index] = index
        if tmp_token == tokens[ori_index]:
            ori_index += 1
            tmp_token = ''
    if ori_index!=len(tokens):
        print(transform_A)
        print(transform_B)
        raise Exception('WARNING: {} and {} not match'.format(sent, bpe_sent))
    new_al2=[]
    for item in al2:
        y=item[0].split(',')
        for x in y:
            new_al2.append([int(x), item[2].split(',')[0]])
    al2=new_al2
    ali, ali2 = gen_par_index_seq(ori_ali, with_r, al2)
    ali_seq = []
    ali_seq2= []
    # print(ali)
    # print(ali2)
    last_key=None
    for i in range(length):
        tmp_list = [0] * length
        key = str(transform_A[i])
        if key==last_key:
            ali_seq += tmp_list
            continue
        last_key=key
        if key in ali:
            for a in ali[key]:
                tmp_list[int(transform_B[int(a)])] = 1
                # print(bpe_tokens[i],bpe_tokens[int(transform_B[int(a)])])
            for b in ali2[key]:
                ali_seq2.append(b)
        ali_seq += tmp_list
    count=0
    for x in ali_seq:
        if x==1:
            count+=1
    assert count==len(ali_seq2),(count, len(ali_seq2), ali, ali2)
    ali_seq = ' '.join([str(x) for x in ali_seq])
    ali_seq2 = ' '.join([str(x) for x in ali_seq2])
    return ali_seq, ali_seq2


if __name__ == '__main__':
 #    sent='liu jianchao said that no plans for another such test by the secretive chinese military .'
 #    bpe_sent='liu jian@@ chao said that no plans for another such test by the secre@@ tive chinese military .'
 #    ali='0-1.1.2.1 1-1.1.2.2 2-1 3-1.2.r 4-1.2.1 4-1.2.1.r 5-1.2 6-1.2.3.r 7-1.2.3.1 8-1.2.3.2 9-1.2.3 10-1.2.2.r 12-1.2.2.2 13-1.2.2.1.2.1 14-1.2.2'
 #    al2=[['2', 'say-01~e.2', ':root'],
 # ['5', 'plan-01~e.5', ':ARG1'],
 # ['14', 'military~e.14', ':ARG0'],
 # ['12', 'secretive~e.12', ':mod'],
 # ['9', 'test~e.9', ':ARG1'],
 # ['7', 'another~e.7', ':mod'],
 # ['8', 'such~e.8', ':mod']]
 #    print(a2b(sent, bpe_sent, ali, False, al2))
 #    exit()
    in_file1, in_file2, in_file3, in_file4, o_file1, o_file2, with_r= sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
    with open(in_file1,'r')as f:
        sents=f.readlines()
    with open(in_file2, 'r')as f:
        bpe_sents = f.readlines()
    with open(in_file3,'r')as f:
        alis=f.readlines()
    with open(in_file4,'rb')as f:
        al2s=pickle.load(f)
    ali_seqs=[]
    for i, sent in enumerate(sents):
        bpe_sent=bpe_sents[i]
        ali=alis[i]
        al2=al2s[i]
        # print(sent)
        # print(bpe_sent)
        ali_seqs.append(a2b(sent, bpe_sent, ali, with_r, al2))
    with open(o_file1,'w')as f:
        f.write('\n'.join([x for x,y in ali_seqs]))
    with open(o_file2,'w')as f:
        f.write('\n'.join([y for x,y in ali_seqs]))