#!/usr/bin/python3

from __future__ import division, print_function
import time
import os
from PIL import Image
import torch
from torchvision import transforms
import torchvision.models as models

import cgi, os
import cgitb; cgitb.enable()
import socket


workers_info = open('workers.txt', 'r') 
workers_info = workers_info.readlines() 
workers_info = [line.strip().split(',') for line in workers_info]


def recvall(s):
  End = '\n'
  data = ''
  while True:
    msg = s.recv(1024).decode()
    data += msg
    if End == msg[-1:]:
      break
  return data


def check_available(resp_main): 
    msg = resp_main.strip('\n')
    if msg == '200 Busy': 
        return False
            
    if msg == '201 Free':
        return True 

form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid 
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    open('images/' + fn, 'wb').write(fileitem.file.read())
    connected_to_worker = False 

    while connected_to_worker == False:  
        for worker in workers_info: 
            ip, port = worker 

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = False 

            try: 
                s.connect((ip, int(port)))
                connection = True 
            except: 
                pass
            
            if connection: 
                msg_main = '100\n'
                s.sendall(msg_main.encode()) 
                resp_main = check_available(recvall(s))
                
                if resp_main:
                
                    imagepath = os.path.join('images', fileitem.filename)
                    image_to_send = open(imagepath, 'rb')    
                    image_to_send = image_to_send.read()
                    s.sendall(image_to_send)
                     
                    result = recvall(s) 
                    result = result.strip('\n')  
                    message = 'Model Prediction: %s'%(result) 
                    connected_to_worker = True 
                
                s.shutdown(socket.SHUT_RDWR) 

            if connected_to_worker: 
                break

else:
    message = 'No file was uploaded'
         
print ("""\
      Content-Type: text/html\n
      <html>
      <body>
        <img src="http://pcvm1-18.instageni.clemson.edu:8080/images/%s">
        <p>%s</p>
      </body>
      </html>
      """ % (fileitem.filename, message,))
