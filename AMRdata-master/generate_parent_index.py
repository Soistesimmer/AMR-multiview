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

def gen_par_index_seq(example):
    tokens=example.split()
    alignment={}
    root_f={}
    for tok in tokens:
        tok=tok.split('-')
        if tok[1].endswith('r'):
            continue
        alignment[tok[1]]=tok[0]
    for ali in alignment:
        for ali2 in alignment:
            if ali.startswith(ali2) and charge_one_dot(ali[len(ali2):]):
                if alignment[ali] in root_f:
                    root_f[alignment[ali]].append(alignment[ali2])
                    # print('WARN: multi-in alert!', example)
                root_f[alignment[ali]]=[alignment[ali2]]
    return root_f


if __name__ == '__main__':
    # example='1-1.2.1.r 2-1.1 6-1.1.1 7-1.1.1.1.r 8-1.1.1.1 10-1.1.1.2.3 11-1.1.1.2 12-1.1.1.2.3.r 13-1.1.1.2.2 13-1.1.1.2.2.1.1 14-1.1.1.2.2.1 16-1.2.1 17-1.2.1.r 18-1.2 19-1.2.2 21-1.3.1 22-1.3.1.r 23-1.3 24-1.3.2 26-1.4.1 27-1.4 28-1.4.2.1.1 30-1.4.2.1 31-1.4.2'
    with open('/home/wangante/work-code-20190910/AMRdata-master/LDC2015/dev.align') as file:
        for example in file.readlines():
            gen_par_index_seq(example)
