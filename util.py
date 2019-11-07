"""Utility functions
A bunch of useful functions.
"""
import os
from datetime import datetime

def tupleToTSV(t):
	"""Converts a tuple to a string with tab separated values."""
	line = ""
	for item in t:
		line += "%s" % item
		line += '\t'
	return line[:-1]

def TSVToTuple(line):
	"""Returns a tuple with the strings that where separated by tabs."""
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
	return tuple(res)

def loadTSV(tsvfile):
	valuelist = []
	readcount = 0
	commentcount = 0
	for line in tsvfile:
		line = line.rstrip()
		if len(line) > 0 :
			if line[0] not in '#;%':
				info = TSVToTuple(line)
				valuelist.append(info)
				readcount += 1
			else:
				commentcount += 1
	return valuelist

def loadTSVFromFile(TSVfilename):
	"""Loads file info list from tsv file.

	Ignores empty lines and comment lines,
	i.e. lines starting with semicolon or hash sign.
	@return tuple list of tab separated strings.
	"""
	valuelist=[]
	try:
		tsvfile = open(TSVfilename, 'r')
	except:
		return valuelist
	valuelist = loadTSV(tsvfile)
	tsvfile.close()
	return valuelist

def crawl(dir):
	"""Recursively crawl through each directory
		@return list of pathnames to files."""
	filelist = []
	for file in [fn for fn in os.listdir(dir) if not fn.startswith("._")]:
		fullname = dir+os.sep+file
		if os.path.isdir(fullname):
			filelist += crawl(fullname)
		else:
			filelist.append(fullname)
	return filelist

def stat(filename):
	"""
	@return (bytecount, s_mtime, filename) on success
	@return None on fail
	"""
	try:
		sres = os.stat(filename)
	except:
		return None
	bytecount = sres.st_size
	mtime = datetime.fromtimestamp(sres.st_mtime)
	s_mtime = mtime.strftime("%Y-%m-%d %H:%M:%S")
	return (bytecount, s_mtime, filename)
