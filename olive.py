#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File Hashes Calculator.

@author Miguel Maltez Jose
@created 20190215
@date    20190217
"""
import os
import time
import zlib
import hashlib
import logging

BLOCKSIZE = 2**16

class HashesCalculator: # pylint: disable=too-few-public-methods
	"""Iterator that incrementally calculates the hashes for a file."""
	def __init__(self, filename):
		self.file = open(filename, 'rb')
		self.bytecount = 0
		self.crc32 = 0
		self.md5 = hashlib.md5()
		self.sha1 = hashlib.sha1()
		self.calculated = 0 ##< time stamp of calculation end
	def __del__(self):
		self.file.close()
	def __iter__(self):
		return self
	def __next__(self):
		byteblock = self.file.read(BLOCKSIZE)
		if not byteblock:
			self.calculated = int(time.time())
			raise StopIteration
		self.bytecount += len(byteblock)
		self.crc32 = zlib.crc32(byteblock, self.crc32)
		self.md5.update(byteblock)
		self.sha1.update(byteblock)
		return self.bytecount
	def hashes(self):
		"""Returns a tuple of hashes.

		Bigger hashes are hexadecimal coded values in a string:
		- sha1
		- md5
		- crc32

		Returns:
			tuple: (sha1, md5, crc32, bytecount, calctimestamp)
		"""
		crc32 = self.crc32
		s_crc32 = "%08x" % (crc32 if crc32 >= 0 else 2**32 + crc32)
		s_md5 = self.md5.hexdigest()
		s_sha1 = self.sha1.hexdigest()
		return (s_sha1, s_md5, s_crc32, self.bytecount, self.calculated)

def printProgressBar(count, total, start, now
	, prefix="", suffix=""
	, fgchar="#", bgchar="-"
	): #pylint: disable-msg=too-many-arguments
	"""Prints progressbar corresponding to the state given in arguments."""
	completion = count / total if total != 0 else 0
	speed = count / (now - start)
	eta = (1 - total / count) * (start - now) if count != 0 else 0.0
	eta = eta if eta > 0.0 else 0.0
	progressbar = (fgchar*int(10*completion)).ljust(10, bgchar)
	print("\r%s[%s] %3.0f%% ETA %.1f s : %.3f MB/s%s" %
		(prefix, progressbar, 100*completion, eta, speed/2**20, suffix)
		, end="")
	return

def calculateHashesForFiles(filelist):
	"""Calculates hashes for a list of files."""
	results = {}
	try:
		sizelist = [os.path.getsize(fn) for fn in filelist]
		totalsize = sum(sizelist)
		sizeacc = 0
		absstart = time.time()
		for fi, filename in enumerate(filelist):
			lastshow = start = time.time()
			size = os.path.getsize(filename)
			print(filename)
			hashiter = HashesCalculator(filename)
			bytecount = 0
			for bc in hashiter:
				now = time.time()
				bytecount = bc
				if now - lastshow > 1/16:
					printProgressBar(bc, size, start, now)
					lastshow = now
			printProgressBar(bytecount, size, start, time.time())
			print()
			results[filename] = hashiter.hashes()

			sizeacc += hashiter.bytecount
			printProgressBar(sizeacc, totalsize, absstart, time.time()
				, prefix="\033[1mfile %d of %d: " % (fi+1, len(filelist))
				, suffix="\033[0m "
			)
			print()
		print("TOTAL TIME: %.3f" % (time.time() - absstart))
	except KeyboardInterrupt:
		print("\n\033[33mCalculated %d file hashes.\033[0m" % len(results))
	return results

def main():
	"""Called when module used as executable."""
	import argparse
	parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
	parser.add_argument("file"
		, nargs='*'
	)
	args = parser.parse_args()
	args.file = [fn for fn in args.file if os.path.isfile(fn)]

	hashes = calculateHashesForFiles(args.file)
	print(len(hashes))

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	main()
