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
from time import sleep

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
array = [1,2,3]
array_buffer.append(array)
picture_buffer = None

counter = 0

@app.route("/send_from_webcam", methods=['POST'])
def send_to_server_webcam():
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
    print(array_buffer[-1])

    #file.save("./snaps/" + "snap_{}.jpg".format(counter))
    return flask.make_response(json.dumps({"status": "ok"}))

@app.route("/send_from_file", methods = ['POST'])
def send_to_server_file():

    file = flask.request.files['file']
    string = file.read()
    base64_data = codecs.encode(string, 'base64')
    image_bytes = io.BytesIO(base64.b64decode(base64_data))
    image = Image.open(image_bytes)
    array = np.array(image)[:,:,0]
    assert array.shape == (240, 320)

    #Put array to single picture buffer
    picture_buffer = array

    flask.make_response(json.dumps({"status": "ok"}))
    return flask.render_template("index.html")

@app.route('/stream')
def stream():
    def generate():
        while True:
            yield json.dumps(array_buffer[-1])
            sleep(1)

    return app.response_class(generate(), mimetype='text/event-stream')

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404
