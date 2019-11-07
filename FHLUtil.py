#!/usr/bin/env python
"""File Hash list utility functions.
@author Miguel Maltez Jose
@date 20190720
"""

def loadFHL(fhlfile):
	"""Load File Hash List from a file and returns list of FileInfo tuples."""
	res = []
	for line in fhlfile:
		if (line[0] == '#'): continue # ignore comment lines
		line = line.rstrip()
		row = tuple(line.split('\t'))
		if len(row) == 6:
			res.append(row)
	return res

def groupBySHA1(flatlist):
	"""Run through a list of FileInfo tuples and group them into lists
	in a dictionary.
	@return a triplet of dictionaries
		[ group member count
		, total byte size of group
		, list of FileInfo tuples in the group ]
	"""
	freq = {}
	size = {}
	groups = {}
	for item in flatlist:
		key = item[0]
		freq[key] = freq.get(key, 0) + 1
		size[key] = size.get(key, 0) + int(item[3])
		groups[key] = groups.get(key, []) + [item]
	return [freq, size, groups]
