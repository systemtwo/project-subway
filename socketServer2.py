#! /usr/bin/env python

import socket
import os
import uuid

def client_thread(s):
	s.send("Hello")
	s.close()

def gen_conf():
	uid = str(uuid.uuid4())
	f = open("conf", "w")
	f.write(uid)
	f.close()

def build_db():
	db = {}
	dirlist =  os.listdir("cache/")
	for i in dirlist:
		item = os.stat("cache/" + i)
		#Should be {"Hash":{"date-modified":7128371293}, "Hash2":{"da...
		minidict = {"date-modified": item.st_mtime}
		db[str(i)] = minidict
	return db


#Get UUID Or Create
try:
	f = open("conf", "r")
except IOError:
	print "IO ERROR: Creating conf file"
	gen_conf()

#Variables
uid = open("conf", "r").read()
db  = build_db()
print db



print "Running with UUID:", uid

print socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 7000))
s.listen(5)

while 1:
	clientsocket, address = s.accept()
	print "Socket Accepted"
	clientsocket.send(uid)

	#Confirm uid
	if (clientsocket.recv(10) == "UID_GOT_IT"):
		print "Confirmed uid"
	else:
		print "UID NOT CONFIRMED"


	#Send DB Size
	dbstr = str(db)
	dblen = len(dbstr)
	print "Sending DB_SIZE...", dblen
	clientsocket.send(str(127))
	print "Sent"

	#Recv Confirm DB Size
	print "Waiting for DB_GOT_SIZE"

	if (clientsocket.recv(len("DB_GOT_SIZE")) == "DB_GOT_SIZE"):
		print "Client Correct Responce"
		clientsocket.send(dbstr)
	else:
		print "Client Wrong DB Response"
		clientsocket.close()


	fname = clientsocket.recv(4096) # Recieve Filename
	#fname = "cache/" + fname
	print fname

	#This chunk finds and appends a file extention (Macs) 
	try:
		print "Trying to open..."
		f = open(fname)
	except IOError:
		dirlist =  os.listdir("cache/")
		for i in dirlist:
			if (i.find(fname) > -1):
				#print "Found it!", i
				fname = "cache/" + i
				f = open(fname, "r")


	#Send File Size
	clientsocket.send(str(os.path.getsize(fname)))
	if (clientsocket.recv(8) == "GOT_SIZE"):
		#Correct Responce
		clientsocket.send(f.read())
		print "Sent!", address
		print "Done."
	clientsocket.close()

