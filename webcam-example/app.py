import flask
import json

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
