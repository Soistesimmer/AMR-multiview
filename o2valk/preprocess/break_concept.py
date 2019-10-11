import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-vocab')
parser.add_argument('-vocab_bpe')
parser.add_argument('-input')
parser.add_argument('-output')
args=parser.parse_args()

vocab_dict={}

with open(args.vocab,'r')as vocab:
    with open(args.vocab_bpe,'r')as vocab_bpe:
        vocab=vocab.readlines()
        vocab_bpe=vocab_bpe.readlines()
        if len(vocab_bpe)!=len(vocab):
            raise Exception('ERROR: The vocab files don\'t match!')
        for i,word in enumerate(vocab):
            vocab_dict[word.strip()]=vocab_bpe[i].strip()


def break_node(example):
    concept=example[0]
    concept=vocab_dict[concept]
    example = example[1:]
    relation = {}
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
        child=vocab_dict[example[0]]
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


def break_down_and_build_up(example_dict):
    keys = example_dict.keys()
    concept=[key for key in keys][0]
    r_key=':head'
    return ' '.join(break_concept(concept.split(), r_key, example_dict[concept]))


def break_concept(concept, relation, content):
    if len(concept)>2:
        return [concept[0]] + [relation] + ['('] + break_concept(concept[1:], relation, content) + [')']
    elif len(concept)==2:
        if content:
            return [concept[0]] + [relation] + ['('] + break_concept(concept[1:], relation, content) + [')']
        else:
            return [concept[0]]+[relation]+[concept[1]]
    else:
        if content:
            return [concept[0]]+break_relation(content)
        else:
            return [concept[0]]


def break_relation(example_dict):
    example_list=[]
    keys=example_dict.keys()
    for r_key in keys:
        child=example_dict[r_key]
        if isinstance(child, dict):
            concept=[c_key for c_key in child.keys()][0]
            example_list+=[r_key]+['(']+break_concept(concept.split(), r_key, child[concept])+[')']
        else:
            concept=child
            example_list+=[r_key]+break_concept(concept.split(),r_key, None)
    return example_list


with open(args.input, 'r')as input:
    with open(args.output, 'w')as output:
        amr=[]
        for example in input.readlines():
            example=break_down_and_build_up(break_node(example.split()))
            amr.append(example)
        output.writelines('\n'.join(amr))

# example="own :arg0 ( conglomerate :name ( name :op1 bertelsmann :op2 ag ) :mod ( country :name ( name :op1 germany ) ) :mod media ) :arg1 ( publication :name ( name :op1 rtl :op2 nieuws ) ) :mod ultimate"
# example_dict=break_node(example.split())
# print(break_down_and_build_up(example_dict))