import flask
import json
import zlib

import time
app = flask.Flask(__name__)

# noinspection PyUnresolvedReferences
from picamera.array import PiRGBArray
# noinspection PyUnresolvedReferences
from picamera import PiCamera
robot_camera = PiCamera()
robot_camera.resolution = (320,320)
robot_RawCap = PiRGBArray(robot_camera)


@app.route('/')
def home():
    return "OK"

@app.route('/get_camera_array')
def cam():
    s = time.time()
    robot_camera.capture(robot_RawCap, format="bgr")
    arr = robot_RawCap.array
    robot_RawCap.truncate(0)
    return json.dumps(arr.tolist())

def startFlask():
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    startFlask()