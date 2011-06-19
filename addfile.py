#! /usr/bin/env python

import sys
import os
import hashlib
import shutil

if (len(sys.argv) = 2):
	path = sys.argv[1]
	filename = os.path.basename(path)
	hash = hashlib.sha256()
	hash.update(filename)
	hashhex = hash.hexdigest()

	shutil.copy2(path, "cache/" + hashhex)
	print "Added file", hashhex
else:
	print "Usage"
	print "addfile.py /full/path/to/file"


