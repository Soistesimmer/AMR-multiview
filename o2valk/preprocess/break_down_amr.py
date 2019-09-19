import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-output')
parser.add_argument('-vocab')
args=parser.parse_args()

concept_list=[]

def break_node(example):
    concept=example[0]
    concept_list.append(concept)
    example=example[1:]
    relation={}
    while 1:
        if not example:
            break
        relation[example[0]], example=find_relation(example)
    return {concept: relation}

def find_relation(example):
    example=example[1:]
    best_match = 0
    child=None
    if example[0]!='(':
        child=example[0]
        example=example[1:]
    else:
        for i,item in enumerate(example):
            if item=='(':
                best_match+=1
            elif item==')':
                best_match-=1
            if best_match==0:
                child=break_node(example[1:i])
                example=example[i+1:]
                break
    return child, example

# example="and :op1 ( lawyer :domain ( person :name ( name :op1 sulaiman :op2 al-rushoodi ) :arg1-of ( include :arg2 ( group :consist-of ( activist :arg1-of ( detain :time ( date-entity :year 2004 ) ) ) ) ) ) ) :op2 ( have-org-role :arg0 person :arg3 judge :time former )"
with open(args.input, 'r')as input:
    train=json.load(input)
    for instance in train:
        example=instance['amr']
        example=example.split()
        break_node(example)
with open(args.output, 'w')as output:
    output.writelines('\n'.join(concept_list))
with open(args.vocab, 'w')as output:
    output.writelines('\n'.join(set(concept_list)))
