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
    in_file, in_dir, o_file1, o_file2, o_file3, o_file4, o_file5, o_file6 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[
        5], sys.argv[6], sys.argv[7], sys.argv[8]

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
        amrs, text, concepts, alignments, al2s, un_toks = [], [], [], [], [], []
        inconsist_sent_counter = 0
        total_number=0
        tmp_count = 0
        for item in input_list:
            id = item['id']
            [ori_ali, ori_sent, al2] = origin_amr[id]

            simplified_amr = remove_wiki(item['amr'].strip().split())
            amrs.append(' '.join(simplified_amr))

            sent = item['sent']
            total_number+=1
            if sent != ori_sent:
                inconsist_sent_counter += 1
            ori_tok=ori_sent.split()
            tokens = nlp.word_tokenize(sent)
            ali_tok=ori_ali.split()
            for i,a in enumerate(ali_tok):
                a=a.split('-')
                a[0]=int(a[0])
                b=-1
                for index, tok in enumerate(tokens):
                    if ori_tok[a[0]]==tok:
                        b=index
                        break
                if b==-1:
                    for index, tok in enumerate(tokens):
                        if tok.startswith(ori_tok[a[0]]):
                            b = index
                            break
                    if b==-1:
                        raise Exception([ori_sent, sent, a[0], ori_tok[a[0]]])
                ali_tok[i]=str(b)+'-'+a[1]

            ori_ali=' '.join(ali_tok)
            un_toks.append(sent)
            sent=' '.join(tokens)
            alignments.append(ori_ali)
            al2s.append(al2)
            text.append(sent)
            concepts.append(' '.join(get_concepts(simplified_amr)))
        print(tmp_count)

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
            f6.write('\n'.join(un_toks))
