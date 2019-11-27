# /usr/bin/python
# coding:utf-8
import pickle
import re
import sys
import json
import os
import argparse
from stanfordcorenlp import StanfordCoreNLP
from amr_utils import read_json, remove_wiki, read_anonymized, get_concepts
from generate_parent_index import gen_par_index_seq

if __name__ == '__main__':
    nlp = StanfordCoreNLP(r'/home/wangante/stanford-corenlp-full-2018-10-05', lang='en')
    in_file, in_dir, o_file1, o_file2, o_file3, o_file4, o_file5, o_file6, o_file7 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[
        5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]

    origin_amr = {}
    for file_name in os.listdir(in_dir):
        with open(os.path.join(in_dir, file_name)) as file:
            for example in file.read().strip().split('\n\n')[1:]:
                example = example.split('\n')
                origin_amr[example[0].split()[2]] = [example[2][len('# ::alignments '):],
                                                     example[1][len('# ::tok '):].lower(),
                                                     ' '.join(example[3:])]

    input_list = read_json(in_file)
    num_items = len(input_list[0])
    regu = re.compile(r'[^:][^\s]*?~e\.\d+')
    for id, amr in origin_amr.items():
        amr=amr[2].split()
        result=[]
        for index, token in enumerate(amr):
            token=re.sub(r'\)*','',token)
            if regu.match(token):
                tmp=index-1
                rel=None
                while tmp>0:
                    if amr[tmp].startswith(':'):
                        rel=amr[tmp]
                        rel=re.sub(r'~e\.\d+','',rel)
                        break
                    else:
                        tmp-=1
                if rel is None:
                    rel=':root'
                result.append([token.split('~e.')[1], token, rel])
        origin_amr[id][2]=result
    if num_items in [2, 3]:
        amrs, text, concepts, alignments, al2s, gold_reference, un_toks = [], [], [], [], [], [], []
        inconsist_sent_counter = 0
        total_number=0
        for item in input_list:
            id = item['id']
            [ori_ali, ori_sent, al2] = origin_amr[id]

            simplified_amr = remove_wiki(item['amr'].strip().split())
            amrs.append(' '.join(simplified_amr))

            a_length=len(ori_sent.split())
            ori_sent=ori_sent.replace('\'\'','"')
            ori_sent = ori_sent.replace('``', '"')
            ori_sent = ori_sent.replace('\' ', '" ')
            b_length=len(ori_sent.split())
            assert a_length==b_length
            sent = item['sent']
            # sent=re.sub(r'([a-zA-Z0-9]+)\s@-@([a-zA-Z]+)', lambda m: m.group(1) + '-' + m.group(2),
            #                   sent)
            total_number+=1
            if sent != ori_sent:
                inconsist_sent_counter += 1
            tokens=nlp.word_tokenize(sent)
            sent=re.sub(r'\s@\s?(.)\s?@\s',lambda m: ' @'+m.group(1)+'@ ',' '.join(tokens))
            sent=re.sub(r'([a-zA-Z0-9]+)\s@\s-@([a-zA-Z]+)', lambda m: m.group(1) + ' @-@ ' + m.group(2),
                              sent)
            un_toks.append(ori_sent)
            ori_tokens=nlp.word_tokenize(ori_sent)
            ori_sent=re.sub(r'\s@\s?(.)\s?@\s',lambda m: ' @'+m.group(1)+'@ ',' '.join(ori_tokens))
            # # 超麻烦的alignment迁移 **这部分已换到a2b.py实现
            # length=len(tokens)
            # ori_tokens=ori_sent.split()
            # transform_A=[]
            # transform_B={}
            # ori_index=0
            # tmp_token=''
            # for index, token in enumerate(tokens):
            #     tmp_token+=token
            #     transform_A.append(ori_index)
            #     transform_B[ori_index]=index
            #     if tmp_token==ori_tokens[ori_index]:
            #         ori_index+=1
            #         tmp_token=''
            # ali=gen_par_index_seq(ori_ali)
            # ali_seq=[]
            # for i in range(length):
            #     tmp_list=[0]*length
            #     key=str(transform_A[i])
            #     if key in ali:
            #         for a in ali[key]:
            #             tmp_list[int(transform_B[int(a)])]=1
            #     ali_seq+=tmp_list
            # ali_seq=' '.join([str(x) for x in ali_seq])
            # alignments.append(ali_seq)

            alignments.append(ori_ali)
            al2s.append(al2)
            text.append(ori_sent)
            gold_reference.append(sent)
            # text.append(' '.join(tokens))
            # text.append(sent)
            concepts.append(' '.join(get_concepts(simplified_amr)))

        print('INFO: {}/{} sent are not consist in {}'.format(inconsist_sent_counter,total_number,in_file))
        with open(o_file1, 'w') as f1:
            f1.write('\n'.join(amrs))
        with open(o_file2, 'w') as f2:
            f2.write('\n'.join(text))
        with open(o_file3, 'w') as f3:
            f3.write('\n'.join(concepts))
        with open(o_file4, 'w') as f4:
            f4.write('\n'.join(alignments))
        with open(o_file5, 'wb') as f5:
            pickle.dump(al2s, f5)
        with open(o_file6, 'w') as f6:
            f6.write('\n'.join(gold_reference))
        with open(o_file7, 'w') as f7:
            f7.write('\n'.join(un_toks))
