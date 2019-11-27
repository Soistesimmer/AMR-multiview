from amr_utils import read_json

if __name__ == '__main__':
    i_file='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/dev.json'
    i_file2=''
    o_file='/home/wangante/work-code-20190910/AMRdata-master/LDC2015/dev.sent'
    input_list=read_json(i_file)
    sents=[]
    for item in input_list:
        sents.append(item['sent'])
    with open(o_file, 'w') as f:
        f.write('\n'.join(sents))