import flask
import flask_socketio
import threading
import queue
import json
import time
import numpy
import random
#import os
#import shutil
#import requests
#import threading
import io
import base64
import codecs
import collections
import numpy as np
from PIL import Image

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = flask_socketio.SocketIO(app, async_mode=None)

input_q = queue.Queue()

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/upload")
def show_page():
    return flask.render_template("upload.html")

#Creating a circular buffer
array_buffer = collections.deque(maxlen=4)
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
    #print(array_buffer[-1])
    input_q.put(array_buffer[-1])

    #Placeholder for prediction function
    #random_list = random.sample(range(10), 10)
    #input_q.put(random_list)

    #file.save("./snaps/" + "snap_{}.jpg".format(counter))
    return flask.make_response(json.dumps({"status": "ok"}))

@app.route("/send_from_file", methods = ['POST'])
def send_to_server_file():

    global picture_buffer

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

'''
@app.route("/send/<message>")
def send_msg(message):
    input_q.put(message)
    return flask.Response(status=200)
'''

def count_thread():
    i = 0
    while True:
        time.sleep(1)
        random_list = np.round(np.random.rand(6), decimals=2)
        #test = input_q.get()
        print(random_list)
        #column = test[:,1]
        #print(column)
        socketio.emit('scan', {"text": "{}".format(random_list)})

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__=="__main__":
    thread = threading.Thread(target=count_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
