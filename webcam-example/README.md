# group-project-front-end
### To run
Install relevant packages from the requirements.txt found in the root directory.

Run app.py and open http://127.0.0.1:5000/ (tested on Google Chrome).
Predictions will be started by clicking on "Start Predictions" in the navigation bar.

Note that the Python script loads the neural network model from the root directory,
which could not be uploaded due to size constraints on Cate.

### File structure
```
Project root (Contains this file)
------------------
webcam_example   >
                 static            >
                                webcam.js (files for WebcamJS library)
                                images
                 static            >
                 -------------------
                 templates         >
                                index.html (main file of webpage)
                                404.html (error page)
                 templates         >
                 -------------------
              app.py (main script for server)
webcam_example   >
--------------
```
