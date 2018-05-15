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
#from keras import backend as K
import cv2
from PIL import Image

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = flask_socketio.SocketIO(app, async_mode=None)

@app.route("/")
def index():
    return flask.render_template('index.html')

#Creating a circular buffer for pictures
array_buffer = collections.deque(maxlen=4)
picture_buffer = None

#Creating a queue for predictions
input_q = queue.LifoQueue(maxsize=3)

#counter = 0
time_ = time.time()

model_path = "/Users/manuelzander/Computer_Science/Ocado/group-project-front-end/webcam-example/intermediate.hdf5"
#print(model.summary())
model = keras.models.load_model(model_path)
model._make_predict_function()
graph = tf.get_default_graph()

#K.set_learning_phase(0)

@app.route("/send_from_webcam", methods=['POST'])
def send_to_server_webcam():
    '''
    global counter
    counter += 1
    #print(flask.request.data)
    print(flask.request.files)
    file = flask.request.files['webcam']
    file.save("./snaps/" + "snap_{}.jpg".format(counter))
    '''
    global time_
    #Get picture and convert into right format for prediction
    #time_ = time.time()
    file = flask.request.files['webcam']
    string = file.read()
    base64_data = codecs.encode(string, 'base64')
    image_bytes = io.BytesIO(base64.b64decode(base64_data))
    image = np.array(Image.open(image_bytes))
    #array = np.array(image)[:,:,0]
    #assert array.shape == (240, 320)
    array = cv2.resize(image, (250, 250))
    array = (array / 255)

    #Append array to a circular buffer
    array_buffer.append(array)
    #print(time.time() - time_)
    #time_ = time.time()
    #print("----------------------------------------------")
    #print("--------------NEW PICTURES ADDED--------------")
    #print("----------------------------------------------")
    return flask.make_response(json.dumps({"Status": "OK"}))

'''
@app.route("/send/<message>")
def send_msg(message):
    input_q.put(message)
    return flask.Response(status=200)
'''

def predict():
    #global time_
    while True:
        if (len(array_buffer) >= 4):
            list_of_images = []
            for item in array_buffer:
                list_of_images.append(item)

            pictures = np.asarray(list_of_images)
            #time_ = time.time()
            with graph.as_default():
                predictions = model.predict(pictures)#np.expand_dims(pictures[0,:,:,:],axis=0))
            #print(time.time() - time_)
            indices = [1,4,6,9,10,13,14,15,16,17]
            predictions = np.sum(predictions[:,indices],axis = 0)
            predictions = predictions/sum(predictions)
            predictions = predictions.tolist()
            input_q.put(predictions)

def send_thread():
    while True:
        #time.sleep(0.2)
        '''
        random_list = np.round(np.random.rand(6), decimals=2)
        random_list = random_list.tolist()
        '''
        if (len(array_buffer) >= 4):
            predictions = input_q.get()
            #predictions = predict()
            socketio.emit('scan', json.dumps(predictions))

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
