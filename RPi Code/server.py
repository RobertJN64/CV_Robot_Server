import flask
from flask import request
import json

app = flask.Flask(__name__)

# noinspection PyUnresolvedReferences
from picamera.array import PiRGBArray
# noinspection PyUnresolvedReferences
from picamera import PiCamera
robot_camera = PiCamera()
robot_camera.resolution = (320,320)
robot_RawCap = PiRGBArray(robot_camera)

# noinspection PyUnresolvedReferences
import explorerhat as eh
l_motor = eh.motor.one
r_motor = eh.motor.two

@app.route('/')
def home():
    return "OK"

@app.route('/get_camera_array')
def cam():
    robot_camera.capture(robot_RawCap, format="bgr")
    arr = robot_RawCap.array
    robot_RawCap.truncate(0)
    return json.dumps(arr.tolist())


FORWARD = 1
STOP = 0
REVERSE = -1

target_drive_speed = 75
l_motor_dir = STOP
r_motor_dir = STOP

def _update_motors():
    l_motor.speed(target_drive_speed * l_motor_dir)
    r_motor.speed(target_drive_speed * r_motor_dir)

@app.route('/forward')
def forward():
    global l_motor_dir, r_motor_dir
    l_motor_dir = FORWARD
    r_motor_dir = FORWARD
    _update_motors()
    return "OK"

@app.route('/backward')
def backward():
    global l_motor_dir, r_motor_dir
    l_motor_dir = REVERSE
    r_motor_dir = REVERSE
    _update_motors()
    return "OK"

@app.route('/left')
def left():
    global l_motor_dir, r_motor_dir
    l_motor_dir = REVERSE
    r_motor_dir = FORWARD
    _update_motors()
    return "OK"

@app.route('/right')
def right():
    global l_motor_dir, r_motor_dir
    l_motor_dir = FORWARD
    r_motor_dir = REVERSE
    _update_motors()
    return "OK"

@app.route('/stop')
def stop():
    global l_motor_dir, r_motor_dir
    print("Stopping robot...")
    l_motor_dir = STOP
    r_motor_dir = STOP
    _update_motors()
    return "OK"

@app.route('/speed')
def speed():
    global target_drive_speed
    target_drive_speed = int(request.args.get('val'))
    _update_motors()
    return "OK"

def startFlask():
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    startFlask()