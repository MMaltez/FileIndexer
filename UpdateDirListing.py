#!/usr/bin/env python
"""Verifies listed hashes against files.
@author Miguel Maltez Jose
@date 20141119
"""
import os, sys
from digest import digestSHA1, digestCRC32, calculateFileDigests
from util import loadTSVFromFile, crawl, stat, tupleToTSV

def getMissingNewTouched(dirname):
	"""By reading directory fhl file it figures which files are new,
		or missing, or touched after listing was written.
		@return dict with all relevant lists.
	"""
	## listing file name
	listingfilename = dirname + ".fhl"
	dirfilelist = crawl(dirname)
	infolist = loadTSVFromFile(listingfilename)
	filelisting = [ info[-1] for info in infolist ]

	newfilelist = dirfilelist
	missingfilelist = []
	stillfilelist = []
	for filename in filelisting:
		if filename in dirfilelist:
			stillfilelist.append(filename)
			dirfilelist.remove(filename)
		else:
			missingfilelist.append(filename)

	# filter out touched files from the stills list
	try: listingmtime = os.path.getmtime(listingfilename)
	except: listingmtime = 0
	touchedfilelist = []
	for filename in stillfilelist:
		mtime = os.path.getmtime(filename)
		if mtime > listingmtime :
			touchedfilelist.append(filename)
			stillfilelist.remove(filename)

	retval = {}
	retval["missing"] = missingfilelist
	retval["new"]     = newfilelist
	retval["touched"] = touchedfilelist
	retval["still"]   = stillfilelist
	retval["oldinfo"] = infolist
	return retval

def getInfo(filename):
	st = stat(filename)
	dgst = calculateFileDigests(filename)
	return dgst[:4]+st[-2:]

def processLists(val):
	infolistdict = {}
	still = val["still"]
	missing = val["missing"]
	stillinfolist   = filter(lambda x: x[-1] in still, val["oldinfo"])
	missinginfolist = filter(lambda x: x[-1] in missing, val["oldinfo"])
	newinfolist     = [ getInfo(filename) for filename in val["new"] ]
	touchedinfolist = [ getInfo(filename) for filename in val["touched"] ]
	retval = {}
	retval["still"]   = stillinfolist
	retval["missing"] = missinginfolist
	retval["new"]     = newinfolist
	retval["touched"] = touchedinfolist
	return retval

def saveToTSV(filename, infolist):
	tsvfile = open(filename,'w')
	tsvfile.write("# File Hash List"+os.linesep)
	tsvfile.write("#sha1\tmd5\tcrc32\tbytecount\tmtime\tpathname"+os.linesep)
	for info in infolist:
		tsvfile.write(tupleToTSV(info)+"\n")
	tsvfile.close()

def main():
	import argparse
	desc = """Update list by removing missing files, adding new files, and
	 updating hashes of files younger than listing.
	"""
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument("DIR", nargs='*', help="directory name")
	args = parser.parse_args()

	for dirname in args.DIR:
		if os.path.isdir(dirname) :
			dirname = dirname.rstrip(os.sep)
			dirlistfilename = dirname+".fhl"
			ans = getMissingNewTouched(dirname)
			print("# %s" % dirname)
			print("#\t%d new, %d touched, %d missing" %
				(len(ans["new"]), len(ans["touched"]), len(ans["missing"]))
			)
			info = processLists(ans)
			del info["missing"]
			infolist = []
			for key in info:
				infolist.extend(info[key])
			saveToTSV(dirname+".fhl",infolist)

if "__main__" == __name__:
	main()
