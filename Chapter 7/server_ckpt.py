import torch.nn.functional as functional
import torchvision.transforms as transforms

from PIL import Image

from flask import Flask, request, jsonify

import image_classifier as ic

model = ic.ImageClassifier.load_from_checkpoint("./lightning_logs/version_0/checkpoints/epoch=99-step=3199.ckpt")

IMAGE_SIZE = 64
def transform_image(img):
    transform = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor()
    ])
    return transform(img).unsqueeze(0)

def get_prediction(img):
    result = model(img)
    return functional.softmax(result, dim=1)[:, 1].tolist()[0]

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    img_file = request.files['image']
    img = Image.open(img_file.stream)
    img = transform_image(img)
    prediction = get_prediction(img)
    if prediction >= 0.5:
        cat_or_dog = "dog"
    else:
        cat_or_dog = "cat"
    return jsonify({'cat_or_dog': cat_or_dog})
 
if __name__ == '__main__':
    app.run()