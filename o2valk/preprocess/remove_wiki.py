import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-output')
args=parser.parse_args()

with open(args.input, 'r') as input:
    amr=json.load(input)
    for item in amr:
        example=item['amr'].split()
        while 1:
            try:
                p=example.index(':wiki')
                example=example[:p]+example[p+2:]
            except:
                break
        item['amr']=' '.join(example)

with open(args.output, 'w') as output:
    json.dump(amr,output)



