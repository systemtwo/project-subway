#! /usr/bin/env python

import time
import safeevalnew

f = open ("db")
db = safeevalnew.safe_eval(f.read())

print "Project Subway DB Export"
print "Generated on: "
print time.strftime("%d %b %Y %H:%M:%S", time.localtime())
print ""
print ""
for i in db:
	print i
	for j in range(len(db[i])):
		print "Found on: \t", db[i][j]["host"]
		dm = time.gmtime(db[i][j]["date-modified"])
		print "Date:\t\t", db[i][j]["date-modified"], time.strftime("%d %b %Y %H:%M:%S", dm)
		print ""
