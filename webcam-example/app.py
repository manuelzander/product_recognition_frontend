import flask
import json
import os
import shutil

def create_app():
    app = flask.Flask(__name__)
    return app

app = create_app()

@app.route("/")
def main():
    return flask.render_template("index.html")

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

def manage_buffer():
    while True:
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

manage_buffer()
