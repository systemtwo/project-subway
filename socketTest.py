#! /usr/bin/env python

import socket
import time
import sys
import hashlib
import safeevalnew

def create_socket():
	#time.sleep(2)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((socket.gethostname(), 7000))
	return s

def db_lookup(filename, uid):
	#See if the DB has the file
	print "Testing hash against DB to see if it is attached to this uid"
	dbf = open("db", "r")
	dbstr = dbf.read()
	dbf.close()
	db = safeevalnew.safe_eval(dbstr)
	#print db[filename]
	#print filename
	if (db[filename]["host"] == uid):
		print "Found entry in DB"
		return 1
	else:
		print "Not in db"
		return 0

def recv_uid(s):
	#Argument is socket
	#Recieve UID
	nodeuid = s.recv(UID_LENGTH)
	print "Connected to:", nodeuid 
	s.send("UID_GOT_IT")
	return nodeuid

def recv_db(s):
	#Recieve DB Size
	s.send("DB_REQ")
	print "Waiting for DB_SIZE..."
	dbsize = s.recv(1000)
	if (len(dbsize) == 0):
		print "No DB_SIZE recv"
	else:
		print "DB_SIZE int length", len(dbsize)
	print "DB_SIZE is", dbsize

	#Send DB Size conf
	print "Sending DB_GOT_SIZE"
	s.send("DB_GOT_SIZE")

	#Recieve DB
	print "Waiting for DB_DATA..."
	dbstr = s.recv(int(dbsize))
	print "DB Sync'd"
	#print "DB_DATA:", dbstr
	print "Turning DB_DATA to usable form..."
	db = safeevalnew.safe_eval(dbstr)
	db_sync(db)

def recv_file(s, fhash, nodeuid):
	#Get the Go ahead (Sockets don't want to work if it doesn't respond)
	reply = s.recv(8)
	if (reply != "GO_AHEAD"):
		return 0
	#Send Filename in hash as request
	#Lookup to see if the file is attached to this uid
	if (db_lookup(fhash, nodeuid)):
		print "Sending File Request..."
		s.send(fhash)


	#Recieve Size
	size = s.recv(1000000)
	if (len(size) == 0):
		print "ERROR: No Size Returned from server"

	#Send Responce
	s.send("GOT_SIZE")

	#Recv File
	i = s.recv(int(size))
	f.write(i)
	s.close()
	print "Done"

def db_cleanup(db):
	#Deletes any entries older than two weeks
	curtime = time.time()
	pass

def db_sync(newdb):
	print "Opening old DB (Reading)"
	tempdb = {}
	try:
		g = open ("db", "r")
		olddb = safeevalnew.safe_eval(g.read())
		g.close()
	except IOError:
		#File does not exist, so just dump all what you have in file
		g = open ("db", "w")
		g.write(str(db))
		g.close
		return 1
	print "Syncing old with recv'd DB"
	#Update where newdb's date-modified is newer
	inter = set(newdb.iterkeys()).intersection(set(olddb.iterkeys())) #Find common entries
	#print inter
	for i in inter:
		if (olddb[i]["host"] == newdb[i]["host"]):
			if (olddb[i]["date-modified"] < newdb[i]["date-modified"]):
				print "Updating Old entry"
				tempdb[i] = {"date-modified": newdb[i]["date-modified"], "host": newdb[i]["host"]}
			elif (olddb[i]["date-modified"] >= newdb[i]["date-modified"]):
				tempdb[i] = {"date-modified": olddb[i]["date-modified"], "host": newdb[i]["host"]}
	
	c = set(newdb).union(set(olddb))
	d = set(newdb).intersection(set(olddb))
	uninter = c-d
	#uninter = set(newdb.iterkeys()) - set(inter)
	#print uninter
	#print newdb
	for i in uninter:
		tempdb[i] = newdb[i]
		

#Variables
UID_LENGTH = 46

for i in range(1):
	try:
		fname = "dice.png"

		hasher = hashlib.sha256()
		hasher.update(fname)
		fhash = hasher.hexdigest()

		print "Requesting file:", fhash

		#Open file to write to
		f = open("image.png", "w")


		#Get Uid
		#Request UID
		s = create_socket()
		s.send("UID_REQ")
		nodeuid = recv_uid(s)
		print "Got UID from node"
		s.close()
		

		#Get DB
		s = create_socket()
		recv_db(s)
		print "Got DB"
		s.close()


		#Get File
		s = create_socket()
		s.send("FILE_REQ")
		recv_file(s, fhash, nodeuid)
		print "Got File"
		s.close()
		break

	except KeyboardInterrupt:
		sys.exit(0)
