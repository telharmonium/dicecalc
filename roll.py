#!/usr/bin/env python
import pprint
import argparse
from dicecalc import calc

parser = argparse.ArgumentParser()
parser.add_argument("roll", help="Enter a dice expression here.")
parser.add_argument('-v', action="store_true", dest="v", default=False, help="Print verobse result.")

args = parser.parse_args()

rollResult = calc(args.roll)

if args.v:
	pprint.pprint(rollResult)
else:
	print rollResult['result']
