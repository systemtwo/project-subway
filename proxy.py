from os import curdir, sep, path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urllib
import hashlib

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
	print threading.currentThread().getName()
	data = urllib.urlopen(self.path)
	d = data.read()

	hasher = hashlib.sha256()
	hasher.update(self.path)
	fhash = hasher.hexdigest()
	
	if (self.path.endswith(".jpg") or self.path.endswith(".png") or self.path.endswith(".gif") or self.path.endswith(".css") or self.path.endswith(".js")):
		f = open("cache/"+fhash, "w")
		f.write(d)
		f.close()
		f = open("cache/"+fhash, "r")
		d = f.read()
		f.close()

	self.send_response(200)
	if (self.path.endswith(".css")):
		self.send_header('Content-type', 'text/css')
	else:
		self.send_header('Content-type',	'text/html')
	self.end_headers()
	self.wfile.write(d)
	return

    def do_POST(self):
	if self.headers.has_key('content-length'):
		length = int(self.headers['content-length'])
		data = self.rfile.read(length)
		data = data.split('&')
	
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

