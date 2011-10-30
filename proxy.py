#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
from os import curdir, sep, path
import os.path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
from SocketServer import ThreadingMixIn
import threading
#import pri

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
	print threading.currentThread().getName()
	data = urllib.urlopen(self.path)

	self.send_response(200)
	if (self.path.endswith(".css")):
		self.send_header('Content-type', 'text/css')
	else:
		self.send_header('Content-type',	'text/html')
	self.end_headers()
	self.wfile.write(data.read())
	return

    def do_POST(self):
	if self.headers.has_key('content-length'):
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		data = data.split('&')
		ndata = {}
		tdict = {}
		for i in data:
			a = i.split('=')
			tdict[a[0]] = a[1]

		if (os.path.isfile("data/"+tdict['title'])):
			#file Exists
			self.send_response(200)
			self.send_header('Content-type',	'text/html')
			self.end_headers()
			self.wfile.write("<html>Pick another title</html>")
			
		else:
			f = open("data/"+tdict['title'], "a")
			f.write(tdict['txt'])
			f.close()
			self.send_response(200)
			self.send_header('Content-type',	'text/html')
			self.end_headers()
			self.wfile.write("<html>Submitted</html>")
			print "Submitted Announcement", tdict['title']
		
		return
	
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests asynchronously"""


def main():
    try:
        server = ThreadedHTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

