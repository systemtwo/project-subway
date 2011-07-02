#! /usr/bin/env python
#Dynamic IP -> UID Mapper for Project Subway
#Using logops
#Store in this format (IP, time) so that old entries (1-2wks) Can be removed

import socket
import time

def add_todo(iplist):
	"""Adds Ip/Date Tuple to database FOR SCANNING FOR IP"""
	f = open ("todoip.txt", "a")
	for i in iplist:
		f.write(i[0] + "," + i[1] + "\n")
	
def sanitize_todo():
	"""Clean up entries older than 2 weeks
	Will Also clean duplicates of entries"""

	#Get list from file
	f = open("todoip.txt", "r")
	biglist = []
	for line in f:
		minilist = line.split(",")
		biglist.append((minilist[0], minilist[1]))
	
	#Remove duplicates
	biglist.sort()
	last = biglist[-1]
	for i in range(len(biglist)-2, -1, -1):
		if last == biglist[i]:
			del biglist[i]
		else:
			last = biglist[i]
	
	#Remove entries older than 2 weeks
	curtime = time.time()
	twoweeksago = curtime - 1209600
	for i in range(len(biglist)):
		if int(biglist[i][1]) < twoweeksago:
			del biglist[i]
		

def do_todo():
	"""Gets a TODO list and maps their uids"""


