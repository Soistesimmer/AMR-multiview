import os
import pickle
import re
from sys import exit

if __name__ == '__main__':
    in_dir='/home/wangante/work-code-20190910/o2valk/abstract_meaning_representation_amr_2.0/data/alignments/split/dev'
    out_file='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/dev.align2'
    ids=[]
    amrs=[]
    results={}
    for file_name in os.listdir(in_dir):
        with open(os.path.join(in_dir, file_name)) as file:
            for example in file.read().strip().split('\n\n')[1:]:
                example = example.split('\n')
                ids.append(example[0].split()[2])
                amrs.append(' '.join(example[3:]))
    regu=re.compile(r'\w.*?~e\.\d+')
    for id, amr in zip(ids, amrs):
        amr=amr.split()
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
                result.append([index, token, rel])
        results[id]=result
    with open(out_file, 'wb')as file:
        pickle.dump(results, file)




