#!/usr/bin/python3
import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler
import socketserver

#webdir = '.'   # where your html files and cgi-bin script directory live
#os.chdir(webdir)                                       # run in HTML root dir
#srvraddr = ("0.0.0.0", port)                                  # my hostname, portnumber
#srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
#srvrobj.serve_forever()                                # run as perpetual daemon

class ThreadingCGIServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

server = ThreadingCGIServer(('', 8080), CGIHTTPRequestHandler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print ("Finished")
