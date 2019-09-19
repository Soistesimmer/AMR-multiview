import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('-train')
parser.add_argument('-target')
args=parser.parse_args()
concept=[]
target=[]
with open(args.train, 'r') as input:
    amr=json.load(input)
    target+=[instance['sent'] for instance in amr]

with open(args.target, 'w') as output:
    output.writelines('\n'.join(target))



