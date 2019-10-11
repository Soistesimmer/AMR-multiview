import argparse
import re

parser=argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-output')
args=parser.parse_args()


amr=[]
with open(args.input, 'r')as input:
    for example in input.readlines():
        example=example.strip()
        example=re.sub(r'@@\s', '', example)
        amr.append(example)

with open(args.output, 'w')as output:
    output.writelines('\n'.join(amr))
