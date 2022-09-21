from flask import Flask, render_template, request
import os
import torch

import io
from PIL import Image
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join('static', 'pets_upload')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


YOLOmodel = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/yolov5x_pets/weights/best.pt', source='local')
YOLOmodel.conf = 0.4

register_heif_opener()


@app.route('/', methods=["GET", "POST"])
def main():

    if request.method == "POST":
        im_file = request.files["file"]

        filename = secure_filename(im_file.filename)

        if not im_file:
            return "File not uploaded", 404

        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))
        im.filename = filename

        detected = YOLOmodel(im, size=640)
        detected.save(save_dir=app.config["UPLOAD_FOLDER"])

        return render_template("main.html", display_detection=detected.files[0], fname=detected.files[0])

    else:

        upload_folder = os.path.join('static', 'pets_upload')
        if os.listdir(upload_folder):

            for file in os.listdir(upload_folder):

                file_path = os.path.join(upload_folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        return render_template("main.html")