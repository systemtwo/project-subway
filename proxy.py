from os import curdir, sep, path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urllib
import hashlib
import clientapi

#TODO
#Have a DO_NOT_CACHE list
#Have a DO_NOT_VISIT list (Blocked sites, NSFW things)




class BetterUrllib (urllib.URLopener):
	version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0"

class MyHandler(BaseHTTPRequestHandler):
    bytessaved = 0

    def do_GET(self):
	print threading.currentThread().getName()
	print self.path

	hasher = hashlib.sha256()
	hasher.update(self.path)
	fhash = hasher.hexdigest()

	
#	if (self.path.endswith(".jpg") or self.path.endswith(".png") or self.path.endswith(".gif") or self.path.endswith(".css") or self.path.endswith(".js")):
	if (1):
		try:
			## Try getting file locally
			f = open("cache/"+fhash, "r")
			d = f.read()
			f.close()
			#self.bytessaved += len(d)
		except IOError, e:
			## Try getting file from subway
			subfile = clientapi.getFileFromSubway(fhash)
			if (subfile == None):
				## Get the file thru the internet
				data = urllib.urlopen(self.path)
				d = data.read()
				f = open("cache/"+fhash, "w")
				f.write(d)
				f.close()
	else:
		data = urllib.urlopen(self.path)
		d = data.read()


	self.send_response(200)
	if (self.path.endswith(".css")):
		self.send_header('Content-type', 'text/css')
	else:
		self.send_header('Content-type',	'text/html')
	self.end_headers()
	self.wfile.write(d)
	#print "Bytes Saved:", self.bytessaved
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

