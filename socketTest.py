#! /usr/bin/env python
# Safe Eval Script from Michael Spencer 

import socket
import time
import sys
import hashlib
import safeevalnew
import logops
import ipscan 

def ip_lookup():
	#Should be like [(IP, UID), (IP, UID)]
	f = open ("ipdb", "r")
	pass

def create_socket():
	#time.sleep(2)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (len(sys.argv) > 1):
		s.connect((sys.argv[1], 7000))
	else:
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
	print filename
	for i in range(len(db[filename])):
		if (db[filename][i]["host"] == uid):
			print "Found entry in DB"
			return 1
		#else:
			#if (i == len(db[filename])):
				#print db
				#print "Not in db"
				#return 0
	print "Not found!"

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
	data = s.recv(1024)
	while (len(data) < int(dbsize)):
		sdata = s.recv(1024)
		if (len(sdata) > 0):
			data = data + sdata
		else:
			s.close()
	dbstr = data
	print "DB Sync'd"
	#print "DB_DATA:", dbstr
	print "Turning DB_DATA to usable form..."
	db = safeevalnew.safe_eval(dbstr)
	db_sync(db)

def recv_file(s, fhash, nodeuid):
	#Get the Go ahead (Sockets don't want to work if it doesn't respond)
	reply = s.recv(8)
	if (reply != "GO_AHEAD"):
		print "Wrong Server Response"
		return 0
	#Send Filename in hash as request
	#Lookup to see if the file is attached to this uid
	if (db_lookup(fhash, nodeuid)):
		print "Sending File Request..."
		s.send(fhash)
	else:
		s.send("NEVER_MIND")
		return


	#Recieve Size
	size = s.recv(1000000)
	if (len(size) == 0):
		print "ERROR: No Size Returned from server"

	print "Size of file (bytes):", size

	#Send Responce
	s.send("GOT_SIZE")

	#Recv File
	#Testing bit
	#print len(s.recv(int(size)))
	#i = s.recv(int(size))
	data = s.recv(1024)
	while (len(data) < int(size)):
		sdata = s.recv(1024)
		if (len(sdata) > 0):
			data = data + sdata
		else:
			s.close()


	print "Saving file to clientcache/"
	f = open("clientcache/" + fhash, "wb")
	f.write(data)
	f.close()
	#Verify the size
	f = open ("clientcache/"+ fhash, "rb")
	print len(f.read())
	f.close()
	print "Done"

def db_cleanup(db):
	#Deletes any entries older than two weeks
	curtime = time.time()
	pass

def db_sync(newdb):
	print "Opening old DB (Reading)"
	tempdb = {}
	newdbhosts = []
	olddbhosts = []
	try:
		g = open ("db", "r")
		olddb = safeevalnew.safe_eval(g.read())
		g.close()
	except IOError:
		#File does not exist, so just dump all what you have in file
		g = open ("db", "w")
		g.write(str(newdb))
		g.close
		return 1
	print "Syncing old with recv'd DB"
	print newdb
	#Update where newdb's date-modified is newer
	inter = set(newdb.iterkeys()).intersection(set(olddb.iterkeys())) #Find common entries
	print inter

	#for i in inter:
		#if (olddb[i]["host"] == newdb[i]["host"]):
			#if (olddb[i]["date-modified"] < newdb[i]["date-modified"]):
				#print "Updating Old entry"
				#tempdb[i] = {"date-modified": newdb[i]["date-modified"], "host": newdb[i]["host"]}
			#elif (olddb[i]["date-modified"] >= newdb[i]["date-modified"]):
				#tempdb[i] = {"date-modified": olddb[i]["date-modified"], "host": newdb[i]["host"]}
	
	for i in inter:
		filehostsarray = [] #This is the array which the hosts for ONE file should be stored in
		tempdb[i] = []
		print "Working on", i
		print "Operating Data", len(olddb[i]), len(newdb[i])
		print olddb[i]
		print newdb
		for j in range(len(olddb[i])):
			print olddb[i][j]
			olddbhosts.append(olddb[i][j]["host"])
			for k in range(len(newdb[i])):
				newdbhosts.append(newdb[i][k]["host"])
				print "On Loop", i, j, k
				if (olddb[i][j]["host"] == newdb[i][k]["host"]):
					if (olddb[i][j]["date-modified"] < newdb[i][k]["date-modified"]):
						#if (olddb[i][j]["host"] == newdb[i][k]["host"]):
						print "Entry", i, "is newer in new"
						tempdb[i].append (newdb[i][k])
						print "Entry appended to index", j
						print tempdb
					elif (olddb[i][j]["date-modified"] >= newdb[i][k]["date-modified"]):
						#if (olddb[i][j]["host"] == newdb[i][k]["host"]):
						print "olddb is newer for entry", i
						print "Adding entry for host:", olddb[i][j]["host"]
						tempdb[i].append(olddb[i][j])
						print "Entry appended from index", j
						#print tempdb
						#print "!!!!!!!!!!!!!"
						#print "filehostsarray is currently"
						#print filehostsarray
						print "**********"
						#print tempdb[i]
						#print i,j
						#tempdb[i].append(olddb[i][j])
						#print tempdb[i]
					
		#Add in entries from other hosts for same file
		#Get rid of duplicates
		newdbhosts.sort()
		last = newdbhosts[-1]
		for t in range(len(newdbhosts)-2, -1, -1):
			if (last == newdbhosts[t]):
				del newdbhosts[t]
			else:
				last = newdbhosts[t]
		print newdbhosts

		olddbhosts.sort()
		last = olddbhosts[-1]
		for t in range(len(olddbhosts)-2, -1, -1):
			if (last == olddbhosts[t]):
				del olddbhosts[t]
			else:
				last = olddbhosts[t]
		print olddbhosts

		#Hosts to be added to the same file but different host (Within newdb)
		commonhosts = list (set (newdbhosts) & set (olddbhosts))
		uniquehosts = list (set(newdbhosts) - set (commonhosts))
		print "UniqueHosts", uniquehosts

		#Add entries listed in uniquehosts
		if (len(uniquehosts) > 0):
			for k in range(len(newdb[i])):
				for l in range(len(uniquehosts)):
					if (newdb[i][k]["host"] == uniquehosts[l]):
						print "Adding new entry for file", i
						tempdb[i].append (newdb[i][k])

		olduniquehosts = list (set(olddbhosts) - set (commonhosts))
		if (len (olduniquehosts) > 0):
			for k in range (len(olddb[i])):
				for l in range(len(olduniquehosts)):
					if (olddb[i][k]["host"] == olduniquehosts[l]):
						print "Copying old entry for file", i
						tempdb[i].append (olddb[i][k])

		print "\n\n=========="
		# Clean up the newdbhosts and olddbhosts arrays
		del olddbhosts[:]
		del newdbhosts[:]
					
	print tempdb
	
	#Add new file (not host) Entries
	#This implementation is BAD because it includes files from both DBs
		#c = set(newdb).union(set(olddb))
		#d = set(newdb).intersection(set(olddb))
		#uninter = c-d
	#uninter = set(newdb.iterkeys()) - set(inter)
	#print uninter
	#print newdb
		#for i in uninter:
			#tempdb[i] = newdb[i]
		

	#Add olddb entries NOT present in newdb
	c = set(newdb).intersection(set(olddb))
	d = set(olddb)
	oldunique = d-c

	print "Copying file entries (not hosts) not existant in tempdb to tempdb from olddb and newdb"

	for a in oldunique:
		print "Adding from olddb (oldunique)", a
		tempdb[a] = olddb[a]
	
	#Add newdb entries NOT present in olddb
	e = set (newdb)
	newunique = e-c

	for b in newunique:
		print "Adding from newdb (newunique)", b
		tempdb[b] = newdb[b]

	
	#Save newly constructed db
	g = open("db", "w")
	g.write(str(tempdb))
	g.close()
	print "Sync'd DB Saved"

def get_fileid(fname):
	if (fname == None):
		return
	hasher = hashlib.sha256()
	hasher.update(fname)
	fhash = hasher.hexdigest()
	return fhash




#Variables
UID_LENGTH = 46

def main():
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
		ipdb = open("ipdb", "a")
		ipdn.write(nodeuid + " " + sys.argv[1])
		

		#Get DB
		s = create_socket()
		recv_db(s)
		print "Got DB"
		s.close()


		#Get File
		s = create_socket()
		s.send("FILE_REQ")
		recv_file(s, fhash, nodeuid)
		#print "Got File"
		s.close()

	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == "__main__":
	main()
