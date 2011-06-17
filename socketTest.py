#! /usr/bin/env python

import socket
import time
import sys
import hashlib

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
		print "Connected to:", s.recv(UID_LENGTH)

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
