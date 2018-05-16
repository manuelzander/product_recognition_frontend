import flask
import flask_socketio
import threading
import queue
import json
import time
import numpy
import random
import io
import base64
import codecs
import collections
import numpy as np
import tensorflow as tf
import keras
import cv2
from PIL import Image

#Flask initialization
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = flask_socketio.SocketIO(app, async_mode=None)

@app.route("/")
def index():
    return flask.render_template('index.html')

#Creating a circular buffer for pictures
array_buffer = collections.deque(maxlen=4)

#Creating a LIFO queue for predictions
input_q = queue.LifoQueue(maxsize=3)

#Load the model
model_path = "/Users/manuelzander/Computer_Science/Ocado/group-project-front-end/webcam-example/intermediate.hdf5"
model = keras.models.load_model(model_path)
model._make_predict_function()
graph = tf.get_default_graph()

#Upload function
@app.route("/send_from_webcam", methods=['POST'])
def send_to_server_webcam():
    #Convert image data into right format
    file = flask.request.files['webcam']
    string = file.read()
    base64_data = codecs.encode(string, 'base64')
    image_bytes = io.BytesIO(base64.b64decode(base64_data))
    image = np.array(Image.open(image_bytes))
    array = cv2.resize(image, (250, 250))
    array = (array / 255)

    #Append array to a circular buffer
    array_buffer.append(array)
    return flask.make_response(json.dumps({"Status": "OK"}))

#Make predictions thread
def predict():
    while True:
        if (len(array_buffer) >= 4):
            list_of_images = []
            for item in array_buffer:
                list_of_images.append(item)

            pictures = np.asarray(list_of_images)

            with graph.as_default():
                predictions = model.predict(pictures)

            #Selected products that we can purchase
            indices = [1,4,6,9,10,13,14,15,16,17]
            predictions = np.sum(predictions[:,indices],axis = 0)
            predictions = predictions/sum(predictions)
            predictions = predictions.tolist()
            input_q.put(predictions)

#Send predictions thread
def send_thread():
    while True:
        if (len(array_buffer) >= 4):
            predictions = input_q.get()
            socketio.emit('scan', json.dumps(predictions))

#Error-page
@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__=="__main__":
    thread = threading.Thread(target=send_thread)
    thread.daemon = True
    thread.start()

    thread2 = threading.Thread(target=predict)
    thread2.daemon = True
    thread2.start()

    socketio.run(app, debug=False)
