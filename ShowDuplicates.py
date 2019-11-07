#!/usr/bin/env python
## @author Miguel Maltez Jose
# ToDo:
# - reimplement using less numerical constants for indexing.
from __future__ import print_function
import sys
from util import loadTSV, TSVToTuple, tupleToTSV

BYTECOUNT_FIELD=-3

def engineeringNotation(number):
	"""Retuns a string with an approximation of the number
	in engineering notation.
	"""
	if number > 2**30:
		return "%dG" % int(number/2**30)
	elif number > 2**20:
		return "%dM" % int(number/2**20)
	elif number > 2**10:
		return "%dk" % int(number/2**10)
	else:
		return "%d" % int(number)

########
# MAIN #
########
import argparse
desc = """Show name of files with duplicated sha1.
	Also shows the byte sum of the duplicated files."""
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("FHLfile", type=argparse.FileType('r')
					, nargs='?', default=sys.stdin
					, help="hash list file, defaults to stdin")
args = parser.parse_args()

infolist = loadTSV(args.FHLfile)
args.FHLfile.close()

# A sorted list has all the duplicated items in sequence.
# So if the first is taken and the next one is not the same,
# then it is unique.
infolist.sort(key=lambda x: x[0])
## dictionary of info items with duplicate key, indexed by that key
dups = {}
previous = infolist[0]
for info in infolist[1:]:
	if previous[0] == info[0]:
		if not dups.has_key(previous[0]):
			# create new entry for this key
			dups[previous[0]] = [previous]
		dups[previous[0]].append(info)
	previous = info

grandtotalsize = 0
groups = []
for hash, il in dups.items():
	totalbytecount = 0
	for info in il:
		totalbytecount += int(info[BYTECOUNT_FIELD])
	groups.append([totalbytecount,il])
	grandtotalsize += totalbytecount

# print information about duplicates, sorted by space
groups.sort(key=lambda x: x[0])
for group in groups:
	size=engineeringNotation(group[0])
	title="%%%% [%s] = %s ~ %sB" % (group[1][0][0], group[0], size)
	print("\033[1m%s\033[0m" % title, file=sys.stderr)
	for info in group[1]:
		print(tupleToTSV(info[-3:]))

if grandtotalsize > 0:
	reportString="%% TOTAL ~ %s" % engineeringNotation(grandtotalsize)
	print(reportString, file=sys.stderr)

exit(0)