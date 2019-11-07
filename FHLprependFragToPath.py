#!/usr/bin/python
"""Prepends a string fragment to the last field of a TSV line in
 the FHL file.

@author Miguel Maltez Jose
@created 20130619
@date 20160807
"""
from __future__ import print_function
import sys
import argparse

def processTSVLine(line):
	res = []
	end = beg = 0
	while True:
		end = line.find("\t",beg)
		if end == -1:
			res.append(line[beg:])
			break
		else:
			res.append(line[beg:end])
		beg = end + 1
	return (res)

########
# MAIN #
########
desc="""Prepends a string fragment to the last field of a TSV line in
 the FHL file.
Tab Separated Value (TSV).
"""
argparser = argparse.ArgumentParser(description=desc)
argparser.add_argument("fragment", help="fragment to be prepended")
argparser.add_argument("FHLfile", type=argparse.FileType("r"),
                       default=sys.stdin, nargs="?",
					   help="input file hash list, defaults to stdin")
args = argparser.parse_args()

# read information to a list of tuples
for line in args.FHLfile:
	if len(line) > 0 and line[0] not in '#;%':
		info = (processTSVLine(line.rstrip()))
		info[-1] = args.fragment + info[-1]
		i = 0
		while i<len(info)-1:
			print(info[i], end='\t')
			i += 1
		print(info[i])

args.FHLfile.close()

exit(0)
