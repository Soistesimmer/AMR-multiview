import random
import re
import sys
import itertools
from sys import exit


def draw_amr_graph(example):
    match = 0
    lb = 0
    rb = 0
    result = []
    result.append(example[0])
    for index, token in enumerate(example[1:]):
        if token == '(':
            if match == 0:
                lb = index
            match += 1
        elif token == ')':
            match -= 1
            if match == 0:
                rb = index
                result.append(draw_amr_graph(example[lb + 2:rb + 1]))
        elif match == 0:
            result.append(example[index + 1])
    return result


def reconstruct_concept_sequence(result):
    str = []
    str += [result[0]]
    if len(result) == 1:
        return str
    children = result[1:]
    random.shuffle(children)
    for child in children:
        if isinstance(child, list):
            str += reconstruct_concept_sequence(child)
        else:
            str += [child]
    return str


def draw_amr_graph_w_relation(relation, example):
    match = 0
    lb = 0
    rb = 0
    result = []
    result.append((relation, example[0]))
    for index, token in enumerate(example[1:]):
        if token == '(':
            if match == 0:
                lb = index
            match += 1
        elif token == ')':
            match -= 1
            if match == 0:
                rb = index
                result.append(draw_amr_graph_w_relation(example[lb], example[lb + 2:rb + 1]))
        elif match == 0 and token[0] == ':' and len(token)>1 and example[index + 2] != '(':
            result.append((example[index + 1], example[index + 2]))
    return result


def reconstruct_amr_sequence(result):
    str = []
    flag = False
    if result[0][0] == ':root':
        str += [result[0][1]]
    else:
        flag = True
        str += [result[0][0], '(', result[0][1]]
    if len(result) == 1:
        if flag:
            return str+[')']
        else:
            return str
    children = result[1:]
    random.shuffle(children)
    for child in children:
        if isinstance(child, list):
            str += reconstruct_amr_sequence(child)
        else:
            str += [child[0], child[1]]
    if flag:
        return str + [')']
    return str


def main_with_relation():
    i_file, o_file, redundancy = sys.argv[1], sys.argv[2], sys.argv[3]
    redundancy = int(redundancy)

    random_amrs = []

    with open(i_file, 'r')as file:
        amrs = file.readlines()
        for i, amr in enumerate(amrs):
            amr=amr.strip()
            example = amr.split()
            result = draw_amr_graph_w_relation(':root',example)
            amr_list = []
            cal_count = 0
            while len(amr_list) != redundancy:
                amr1 = reconstruct_amr_sequence(result)
                assert len(example) == len(amr1), (amr, amr1, len(example), len(amr1))
                amr1 = ' '.join(amr1)
                if amr1 not in amr_list or cal_count >= 5 * redundancy:
                    amr_list.append(amr1)
                cal_count += 1
            random_amrs.append(' '.join(amr_list))

    with open(o_file, 'w')as file:
        file.write('\n'.join(random_amrs))


if __name__ == '__main__':
    # # example = "find-out :arg0 we :arg1 this :time ( about :time ( date-entity :day 23 :month 12 :year 2009 :time 19:30 ) ) :time-of ( phone :arg0 ( person :arg0-of ( have-rel-role :arg1 she :arg2 mum ) ) :arg1 she :arg2 ( say :arg0 person :arg1 ( and :op1 ( be-located-at :arg1 ( person :arg0-of ( have-rel-role :arg1 person :arg2 husband ) ) :arg2 ( back :op1 house ) ) :op2 ( want :arg0 person :arg1 ( talk :arg0 person :arg1 event ) ) ) ) )"
    # example="or :mode interrogative :op1 ( minority :arg0-of ( live :location ( world-region ) ) :mod ( ethnic-group :polarity - :name ( name :op1 arab ) ) :domain you ) :op2 ( know :arg0 you :arg1 ( someone :arg0-of ( live :location world-region ) ) )"
    # # example = re.sub(r'\s:.*?\s', ' ', example)
    # example = example.split()
    # # result = draw_amr_graph(example)
    # result = draw_amr_graph_w_relation(':root', example)
    # # concept = ' '.join(reconstruct_concept_sequence(result))
    # amr = ' '.join(reconstruct_amr_sequence(result))
    # print(example)
    # print(result)
    # # print(concept)
    # for i,x in enumerate(amr.split()):
    #     print(example[i],x)
    # exit()

    main_with_relation()
    exit()

    i_file, i_file2, o_file, redundancy = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    redundancy = int(redundancy)

    concepts = []
    with open(i_file2, 'r')as file:
        b_concepts = [concept for concept in file.readlines()]

    with open(i_file, 'r')as file:
        amrs = file.readlines()
        for i, amr in enumerate(amrs):
            example = re.sub(r'\s:.*?\s', ' ', amr)
            example = example.split()
            result = draw_amr_graph(example)
            concept_list = []
            cal_count = 0
            while len(concept_list) != redundancy:
                concept = reconstruct_concept_sequence(result)
                assert len(concept) == len(b_concepts[i].split()), amr
                concept = ' '.join(concept)
                if concept not in concept_list or cal_count >= 5 * redundancy:
                    concept_list.append(concept)
                cal_count += 1
            concepts.append(' '.join(concept_list))

    with open(o_file, 'w')as file:
        file.write('\n'.join(concepts))
