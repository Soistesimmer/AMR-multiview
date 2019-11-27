# coding-utf-8

import sys


if __name__=='__main__':
    
    input_f, output_f = sys.argv[1], sys.argv[2]
    
    res = [] 
    with open(input_f, 'r') as f1:
        for line in f1:
            bpe_lst = line.strip().split()
            i = 0
            while(bpe_lst[i].endswith('@@')):
                i+=1
            i += 1
            new_str = (''.join(bpe_lst[:i])).replace('@@','') # the first word can not be bped
            new_bpe_lst = [new_str]+bpe_lst[i:]
            res.append(' '.join(new_bpe_lst))

    with open(output_f,'w') as f2:
        f2.write('\n'.join(res))
