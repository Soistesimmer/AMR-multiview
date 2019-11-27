# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import os
import sys
import time
import numpy as np
import codecs

import json
import amr_utils


class Graph:
    def __init__(self, maps={}):
        self.map = maps  #
        self.nodenum = len(maps)
        self.nodes = list(range(self.nodenum))

    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.map:
            return None
        for node in self.map[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None


def create_structural_path(G1, G2, tags):
    tag_dict = {}
    for i in range(len(G2)):
        for j, tag in zip(G2[i], tags[i]):
            if i == j:
                tag_dict[(i, j)] = "None"
            else:
                if tag.startswith(':arg'):
                    tag = tag.replace('arg', 'ARG', 1)
                tag_dict[(i, j)] = '-' + tag
                tag_dict[(j, i)] = '+' + tag

    maps = {i: list(set(l[0] + l[1]) - set([i])) for i, l in enumerate(zip(G1, G2))}

    all_paths = {}
    graph = Graph(maps)
    for i in range(len(maps)):
        ith_path = []
        for j in range(len(maps)):
            path = graph.find_path(i, j)
            # pathstr = ''.join([tag_dict[path[a],path[a+1]] for a in range(len(path)-1)]) if len(path)>1 else 'None'
            if not path:
                print(i, j)
            pathstr = [tag_dict[path[a], path[a + 1]] for a in range(len(path) - 1)] if len(path) > 1 else ['None']
            all_paths[(i, j)] = pathstr
            if i == 0:
                EOS_str = ['+:EOS'] + pathstr if pathstr != ['None'] else ['+:EOS']
                all_paths[(len(maps), j)] = EOS_str
        endstr = all_paths[(i, 0)] + ['-:EOS'] if all_paths[(i, 0)] != ['None'] else ['-:EOS']
        all_paths[(i, len(maps))] = endstr
    all_paths[(len(maps), len(maps))] = ['None']
    return all_paths


def apply_bpe_edge(bpe_node_lst, node_lst, G1, tag1, G2, tag2):
    bpe2word = {}
    word2bpe = {}
    bpe_lst = bpe_node_lst
    start, index = 0, 0
    for i, word in enumerate(node_lst):
        word2bpe[i] = []
        if bpe_lst[start].endswith('@@'):
            index = start + 1
            while bpe_lst[index].endswith('@@'):
                index += 1
            cat_bpe = (''.join(bpe_lst[start:index + 1])).replace('@@', '')
            assert word == cat_bpe, 'Inconsistent bpe {}->{}'.format(cat_bpe, word)
            for j in range(start, index):
                bpe2word[j] = (i, False)
                word2bpe[i].append(j)
            bpe2word[index] = (i, True)  # Last bpe part
            word2bpe[i].append(index)
            start = index + 1
        else:
            assert word == bpe_lst[start], 'Inconsistent bpe {}->{}'.format(bpe_lst[start], word)
            bpe2word[start] = (i, True)
            word2bpe[i].append(start)
            start += 1

    ############transforme G1#############
    G1_new, tag1_new = [], []
    bpe_index = 0
    for i in range(len(bpe_node_lst)):
        Gi, tagi = [], []
        i_parent = bpe2word[i][0]
        bpe_end_flag = bpe2word[i][1]
        if bpe_index == 0:
            for Node_index, tag in zip(G1[i_parent], tag1[i_parent]):
                if Node_index == i_parent:  # Node to itself
                    Gi.append(i)
                    assert tag == ':self', 'Inconsistent tag, should be :self but get {}'.format(tag)
                    tagi.append(':self')
                else:  # Other node to node: i_parent
                    Gi.append(word2bpe[Node_index][-1])  # last children of Node_index
                    tagi.append(tag)  # same tag
        else:
            Gi.append(i)
            tagi.append(':self')
            Gi.append(word2bpe[i_parent][bpe_index - 1])
            tagi.append(':bpe')
        if bpe_end_flag:
            bpe_index = 0
        bpe_index += 1
        G1_new.append(Gi)
        tag1_new.append(tagi)

    ############transforme G2#############
    G2_new, tag2_new = [], []
    bpe_index = 0
    for i in range(len(bpe_node_lst)):
        Gi, tagi = [], []
        i_parent = bpe2word[i][0]  # word node
        bpe_end_flag = bpe2word[i][1]
        if bpe_end_flag is False:
            Gi.append(i)
            tagi.append(':self')
            Gi.append(word2bpe[i_parent][bpe_index + 1])
            tagi.append(':bpe')
            bpe_index += 1
        else:
            for Node_index, tag in zip(G2[i_parent], tag2[i_parent]):  # Node_index: output_node
                if Node_index == i_parent:  # Node out-to itself
                    Gi.append(i)
                    assert tag == ':self', 'Inconsistent tag, should be :self but get {}'.format(tag)
                    tagi.append(tag)
                else:  # Node to other node
                    if bpe2word[i][1]:  # last children of Node_index
                        for bpe_node in word2bpe[Node_index]:  # Node_index's all children
                            Gi.append(bpe_node)
                            tagi.append(tag)  # same tag
                    else:  # bpe_node_i is not the last child of i_parent
                        pass
            bpe_index = 0
        G2_new.append(Gi)
        tag2_new.append(tagi)

    return (G1_new, tag1_new, G2_new, tag2_new)


def read_amr_file(amr_path):
    nodes = []  # [batch, node_num,]
    in_neigh_indices = []  # [batch, node_num, neighbor_num,]
    in_neigh_edges = []
    out_neigh_indices = []  # [batch, node_num, neighbor_num,]
    out_neigh_edges = []
    max_in_neigh = 0
    max_out_neigh = 0
    max_node = 0
    with open(amr_path, "r") as f:
        for inst in f:
            amr = inst.strip()
            amr_node = []
            amr_edge = []
            amr_utils.read_anonymized(amr.strip().split(), amr_node, amr_edge)
            # print(amr_edge)
            # 1.
            nodes.append(amr_node)
            # 2. & 3.
            in_indices = [[i, ] for i, x in enumerate(amr_node)]
            in_edges = [[':self', ] for i, x in enumerate(amr_node)]
            out_indices = [[i, ] for i, x in enumerate(amr_node)]
            out_edges = [[':self', ] for i, x in enumerate(amr_node)]
            for (i, j, lb) in amr_edge:
                in_indices[j].append(i)
                in_edges[j].append(lb)
                out_indices[i].append(j)
                out_edges[i].append(lb)
            in_neigh_indices.append(in_indices)
            in_neigh_edges.append(in_edges)
            out_neigh_indices.append(out_indices)
            out_neigh_edges.append(out_edges)
            # update lengths
            max_in_neigh = max(max_in_neigh, max(len(x) for x in in_indices))
            max_out_neigh = max(max_out_neigh, max(len(x) for x in out_indices))
            max_node = max(max_node, len(amr_node))
    return zip(nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices, out_neigh_edges)


if __name__ == '__main__':
    train_file, concept_bpe, path_out = sys.argv[1], sys.argv[2], sys.argv[3]
    # nodes_out = open('simplified_nodes.txt', "w")
    file_lst, content_lst = [], []
    for i in range(1, 9):  # Eight paths
        f = open(path_out + '_{}'.format(i), 'w')
        content_lst.append([])
        file_lst.append(f)

    path_out = open(path_out, "w")
    trainset = read_amr_file(train_file)
    all_paths, all_nodes = [], []
    bpe_f = open(concept_bpe, 'r')
    index = 0
    for amr_data, bpe_line in zip(trainset, bpe_f):
        index += 1
        nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices, out_neigh_edges = amr_data
        # print('======================{}========================='.format(index))
        # print(nodes)
        # print(in_neigh_indices)
        # print(in_neigh_edges)
        # print(out_neigh_indices)
        # print(out_neigh_edges)

        bpe_nodes = bpe_line.strip().split()
        G1, tag1, G2, tag2 = apply_bpe_edge(bpe_nodes, nodes, in_neigh_indices, in_neigh_edges, out_neigh_indices,
                                            out_neigh_edges)
        # print(bpe_nodes)
        # print(G1)
        # print(tag1)
        # print(G2)
        # print(tag2)
        bpe_path = create_structural_path(G1, G2, tag2)
        bpe_nodes.append('EOS')

        lineth_path = []
        kth_path = [[] for _ in range(8)]
        for i in range(len(bpe_nodes)):
            for j in range(len(bpe_nodes)):
                # print("{}->{}\t{}".format(bpe_nodes[i], bpe_nodes[j], bpe_path[(i, j)]))
                lineth_path.append(''.join(bpe_path[(i, j)]))
                for k in range(8):
                    label = bpe_path[(i, j)][k] if k < len(bpe_path[(i, j)]) else '<blank>'
                    kth_path[k].append(label)

        all_paths.append(' '.join(lineth_path) + ' ')

        for m in range(8):
            content_lst[m].append(' '.join(kth_path[m]) + ' ')
        # bpe_nodes.pop()
        # all_nodes.append(' '.join(bpe_nodes))
    path_out.write('\n'.join(all_paths))
    for idx, ff in enumerate(file_lst):
        ff.write('\n'.join(content_lst[idx]))
