import difflib
import sys
import os

from amr_utils import read_json, remove_wiki

in_dir, in_file, o_file, o_file2 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

origin_sent = []
origin_align = []
for file_name in os.listdir(in_dir):
    with open(os.path.join(in_dir, file_name)) as file:
        for example in file.read().strip().split('\n\n')[1:]:
            example = example.split('\n')
            origin_sent.append(example[1][len('# ::tok '):].lower())
            origin_align.append(example[2][len('# ::alignments '):])

input_list = read_json(in_file)
num_items = len(input_list[0])

alignments = []
sents=[]
if num_items in [2, 3]:
    for item in input_list:
        sent = item['sent']
        try:
            index = origin_sent.index(sent)
            sents.append(sent)
            alignments.append(origin_align[index])
        except:
            max_ratio = -1
            match_index = -1
            for index, tok in enumerate(origin_sent):
                seq = difflib.SequenceMatcher(None, tok, sent)
                if seq.ratio() > max_ratio:
                    max_ratio = seq.ratio()
                    match_index = index
            alignments.append(origin_align[match_index])
            sents.append(origin_sent[match_index])

with open(o_file, 'w') as file:
    file.write('\n'.join(alignments))

with open(o_file2,'w')as file:
    file.write('\n'.join(sents))
