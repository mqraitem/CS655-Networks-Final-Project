from __future__ import division, print_function
import os
from PIL import Image
import torch
from torchvision import transforms
import torchvision.models as models

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import request, Flask, render_template
import time

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



# web servers
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']

        # Save the file
        root = os.path.dirname(__file__)
        img_folder = os.path.join(root, 'images')
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)

        img_path = os.path.join(img_folder, secure_filename(f.filename))
        f.save(img_path)

        # Recognize the image
        reg_model = image_recognition()
        result = reg_model.make_prediction(img_path)
        return result
    return None


if __name__ == '__main__':
    http_server = WSGIServer(app)
    http_server.serve_forever()
