#! /usr/bin/env python
#Log Operations for Project Subway (Getting IPs from logs and write all ops to log

import time

#def log_request(ip, time, file):
def log_request(ip, file):
	time = time.time()
	f = open ("log.txt", "a")
	time = str(time)
	logstr = ip + " " + str(int(time)) + " " + file + "\n"
	f.write (logstr)

def get_all_ips(logfile="log.txt", date="9999999999999999"):
	"""Gets Ips that are less than two weeks old in the log specified
	Must be in format: <IP> <date> <file>"""
	f = open (logfile, "r")
	biglist = []
	for line in f:
		minilist = line.split(" ")
		biglist.append((minilist[0], minilist[1]))
	print biglist


if __name__ == "__main__":
	import random
	f = open("testlog", "a")
	for i in range(50):
		ip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
		time = random.randint(0,9999999)
		file = random.randint(1000000,999999999)
		f.write(ip+" "+str(time)+" "+str(file)+"\n")
	f.close()
	print open("testlog").read()
	get_all_ips("testlog")
