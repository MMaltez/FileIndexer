#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update directory listing.

@author Miguel Maltez Jose
@created 20190127
@date    20190211
"""
import os
import logging
from FHL import getDirectoryListing
from FileDatabase import FileDatabase
from olive import calculateHashesForFiles

def splitIntoNewDelModUnmod(clist, slist):
	"""Return [new, deleted, modified, unmodified] list of sets of filenames.

	Parameters
	----------
	clist: dict
		current file listing keyed by filepathname
	slist: dict
		stored file listing keyed by filepathname

	Returns
	-------
	list
		[new, deleted, modified, unmodified]
	"""
	currentset = set(clist)
	storedset = set(slist)
	new = currentset - storedset
	deleted = storedset - currentset
	modified = set()
	unmodified = set()
	for fn in currentset & storedset:
		if slist[fn].mod != clist[fn].mod \
		or slist[fn].size != clist[fn].size:
			modified.add(fn)
		else:
			unmodified.add(fn)
	return [new, deleted, modified, unmodified]

def main():
	"""Executed when script called directly."""
	import argparse
	parser = argparse.ArgumentParser(description="Update directory listing.")
	parser.add_argument("directory"
		, nargs='*'
		, help="name of directory"
	)
	args = parser.parse_args()

	for directory in args.directory:
		directory = directory.rstrip('/')
		if os.path.isdir(directory):
			print("# \033[34m%s\033[0m #" % directory)
			fdb = FileDatabase()
			fdbfilename = directory + ".fhl"
			if os.path.isfile(fdbfilename):
				fdb.loadFromTSV(fdbfilename)
			## current listing
			clist = getDirectoryListing(directory)
			logging.debug("current list : %d", len(clist))
			## stored listing
			slist = fdb.getDirectoryListing(directory)
			logging.debug("stored list  : %d", len(slist))

			new, deleted, modified, unmodified = splitIntoNewDelModUnmod(
				clist,
				slist)
			print("# %d new, %d deleted, %d modified" %
				(len(new), len(deleted), len(modified))
			)

			# update file database
			for fn in new:
				fdb.insertFileMetadata(fn, clist[fn])
			for fn in modified:
				fdb.updateFileMetadata(fn, clist[fn])
			for fn in deleted:
				fdb.deleteFileMetaData(fn)

			# calculate file hashes
			fhashes = calculateHashesForFiles(new | modified)
			# and update database
			insert_count = 0
			update_count = 0
			delete_count = 0
			for fn in new:
				if fn in fhashes:
					print(fhashes[fn])
					fdb.insertFileHashes(fn, fhashes[fn])
					logging.debug("\033[34;1m%s\033[0m", fn)
					for field, h in zip("sha1 md5 crc32 bc cts".split(), fhashes[fn]):
						logging.debug("\t%s\t%s", field, str(h))
					insert_count += 1
			for fn in modified:
				if fn in fhashes:
					print(fhashes[fn])
					fdb.updateFileHashes(fn, fhashes[fn])
					logging.debug("\033[1m%s\033[0m", fn)
					for field, h in zip("sha1 md5 crc32 bc cts".split(), fhashes[fn]):
						logging.debug("  %s\t%s", field, str(h))
					update_count += 1
			for fn in deleted:
				fdb.deleteFileHashes(fn)
				delete_count += 1
			logging.debug("hashes inserted %d", insert_count)
			logging.debug("hashes updated  %d", update_count)
			logging.debug("hashes deleted  %d", delete_count)
			fdb.saveToTSV(fdbfilename)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO
		, format="%(levelname)s: %(message)s"
	)
	main()
