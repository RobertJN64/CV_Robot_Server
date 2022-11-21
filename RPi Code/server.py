import flask
from flask import request
import threading
import base64
import json

from robot import Robot, FORWARD, STOP, REVERSE
robot = Robot()
threading.Thread(target=robot.update_loop).start()

class B_VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        self.cap.grab()
        ret, frame = self.cap.retrieve()
        return frame

app = flask.Flask(__name__)
import cv2
cam = B_VideoCapture(0)

@app.route('/')
def home():
    return "OK"

@app.route('/get_camera_array')
def get_camera_array():
    img = cam.read()
    img = cv2.resize(img, (320,320))
    return json.dumps(img.tolist())

@app.route('/get_camera_array_fast')
def get_camera_array_fast():
    img = cam.read()
    img = cv2.resize(img, (320,320))
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)


@app.route('/forward')
def forward():
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = FORWARD
    robot.r_motor_dir = FORWARD
    return "OK"

@app.route('/forward_gyro')
def forward_gyro():
    reset_imu()
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = FORWARD
    robot.r_motor_dir = FORWARD
    robot.gyro_correction_active = True
    return "OK"

@app.route('/backward')
def backward():
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = REVERSE
    robot.r_motor_dir = REVERSE
    return "OK"

@app.route('/left')
def left():
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = REVERSE
    robot.r_motor_dir = FORWARD
    return "OK"

@app.route('/left_angle')
def left_angle():
    reset_imu()
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = REVERSE
    robot.r_motor_dir = FORWARD
    robot.target_angle = -int(request.args.get("angle"))
    robot.l_turn_active = True
    return "OK"

@app.route('/right')
def right():
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = FORWARD
    robot.r_motor_dir = REVERSE
    return "OK"

@app.route('/right_angle')
def right_angle():
    reset_imu()
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = FORWARD
    robot.r_motor_dir = REVERSE
    robot.target_angle = int(request.args.get("angle"))
    robot.r_turn_active = True
    return "OK"

@app.route('/stop')
def stop():
    robot.gyro_correction_active = False
    robot.r_speed_mul = 1
    robot.l_speed_mul = 1
    robot.l_motor_dir = STOP
    robot.r_motor_dir = STOP
    return "OK"

@app.route('/done')
def done():
    if robot.l_turn_active or robot.r_turn_active:
        return "BUSY"
    else:
        return "OK"

@app.route('/speed')
def speed():
    robot.target_drive_speed = int(request.args.get('val'))
    return "OK"

@app.route('/reset')
def reset_imu():
    robot.pause_control_loop = True
    while not robot.pause_ack:
        pass
    robot.imu.gyrototal = 0
    robot.pause_control_loop = False
    return "OK"

@app.route('/calibrate')
def calibrate_imu():
    robot.pause_control_loop = True
    while not robot.pause_ack:
        pass
    robot.imu.calibrate()
    robot.pause_control_loop = False
    return "OK"

@app.route('/set_calib_factor')
def set_calib_factor():
    robot.set_calib_factor(float(request.args.get("v")))
    return "OK"

@app.route('/angle')
def angle():
    return """
    <!DOCTYPE html>
    <html lang="en">
    
    <head>
      <meta charset="UTF-8">
      <title>Angle</title>
      <script>
        function reload() { location.reload() }
        setTimeout(reload, 500);
      </script>
    </head>
    
    <body>
      <p>""" + str(robot.angle) + """</p>
    </body>
    </html>
    """

def startFlask():
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    startFlask()