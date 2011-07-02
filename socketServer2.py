#! /usr/bin/env python

#TODO
# Fix the DB so that it does not have the file extention

import socket
import os
import uuid
import time
import serverdbsync
import random
import logops

def client_thread(s):
	s.send("Hello")
	s.close()

def gen_conf():
	uid = str(uuid.uuid4())
	f = open("conf", "w")
	f.write(uid)
	f.close()

#def build_db(uid):
	#db = {}
	#minidb = {}
	#dirlist =  os.listdir("cache/")
	#for i in dirlist:
		#item = os.stat("cache/" + i)
		#Should be {"Hash":{"date-modified":7128371293}, "Hash2":{"da...
		#microdict = {"date-modified": item.st_mtime}
		#minidb[str(i)] = microdict
		#db[uid] = minidb
	#return db


def build_db(uid):
	#Should be {"hash":{date-modified:"jfsdklf",host:uid}}
	db = {}
	dirlist = os.listdir("cache")
	for i in dirlist:
		item = os.stat("cache/" + i)
		#minidb = [{"date-modified": item.st_mtime, "host": uid}, {"date-modified": 37383302, "host": "otherhost"}]
		#minidb = [{"date-modified": item.st_mtime, "host": uid}]
		minidb = [{"date-modified": item.st_mtime, "host": uid}, {"date-modified": random.randint(0,10000000), "host": "otherhost"}]
		db[str(i)] = minidb
	return db


def print_info(uid):
	print "Running on:\t\t", socket.gethostname(), "-", socket.gethostbyname(socket.gethostname())
	print "Running with UUID:\t", uid
	print time.strftime("%d %b %Y %H:%M:%S", time.gmtime(time.time())), "(Local time:", time.strftime("%d %b %Y %H:%M:%S", time.localtime()), ")"
	print "Note all further time values PRINTED will be in local time"

def send_uid(clientsocket):
	#Send this node's uid to client
	clientsocket.send(uid)

	#Confirm uid
	if (clientsocket.recv(10) == "UID_GOT_IT"):
		print "Confirmed uid"
	else:
		print "UID NOT CONFIRMED"

	clientsocket.close()
	print ""

def send_db(clientsocket, db):
	#Send DB Size
	dbstr = str(db)
	dblen = len(dbstr)
	print "Sending DB_SIZE...", dblen
	clientsocket.send(str(dblen))
	print "Sent"

	#Recv Confirm DB Size
	print "Waiting for DB_GOT_SIZE"

	if (clientsocket.recv(len("DB_GOT_SIZE")) == "DB_GOT_SIZE"):
		print "Client Correct Responce"
		clientsocket.send(dbstr)
	else:
		print "Client Wrong DB Response"
		clientsocket.close()

	clientsocket.close()
	print ""
	

def send_file(clientsocket, addr):
	clientsocket.send("GO_AHEAD")
	fname = clientsocket.recv(4096) # Recieve Filename

	#Log Request
	logops.log_request(addr[0], fname)

	if (fname == "NEVER_MIND"):
		print "Got NEVER_MIND\n"
		return
	#fname = "cache/" + fname
	print fname

	#This chunk finds and appends a file extention (Macs, sometimes if you touch the file)
	try:
		print "Trying to open..."
		f = open(fname, "rb")
	except IOError:
		dirlist =  os.listdir("cache/")
		for i in dirlist:
			if (i.find(fname) > -1):
				#print "Found it!", i
				fname = "cache/" + i
				f = open(fname, "rb")


	#Send File Size
	clientsocket.send(str(os.path.getsize(fname)))
	if (clientsocket.recv(8) == "GOT_SIZE"):
		#Correct Responce
		sentbytes = clientsocket.sendall(f.read())
		print "Sent!", address
		print sentbytes 
		f.seek(0,2)
		print "Total size:", f.tell()
		print "Done."
		print " " #Empty Line
	clientsocket.close()
	print ""





#Get UUID Or Create
try:
	f = open("conf", "r")
except IOError:
	print "IO ERROR: Creating conf file"
	gen_conf()

#Variables
uid = open("conf", "r").read()
db  = build_db(uid)
ip  = socket.gethostbyname(socket.gethostname())


print_info(uid)
#print socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 7000))
s.listen(5)

while 1:
	clientsocket, address = s.accept()
	print "Socket Accepted"
	print time.strftime("%d %b %Y %H:%M:%S", time.localtime())


	#Detect Requests
	req = clientsocket.recv(1000000)
	if (req == "UID_REQ"):
		#Log Request
		logops.log_request(address[0], "UID_REQ")

		print "Got Call for UID"
		send_uid(clientsocket)
	elif (req == "DB_REQ"):
		#Log Request
		logops.log_request(address[0], "DB_REQ")

		#Rebuild DB
		print "Rebuilding DB"
		db = build_db(uid)
		#Sync script has errors
		db = serverdbsync.db_sync(db)
		print "Got call for db"
		send_db(clientsocket, db)
	elif (req == "FILE_REQ"):
		#Log Request in function
		print "Got call for File"
		send_file(clientsocket, address)
	elif (req == "IPDB_REQ"):
		#Sync IP -> uid db
		pass




