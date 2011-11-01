import socketTest
import safeevalnew
import socket

def getFileFromSubway(hash):
	## First, look if the file is in the database
	flist = dbFileLookup(hash)
	if (flist is not None):
		## Get the newest file entry
		curr = None # To hold the nodeuid (dict) with best date
		curr = flist[0] # To hold something to compare with
		for i in range(len(flist)):
			if (i["date-modified"] > curr['date-modified']):
				curr = i
		## Get the file itself
		s = makeSocket(curr['host'])
		socketTest.recv_file(s, hash, curr['host'])

	else:
		## If it is not there, force db to update
		ipdb = open("ipdb", "r").read()
		ipdb = ipdb.split("\n")
		minidict = {}
		for i in ipdb:
			i.split(" ")
			s = makeSocket(i[0])
			socketTest.recv_db(s)
		## Try to get the file again
		## Look if the file is in the database
		flist = dbFileLookup(hash)
		if (flist is not None):
			## Get the newest file entry
			curr = None # To hold the nodeuid (dict) with best date
			curr = flist[0] # To hold something to compare with
			for i in range(len(flist)):
				if (i["date-modified"] > curr['date-modified']):
					curr = i
			## Get the file itself
			s = makeSocket(curr['host'])
			socketTest.recv_file(s, hash, curr['host'])
		else:
			## Everything has failed. There is no file in the network
	
def dbFileLookup(hash):
	db = open("db", "r").read()
	db = safeevalnew.safe_eval(db)
	if (db.has_key(hash)):
		return db[hash]
	else:
		return None

def makeSocket(uid):
	## Get IP of the host
	ipdb = open("ipdb", "r").read()
	ipdb = ipdb.split("\n")
	minidict = {}
	for i in ipdb:
		i.split(" ")
		minidict[i[0]] = i[1]
	
	if (minidict.has_key(uid)):
		nodeip = minidict[uid][1]


	## Make the socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((nodeip, 7000))
	return s
