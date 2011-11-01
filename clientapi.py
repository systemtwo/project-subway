import socketTest
import safeevalnew
import socket

def getFileFromSubway(hash):
	## First, look if the file is in the database
	flist = dbFileLookup(hash)
	print flist
	if (flist is not None):
		## Get the newest file entry
		curr = None # To hold the nodeuid (dict) with best date
		curr = flist[0] # To hold something to compare with
		for i in range(len(flist)):
			if (i["date-modified"] > curr['date-modified']):
				curr = i
		## Get the file itself
		s = makeSocket(curr['host'])
		if (s == false):
			return none
		socketTest.recv_file(s, hash, curr['host'])

	else:
		return None
		## If it is not there, force db to update from first node in ipdb
		ipdb = open("ipdb", "r").read()
		ipdb = ipdb.split("\n")
		minidict = {}
		s = False
		for i in ipdb:
			j = i.split(" ")
			try:
				s = makeSocket(j[0])
				break
			except:
				print "No connection made"
			if (s is not False):
				socketTest.recv_db(s)
		if (s is False):
			## Could not connect to any node
			return None
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
			if (s == false):
				return none
			socketTest.recv_file(s, hash, curr['host'])
		else:
			## Everything has failed. There is no file in the network
			return None
	
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
		if (len(i) is not 0):
			j = i.split(" ")
			print j
			print j[0], j[1]
			minidict[j[0]] = j[1]
	
	if (minidict.has_key(uid)):
		nodeip = minidict[uid]
		print "Nodeip: ", nodeip
	else:
		return False


	## Make the socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (nodeip == "localhost"):
		s.connect((socket.gethostname(), 7000))
		return s
	s.connect((nodeip, 7000))
	return s
