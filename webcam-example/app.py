import flask
import json
#import os
#import shutil
#import time
#import requests
#import threading
import io
import base64
import codecs
import collections
import numpy as np
from PIL import Image

def create_app():
    app = flask.Flask(__name__)
    return app

app = create_app()

@app.route("/")
def main():
    return flask.render_template("index.html")

@app.route("/upload")
def show_page():
    return flask.render_template("upload.html")

#Creating a circular buffer
array_buffer = collections.deque(maxlen=4)

counter = 0

@app.route("/send", methods=['POST'])
def send_to_server():
    global counter
    counter += 1
    #print(flask.request.data)
    #print(flask.request.files)

    file = flask.request.files['webcam']
    string = file.read()
    base64_data = codecs.encode(string, 'base64')
    image_bytes = io.BytesIO(base64.b64decode(base64_data))
    image = Image.open(image_bytes)
    array = np.array(image)[:,:,0]
    assert array.shape == (240, 320)

    #Append array to a circular buffer
    array_buffer.append(array)
    #print(array_buffer)

    #file.save("./snaps/" + "snap_{}.jpg".format(counter))
    return flask.make_response(json.dumps({"status": "ok"}))

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404
