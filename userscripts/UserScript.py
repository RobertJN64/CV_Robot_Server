from CV_Robot import robot
from CV_Robot import vision
from time import sleep
from printlog import printlog as print
vision.activate_camera()
robot.forward()
while True:
    img = vision.get_camera_image()
    objs = vision.find_objects(img)
    print(objs)
    if vision.Objects.STOP_SIGN in objs:
        break
     
robot.stop()