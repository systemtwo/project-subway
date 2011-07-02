#! /usr/bin/env python
#Dynamic IP -> UID Mapper for Project Subway
#Using logops
#Store in this format (IP, time) so that old entries (1-2wks) Can be removed

import socket

def add_todo(iplist):
	"""Adds Ip/Date Tuple to database FOR SCANNING FOR IP"""
	f = open ("todoip.txt", "a")
	for i in iplist:
		f.write(i[0] + "," + i[1] + "\n")
	
def sanitize_todo():
	"""Clean up entries older than 2 weeks
	Will Also clean duplicates of entries"""
	f = open("todoip.txt", "r")
	for line in f:
		minilist = line.split(",")
		b

def do_todo():
	"""Gets a TODO list and maps their uids"""


