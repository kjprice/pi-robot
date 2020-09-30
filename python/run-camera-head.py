#!/usr/bin/python3
import atexit
import os
import time

import numpy as np


# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from camera_module import capture_camera_image, camera_setup, shutdown_camera
from image_module import save_image
from process_image_for_servo import get_face_quadrant_from_image, get_image_with_face_boxes
from servo_module import Servo

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

def save_image_with_faces(img):
    img_with_faces = get_image_with_face_boxes(img)

    save_image(img_with_faces, 'test-face-image.jpg')

def move_servo_based_on_quadrant(quadrant):
    if quadrant == 0:
        return
    if quadrant == None:
        servo.reset()
    elif quadrant < 0:
        servo.move_left()
    elif quadrant > 0:
        servo.move_right()
    else:
        raise Exception('Unkown quadrant {}'.format(quadrant))

camera_setup(IS_TEST)
servo = Servo(IS_TEST)
while True:
    time_start = time.time()
    img = capture_camera_image(IS_TEST)

    quadrant = get_face_quadrant_from_image(img)
    if IS_TEST:
        save_image_with_faces(img)
    
    move_servo_based_on_quadrant(quadrant)
    time_end = time.time()
    time_total = time_end - time_start
    print('Took {} seconds to run'.format(np.round(time_total, 2)))
    print('Currently at position {} with quadrant {}'.format(servo.current_position, quadrant))
    time.sleep(0.2)


atexit.register(shutdown_camera, servo.teardown)