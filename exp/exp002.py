#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List files in directory.

Experiment comparing os.walk with os.scandir

@author Miguel Maltez Jose
@date 20210314
"""
import os
import argparse
from dataclasses import dataclass
from abc import abstractmethod
from pprint import pprint

@dataclass
class FileInfo:
	"""File system information about a single file."""
	name: str
	path: str
	size: int
	mtime: int

def getFileInfo(path, name=None):
	if name is None:
		fullpath = path
		path, name = os.path.split(fullpath)
	else:
		fullpath = os.path.join(path, name)
	st = os.stat(fullpath)
	size = st.st_size
	mtime = int(st.st_mtime)
	return FileInfo(name, path, size, mtime)

exclude_files = {".DS_Store", }
def listdir1(directory, getFileInfo=getFileInfo):
	flst = []
	for dirpath, dirnames, filenames in os.walk(directory):
		for fn in filenames:
			if fn not in exclude_files:
				flst.append(getFileInfo(dirpath, fn))
	return flst

def listdir2(directory, pffun=print):
	"""List files under directory."""
	flst = []
	with os.scandir(directory) as it:
		for entry in it:
			if entry.is_file():
				path, _ = os.path.split(entry.path)
				size = entry.stat().st_size
				mtime = int(entry.stat().st_mtime)
				flst.append(FileInfo(entry.name, path, size, mtime))
			if entry.is_dir():
				flst += listdir2(entry.path)
	return flst

def main():
	"""Executed when module executed as script."""
	parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
	parser.add_argument("directory")
	args = parser.parse_args()
	#
	ans = listdir2(args.directory)
	pprint(ans)

if __name__ == "__main__":
	main()
