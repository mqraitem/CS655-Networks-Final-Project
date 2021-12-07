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

worker_address = '127.0.0.1'
PORT = 8081 

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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((worker_address, PORT))
 
        while True: 
        
            msg_main = '100\n'
            s.sendall(msg_main.encode()) 
            resp_main = recvall(s) 
            
            if resp_main:
                print('Worker is free')
                break 
        
        imagepath = os.path.join('images', fileitem.filename)
        image_to_send = open(imagepath, 'rb')    
        image_to_send = image_to_send.read()
        s.sendall(image_to_send)
         
        result = recvall(s) 

    result = result.strip('\n')  
    message = 'Model Prediction: %s'%(result) 
                      
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
