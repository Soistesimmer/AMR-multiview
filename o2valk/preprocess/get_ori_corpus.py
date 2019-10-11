import argparse
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-src')
parser.add_argument('-tgt')
parser.add_argument('-combine', default=None)
args = parser.parse_args()

with open(args.input, 'r') as input:
    amr = json.load(input)
    source, target = zip(*[(instance['amr'], instance['sent']) for instance in amr])

with open(args.src, 'w') as output:
    output.writelines('\n'.join(source))

with open(args.tgt, 'w') as output:
    output.writelines('\n'.join(target))

if args.combine:
    with open(args.combine, 'w')as output:
        combine = list(source) + list(target)
        random.shuffle(combine)
        output.writelines('\n'.join(combine))
