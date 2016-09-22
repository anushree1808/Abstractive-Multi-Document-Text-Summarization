import time
import BaseHTTPServer
import os
from urlparse import urlparse,parse_qs
import json
HOST_NAME = 'localhost' 
PORT_NUMBER = 8080 

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to a GET request."""
        #TestSummarizer.html
        if urlparse(self.path).path == '/getsummary':
        	parsed_path = urlparse(self.path)
	       	query_components = parse_qs(parsed_path.query)
	       	if len(query_components.keys()) !=0 :
	       		print "algorithm is : ", query_components["algorithm"][0]	
	       	# input to os.system() is the python file. Give the right path	
	       	os.system('python summarizer.py ' + query_components["algorithm"][0])
	       	#input to open() in the path to the summary.json
	       	data = json.loads(open('modified_summary.json').read())
	       	#data={"name":"akshata"}
	       	jd = json.dumps(data)
	       	self.send_response(200)
	       	self.send_header("Content-type", "application/json")
	       	self.end_headers()
	       	self.wfile.write(jd)
	       	return 
       	#return
        else:
            #print self.path
            f = open("C:/Anaconda"+urlparse(self.path).path)
            #print "C:/Python27"+urlparse(self.path).path
            self.send_response(200)
            if urlparse(self.path).path.endswith(".html"):
                self.send_header("Content-type", "text/html")
            elif self.path.endswith(".js"):
                self.send_header("Content-type", "text/javascript")
            elif self.path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            elif self.path.endswith(".jpg"):
                self.send_header("Content-type", "image/jpeg")
                f = open("C:/Anaconda"+urlparse(self.path).path, 'rb')
            elif self.path.endswith(".jpeg"):
                self.send_header("Content-type", "image/jpeg")
                f = open("C:/Anaconda"+urlparse(self.path).path, 'rb')
            elif self.path.endswith(".png"):
                self.send_header("Content-type", "image/png")
                f = open("C:/Anaconda"+urlparse(self.path).path, 'rb')
            elif self.path.endswith(".gif"):
                self.send_header("Content-type", "image/gif")
                f = open("C:/Anaconda"+urlparse(self.path).path, 'rb')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)   