import socketTest
import clientapi
import sys
import socket

if (sys.argv[1] is not ""):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((sys.argv[1], 7000))
	except:
		exit()
	uid = socketTest.recv_uid(s)
	f = open("ipdb", "a")
	f.write(uid + " " + sys.argv[1])
	
