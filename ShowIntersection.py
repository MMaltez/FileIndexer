#!/usr/bin/env python
## Shows files in listA also in listB.
## Does this by comparing content hashes.
## @author Miguel Maltez Jose
## @date 20130416
# ToDo:
from __future__ import print_function
import sys
from util import TSVToTuple, tupleToTSV, loadTSV

HASHFIELD=0
PATHNAMEFIELD=-1

def printList(l):
	for row in l:
		print(row)

########
# MAIN #
########
import argparse
desc = """Show files in listA that are also in listB."""
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("listAfile", type=argparse.FileType('r')
					, help="listA")
parser.add_argument("listBfile", type=argparse.FileType('r')
					, nargs='?', default=sys.stdin
					, help="listB, defaults to stdin")
args = parser.parse_args()

listA = loadTSV(args.listAfile)
listB = loadTSV(args.listBfile)
args.listAfile.close()
args.listBfile.close()

## "list" of unique hashes in listB
hashlistB = {}
for info in listB:
	if not hashlistB.has_key(info[HASHFIELD]):
		hashlistB[info[HASHFIELD]] = [info]
	else:
		hashlistB[info[HASHFIELD]].append(info)
## non overlaping file info
outsidelist=[]
## overlapping file info
insidelist=[]
for info in listA:
	if hashlistB.has_key(info[HASHFIELD]):
		insidelist.append(info)
	else:
		outsidelist.append(info)

for info in insidelist:
	print(tupleToTSV(info[-3:]))

exit(0)