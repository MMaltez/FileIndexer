#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File Hashing Library contains basic object types used in file hash listing.

@author Miguel Maltez Jose
@date 20190217
"""
import os
from datetime import datetime
from collections import namedtuple

class FileMetadata(namedtuple("FileMetadata",
	["name", "path", "mod", "size"])):
	"""Container for file metadata information."""
	__slots__ = ()
	def __str__(self):
		formstr = "{}(name='{name}', path='{path}', mod='{modstr}'"
		formstr += ", size={size})"
		retstr = formstr.format(self.__class__.__name__
			, **self._asdict()
			, modstr=self.modstr()
		)
		return retstr
	def modstr(self):
		"""Returns modification date as a string in ISO 8601."""
		return str(datetime.fromtimestamp(self.mod))

class FileHashes(namedtuple("FileHashes",
	["sha1", "md5", "crc32", "bytecount", "calculated"])):
	"""File hashes container."""
	__slots__ = ()
	def __repr__(self):
		formstr = "{}(sha1='{sha1}', md5='{md5}', crc32='{crc32}'"
		formstr += ", bytecount={bytecount}"
		formstr += ", calculated={calculated})"
		retstr = formstr.format(self.__class__.__name__
			, **self._asdict()
		)
		return retstr

def getFileMetadata(filepathname):
	"""Returns file system metadata for file."""
	s = os.stat(filepathname)
	path, name = os.path.split(filepathname)
	return FileMetadata(name, path, int(s.st_mtime), s.st_size)

def joinPath(dirpath, filename):
	"""Join path and filename. Removes the local directory dot notation."""
	pathname = os.path.join(dirpath, filename)
	if pathname.startswith("."+os.sep):
		pathname = pathname[2:]
	return pathname

def getDirectoryListing(directory):
	"""Returns a dictionary with FileMetadata keyed by path+os.sep+filename
	of all the files currently in the specified directory and subdirectories
	in the file system.
	"""
	result = {}
	for dirpath, dirnames, filenames in os.walk(directory):
		for filename in filenames:
			pathfilename = joinPath(dirpath, filename)
			result[pathfilename] = getFileMetadata(pathfilename)
	return result
