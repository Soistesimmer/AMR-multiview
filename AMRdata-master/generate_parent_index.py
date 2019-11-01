# 因为原AMR文件和simplify的文件中sentence有差异，需要对json文件中的sent进行替换！！

def charge_one_dot(str):
    count=0
    for let in str:
        if let=='.':
            count+=1
        if count > 1:
            return False
    if count==1:
        return True
    else:
        return False

def gen_par_index_seq(example, with_r):
    tokens=example.split()
    alignment={}
    root_f={}
    for tok in tokens:
        tok=tok.split('-')
        if with_r:
            pass
        elif tok[1].endswith('r'):
            continue
        alignment[tok[1]]=tok[0]
    for ali in alignment:
        for ali2 in alignment:
            if ali.startswith(ali2) and charge_one_dot(ali[len(ali2):]):
                if alignment[ali] in root_f:
                    root_f[alignment[ali]].append(alignment[ali2])
                    # print('WARN: multi-in alert!', example)
                else:
                    root_f[alignment[ali]]=[alignment[ali2]]
    return root_f


if __name__ == '__main__':
    example='0-1.1.1 1-1.1 2-1.3 2-1.3.r 3-1 4-1.2.r 6-1.2.1 8-1.2.2 9-1.2'
    print(gen_par_index_seq(example, True))
    # with open('/home/wangante/work-code-20190910/AMRdata-master/LDC2015/dev.align') as file:
    #     for example in file.readlines():
    #         gen_par_index_seq(example, False)
