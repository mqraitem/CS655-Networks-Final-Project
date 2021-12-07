import socket
import os
from _thread import *
import time 
import os

from PIL import Image
import torch
from torchvision import transforms
import torchvision.models as models
import sys 


if len(sys.argv) < 2: 
    print('Please Enter a port number')
    sys.exit()

PORT = int(sys.argv[1]) 
BUSY = False

class image_recognition:
    def __init__(self):
        self.model = models.squeezenet1_1(pretrained=True).eval()
        self.transform = transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
                ])
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip().split(',')[1] for s in f.readlines()]
        self.classes = categories

    def make_prediction(self, img_path):
        img = Image.open(img_path)
        input_tensor = self.transform(img)
        input_batch = input_tensor.unsqueeze(0)
        with torch.no_grad():
            start_time = time.time()
            output = self.model(input_batch)
            end_time = time.time()
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top1_prob, top1_catid = torch.topk(probabilities, 1)
        result = "Prediction:\"" + str(self.classes[top1_catid]) + " \";  Confidence: %.3f"% (top1_prob.item())\
                 + ", Response Time: %.3f s\n" % (end_time - start_time)
        return result

def recvall(s):
    End = '\n'
    data = ''
    while True:
        msg = s.recv(1024).decode()
        data += msg
        if End == msg[-1:]:
            break
    return data


def decode_msg_main(msg): 
    
    msg = msg.strip('\n')
    if msg == '100': 
        return True 
    else: 
        return False 


def threaded_client(connection): 
    global BUSY
    while True: 
        msg_main = recvall(connection)
        valid = decode_msg_main(msg_main) 
        if valid: 
            if BUSY: 
                busy_msg = '200 Busy\n'
                connection.sendall(str.encode(busy_msg)) 
            else: 
                BUSY = True
                free_msg = '201 Free\n'
                connection.sendall(str.encode(free_msg)) 
                
                img = connection.recv(40960000) 
                img_written = open('tmp.jpg', 'wb')
                img_written.write(img) 
                img_written.close() 
                print('Image Received')  

                reg_model = image_recognition()
                result = reg_model.make_prediction('tmp.jpg') 

                connection.sendall(str.encode(result))
                BUSY = False
        else: 
            invalid_msg = '404 Error'
            connection.sendall(str.encode(invalid_msg)) 
    
    connection.close() 

ServerSocket = socket.socket()
host = ''
port = PORT
ThreadCount = 0

ServerSocket.bind((host, port))

print('Waiting for a Connection..')
ServerSocket.listen(5)

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()
