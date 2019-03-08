#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""FileDatabase module.

@author Miguel Maltez Jose
@date 20190126
"""
import os
import logging
from datetime import datetime
from FHL import FileMetadata
from FHL import FileHashes

def lineToRecord(line):
	"""Convert tsv line to a tuple with key, info and hashes."""
	fields = line.split('\t')
	fields[3] = int(fields[3])
	fields[-2] = datetime.strptime(fields[-2]
		, "%Y-%m-%d %H:%M:%S").timestamp()
	key = fields[-1]
	hashes = FileHashes(*fields[0:4], None)
	path, name = os.path.split(key)
	info = FileMetadata(name, path, fields[-2], fields[-3])
	return (key, info, hashes)

def recordToLine(key, info, hashes):
	strtup = map(str, hashes[0:4] + (info.modstr(), key))
	return "\t".join(strtup)

class FileDatabase:
	"""A database with information about files in the file system.

	The database key is path+os.sep+filename.
	"""
	def __init__(self):
		## filemetadata table
		self.filemetadata = dict()
		## filehashes table
		self.filehashes = dict()
	def insertFileMetadata(self, fn, filemetadata):
		"""Inserts new filemetadata into database indexing with fn."""
		logging.debug("called %s -- '%s'"
			, self.insertFileMetadata.__name__, fn)
		self.filemetadata[fn] = filemetadata
	def updateFileMetadata(self, fn, filemetadata):
		"""Replace filemetadata indexed by fn."""
		logging.debug("called %s -- '%s'"
			, self.updateFileMetadata.__name__, fn)
		self.filemetadata[fn] = filemetadata
	def deleteFileMetaData(self, fn):
		"""Delete filemetadata indexed by fn."""
		logging.debug("called %s -- '%s'"
			, self.deleteFileMetaData.__name__, fn)
		del self.filemetadata[fn]
	def insertFileHashes(self, fn, filehashes):
		"""Inserts new filehashes into database indexing with fn."""
		logging.debug("called %s -- '%s'"
			, self.insertFileHashes.__name__, fn)
		self.filehashes[fn] = filehashes
	def updateFileHashes(self, fn, filehashes):
		"""Replace filehashes indexed by fn."""
		logging.debug("called %s -- '%s'"
			, self.updateFileHashes.__name__, fn)
		self.filehashes[fn] = filehashes
	def deleteFileHashes(self, fn):
		"""Delete filehashes indexed by fn."""
		logging.debug("called %s -- '%s'"
			, self.deleteFileHashes.__name__, fn)
		del self.filehashes[fn]
	def getDirectoryListing(self, directory):
		"""Returns a dictionary of FileMetadata keyed by path+os.sep+filename
		of all the files in the specified directory and subdirectories
		in the file listing database.
		"""
		return self.filemetadata
	def loadFromTSV(self, filename):
		"""Load database from tab separated values file."""
		logging.debug("Called %s('%s')."
			, self.loadFromTSV.__name__, filename)
		file = open(filename, 'r')
		for line in file:
			line = line.rstrip()
			if line and line[0] in "#;" or not line:
				continue
			record = lineToRecord(line)
			key = record[0]
			self.filemetadata[key] = record[1]
			self.filehashes[key] = record[2]
		file.close()
	def saveToTSV(self, filename):
		"""Save database into a tab separated values file."""
		logging.debug("Called %s('%s') implementation needs refinement."
			, self.saveToTSV.__name__, filename)
		file = open(filename, 'w')
		for fn in self.filemetadata:
			if fn in self.filehashes:
				info = self.filemetadata[fn]
				hashes = self.filehashes[fn]
				line = recordToLine(fn, info, hashes)
				file.write(line + os.linesep)
		file.close()

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	db = FileDatabase()
	db.loadFromTSV('sampledir.fhl')
	print(len(db.filemetadata))
	print(len(db.filehashes))
	db.saveToTSV('out.fhl')
