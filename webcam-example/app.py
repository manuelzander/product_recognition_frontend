import flask
import flask_socketio
import threading
import queue
import json
import time
import numpy
import random
import tensorflow as tf
import io
import base64
import codecs
import collections
import numpy as np
import keras
import cv2
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

model_path = "/Users/manuelzander/Computer_Science/Ocado/group-project-front-end/webcam-example/intermediate.hdf5"
#print(model.summary())

model = keras.models.load_model(model_path)
model._make_predict_function()
graph = tf.get_default_graph()

def predict():
    if(len(array_buffer) < 4):
        return

    list_of_images = []
    for item in array_buffer:
        list_of_images.append(item)

    pictures = np.asarray(list_of_images)

    with graph.as_default():
        predictions = model.predict(pictures)#np.expand_dims(pictures[0,:,:,:],axis=0))

    #print(predictions.shape)
    #print(predictions)
    #print(np.argmax(np.sum(predictions[:,0:10],axis = 0)))
    indices = [1,4,6,9,10,13,14,15,16,17]
    predictions = np.sum(predictions[:,indices],axis = 0)
    predictions = predictions/sum(predictions)
    predictions = predictions.tolist()
    return predictions

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
    image = np.array(Image.open(image_bytes))
    #array = np.array(image)[:,:,0]
    #assert array.shape == (240, 320)
    #print(array)
    #print(array.shape)
    array = cv2.resize(image, (250, 250))
    array = (array / 255)
    #Append array to a circular buffer
    array_buffer.append(array)

    #Placeholder for prediction function
    '''
    if (len(array_buffer) >= 4):
        predictions = predict()
        input_q.put(predictions)
    '''
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
        time.sleep(0.2)
        '''
        random_list = np.round(np.random.rand(6), decimals=2)
        random_list = random_list.tolist()
        '''
        #predictions = input_q.get()
        if (len(array_buffer) >= 4):
            predictions = predict()
            print(predictions)
            socketio.emit('scan', json.dumps(predictions))

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

if __name__=="__main__":
    thread = threading.Thread(target=count_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=False)
