import flask
import json
import os
import shutil
import time
import requests
import threading

def create_app():
    app = flask.Flask(__name__)
    return app

app = create_app()

@app.before_first_request
def activate_job():
    def manage_buffer():
        while True:
            time.sleep(1)
            snaps = "snaps"
            dir = os.getcwd()

            image_list = get_image_names(os.path.join(dir, snaps))
            print(len(image_list))

            if len(image_list) == 8:
                for i in range(4):
                    file_path = os.path.join(dir, snaps, image_list[i])
                    print(file_path)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)

    thread = threading.Thread(target=manage_buffer)
    thread.start()

@app.route("/")
def main():
    return flask.render_template("index.html")

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == "__main__":
    start_runner()
    app.run()

counter = 0

@app.route("/upload", methods=["POST"])
def upload_photo():
    global counter
    counter += 1
    #print(flask.request.data)
    print(flask.request.files)
    file = flask.request.files['webcam']
    file.save("./snaps/" + "snap_{}.jpg".format(counter))
    return flask.make_response(json.dumps({"status": "ok"}))

def get_image_names(directory_):
    files = os.listdir(directory_)
    image_present = False
    images = []
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png'):
            images.append(file)
            image_present = True

    if not image_present:
        print("Could not find any Images!")
    return images
