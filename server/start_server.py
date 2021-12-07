#!/usr/bin/python3
import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler
import socketserver

class ThreadingCGIServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

server = ThreadingCGIServer(('', 8080), CGIHTTPRequestHandler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print ("Finished")
