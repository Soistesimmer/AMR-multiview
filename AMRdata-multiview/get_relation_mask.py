import numpy as np
if __name__ == '__main__':
    mask='/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/0/train.align'
    relation='/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/0/train.al2'
    vocab='/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/gq_relation_vocab'
    output='/home/wangante/work-code-20190910/AMRdata-multiview/LDC2015/0/train.rm'
    vocab_size=50
    with open(mask,'r')as file:
        mask=[line for line in file.readlines()]
        for index, x in enumerate(mask):
            x=np.array(x.split()).astype(int)
            length=int(np.sqrt(np.size(x)))
            x=x.reshape(length, length)
            mask[index]=x.sum(1)
    with open(relation,'r')as file:
        relation=[line.split() for line in file.readlines()]
    with open(vocab,'r')as file:
        vocab=[line.split() for line in file.readlines()]
        # vocab_size=len(vocab)
        vocab={line[1]:int(line[0]) for line in vocab}
    relation_mask=[]
    for x, y in zip(mask, relation):
        rm=np.zeros((np.size(x),vocab_size)).astype(int)
        i=0
        for index, z in enumerate(x):
            for _ in range(z):
                try:
                    rm[index][vocab[y[i]]]=1
                except:
                    rm[index][vocab['<unk>']] = 1
                i+=1
        rm=rm.reshape(-1).astype(str)
        relation_mask.append(' '.join(rm.tolist()))
    with open(output, 'w')as file:
        file.write('\n'.join(relation_mask))
