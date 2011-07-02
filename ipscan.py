#! /usr/bin/env python
#Dynamic IP -> UID Mapper for Project Subway
#Using logops
#Store in this format (IP, time) so that old entries (1-2wks) Can be removed

import socket
import time

UID_LENGTH = 46

def recv_uid(s):
	#Argument is socket
	#Recieve UID
	nodeuid = s.recv(UID_LENGTH)
	print "Connected to:", nodeuid
	s.send("UID_GOT_IT")
	return nodeuid


def get_list():
	f = open("todoip.txt", "r")
	biglist = []
	for line in f:
		minilist = line.split(",")
		biglist.append((minilist[0], minilist[1]))
	return biglist


def add_todo(iplist):
	"""Adds Ip/Date Tuple to database FOR SCANNING FOR UID"""
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
	dellist = [] #List of entries to delete
	print biglist, twoweeksago
	for i in range(len(biglist)):
		print biglist[i], i, "Out of", len(biglist)
		if int(biglist[i][1]) < twoweeksago:
			dellist.append(biglist[i])
	
	print dellist
	for i in dellist:
		biglist.remove(i)

def do_todo():
	"""Gets a TODO list and maps their uids"""
	iplist = []
	list = get_list()
	for i in range(len(list)):
		#Query all todo ips
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(list[i][0], 7000)
		s.send("UID_REQ")
		nodeuid = rec_uid(s)
		iplist.append((list[i], nodeuid))
	
	#Read file and remove duplicates that occur with new ips
	try:
		f = open ("ipdb.txt", "r")
		biglist = []
		for line in f:
			minilist = line.split(",")
			biglist.append((minilist[0], minilist[1]))
		combined = set.union(set(biglist), set(iplist))
		totallist = list(combined)
		f.close()
	except IOError:
		#Create File if it doesn't exist
		f = open ("ipdb.txt", "w")
		f.write("")
		f.close
	

	#Write to file
	f = open ("ipdb.txt", "a")
	for i in range(len(iplist)):
		str = totallist[i][0] + " " + totallist[i][1] + "\n"
		f.write(str)
	f.close()


def print_todo():
	f = open ("todoip.txt")
	print f.read()
	f.close()

