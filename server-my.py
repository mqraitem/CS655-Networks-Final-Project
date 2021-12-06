#!/usr/bin/python3
import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler


webdir = '.'   # where your html files and cgi-bin script directory live
port   = 8080    # default http://localhost/, else use http://localhost:xxxx/

os.chdir(webdir)                                       # run in HTML root dir
srvraddr = ("", port)                                  # my hostname, portnumber
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # run as perpetual daemon
