#! /usr/bin/env python
#Log Operations for Project Subway (Getting IPs from logs and write all ops to log

def log_request(ip, time, file):
	f = open ("log.txt", "a")
	logstr = ip + " " + time + " " + file
	f.write (logstr)

def get_all_ips():
	f = open ("log.txt", "r")
	biglist = []
	for line in f:
		minilist = line.split(" ")
		biglist.append(minilist[0])
	print biglist


