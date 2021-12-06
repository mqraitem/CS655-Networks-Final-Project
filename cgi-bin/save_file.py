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
                 + ", Response Time: %.3f s" % (end_time - start_time)
        return result

form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid 
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    open('/tmp/' + fn, 'wb').write(fileitem.file.read())

    reg_model = image_recognition()
    result = reg_model.make_prediction(os.path.join('/tmp', fileitem.filename))
    
    message = 'Model Prediction: %s'%(result) 
    
                      
else:
    message = 'No file was uploaded'
         
print ("""\
      Content-Type: text/html\n
      <html>
      <body>
        <p>%s</p>
      </body>
      </html>
      """ % (message,))