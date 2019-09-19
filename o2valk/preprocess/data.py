import os
import re
import pandas as pd
import stanfordnlp


def break_amr_instance(example):
    example = example.strip().lower().split('\n')
    example_id = example[0].split()[2]
    # print(example_id)
    target = example[1][8:]
    # print(target)
    example = ' '.join(example[3:])
    example = re.sub(r'\s+', ' ', example).strip()  # remove space
    # print(example)
    nodes = re.findall(r'(\w+\d*)\s/\s(.+?)[\s)]', example)  # extract all nodes
    nodes = dict(zip([node[0] for node in nodes], [re.sub(r'(.+?)-0\d*', lambda x: x.group(1), node[1]) for node in
                                                   nodes]))  # convert list to dict and remove senses
    # print(nodes)
    # print(break_basket(example, nodes))
    return (example_id, break_basket(example, nodes), target)


# break basket '( )' layer by layer
def break_basket(example, nodes):
    str = ''
    match_basket = 0
    left_basket_position = -1
    right_basket_position = -1
    try:
        root_node = example[1:example.index(' /')]
    except:
        return example
    example = example[1:-1]
    for (i, letter) in enumerate(example):
        if letter == '(':
            match_basket += 1
            if left_basket_position == -1 or match_basket == 1:
                left_basket_position = i
        elif letter == ')':
            match_basket -= 1
            if match_basket == 0:
                str += extract_relation(example[right_basket_position + 1: left_basket_position], nodes)
                right_basket_position = i
                # print(example[left_basket_position:right_basket_position + 1])
                str += break_basket(example[left_basket_position:right_basket_position + 1], nodes)
    if str == '':
        str += extract_relation(example, nodes)
    if str == '':
        return nodes[root_node] + ' '
    return '( ' + nodes[root_node] + ' ' + str + ') '


# extract relation like ':arg1'
def extract_relation(example, nodes):
    flag = False
    str = ''
    for item in example.split():
        if flag:
            entity = re.sub(r'\"?(.*?)\"?\)*', lambda x: x.group(1), item) + ' '
            if entity in nodes:
                entity = nodes[entity]
            str += entity
            flag = False
        elif item[0] == ':' and item != ':wiki':
            flag = True
            str += item + ' '
    return str


def combine_all_files_in_dir(dir, output):
    amr_list = []
    files = os.listdir(dir)
    for file in files:
        print('Begin linearizing file', file)
        with open(os.path.join(dir, file), 'r') as f:
            amr_example = ''
            flag = False
            for line in f.readlines()[1:]:
                if not line.strip():
                    flag = not flag
                    if not flag:
                        amr_list.append(break_amr_instance(amr_example))
                        amr_example = ''
                if flag:
                    amr_example += line
    dataset = pd.DataFrame(columns=['id', 'amr_seq', 'target'], data=amr_list)
    dataset.to_csv(output, index=False)


if __name__ == '__main__':
    dir_path = 'abstract_meaning_representation_amr_2.0/data/amrs/split'
    output_dir_path = 'corpus'
    train_path = os.path.join(dir_path, 'training')
    dev_path = os.path.join(dir_path, 'dev')
    test_path = os.path.join(dir_path, 'test')
    train_output_path = os.path.join(output_dir_path, 'train.csv')
    dev_output_path = os.path.join(output_dir_path, 'dev.csv')
    test_output_path = os.path.join(output_dir_path, 'test.csv')
    combine_all_files_in_dir(train_path, train_output_path)
    combine_all_files_in_dir(dev_path, dev_output_path)
    combine_all_files_in_dir(test_path, test_output_path)

    # example when testing
    example = '''# ::id bolt12_07_4800.3 ::date 2012-12-20T08:37:49 ::annotator SDL-AMR-09 ::preferred
    # ::snt 1. Establish an innovation fund with a maximum amount of 1,000 U.S. dollars.
    # ::save-date Mon Oct 12, 2015 ::file bolt12_07_4800_3.txt
    (e / establish-01 :li 1
          :ARG1 (f2 / fund
                :purpose (i / innovate-01)
                :ARG1-of (a / amount-01
                      :ARG2 (a2 / at-most
                            :op1 (m / monetary-quantity :quant 1000
                                  :unit (d / dollar
                                        :mod (c / country :wiki "United_States"
                                              :name (n / name :op1 "United" :op2 "States"))))))))
    '''
    # print(break_amr_instance(example))
