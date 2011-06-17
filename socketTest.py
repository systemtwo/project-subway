#! /usr/bin/env python

import socket
import time
import sys
import hashlib
import safeevalnew

#Variables
UID_LENGTH = 46

for i in range(1):
	try:
		fname = "dice.png"

		hasher = hashlib.sha1()
		hasher.update(fname)
		fhash = hasher.hexdigest()

		print "Requesting file:", fhash

		#Open file to write to
		f = open("image.png", "w")

		#time.sleep(2)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((socket.gethostname(), 7000))

		#Recieve UID
		nodeuid = s.recv(UID_LENGTH)
		print "Connected to:", nodeuid 
		s.send("UID_GOT_IT")

		#Recieve DB Size
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
		print "DB_DATA:", dbstr
		print "Turning DB_DATA to usable form..."
		db = safeevalnew.safe_eval(dbstr)
		print "Saving DB"
		g = open ("db", "w")
		g.write(dbstr)
		g.close()

		#Send Filename in hash as request
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
	except KeyboardInterrupt:
		sys.exit(0)
