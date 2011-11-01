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


	## If it is not there, force db to update
	socketTest.recv_db(s)
	## If file is nonexistant, return none

	## If file is there, then query for the file


def dbFileLookup(hash):
	db = open("db", "r").read()
	db = safeevalnew.safe_eval(db)
	if (db.has_key(hash)):
		return db[hash]
	else:
		return None

def makeSocket(uid):
	## Get IP of the host
	##### INCOMPLETE #####

	## Make the socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, 7000))
	return s
