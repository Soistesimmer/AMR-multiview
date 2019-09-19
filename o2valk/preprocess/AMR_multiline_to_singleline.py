import os
import sys
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-data')
parser.add_argument('-src')
parser.add_argument('-tgt')

args=parser.parse_args()

ids = []
id_dict = {}
amrs = []
targets=[]
amr_str = ''

files = os.listdir(args.data)
# amr graph to sequence
for file in files:
    print('Begin linearizing file', file)
    with open(os.path.join(args.data, file), 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                if line.startswith('# ::id'):
                    id = line.lower().strip().split()[2]
                    ids.append(id)
                    id_dict[id] = len(ids)-1
                if line.startswith('# ::snt'):
                    target=line.lower().strip()[8:]
                    targets.append(target)
                continue
            line = line.strip()
            if line == '':
                if amr_str != '':
                    amrs.append(amr_str.strip())
                    amr_str = ''
            else:
                amr_str = amr_str + line + ' '

        if amr_str != '':
            amrs.append(amr_str.strip())
            amr_str = ''

with open(args.src,'w') as src_file:
    src_file.writelines('\n'.join(amrs))

with open(args.tgt, 'w') as tgt_file:
    tgt_file.writelines('\n'.join(targets))

# find amr according to id
# if len(sys.argv) == 3:
#     for line in open(sys.argv[2],'rU'):
#         id = line.lower().strip()
#         print(amrs[id_dict[id]])
