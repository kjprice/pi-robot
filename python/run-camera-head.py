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

from modules.camera_module import capture_camera_image, camera_setup, shutdown_camera
from modules.image_module import save_image
from modules.process_image_for_servo import get_face_quadrant_from_image, get_image_with_face_boxes
from modules.servo_module import Servo

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

def save_image_with_faces(img):
    img_with_faces = get_image_with_face_boxes(img)

    save_image(img_with_faces, 'test-face-image.jpg')

def move_servo_based_on_quadrant(quadrant):
    center_position = [0.45, 0.55]
    if quadrant == None:
        servo.reset()
        return
    if quadrant >= center_position[0] and quadrant <= center_position[1]:
        return
    
    if quadrant < center_position[0]:
        amount_to_move = center_position[0] - quadrant
        servo.move_left(amount_to_move)
    elif quadrant > center_position[1]:
        amount_to_move = center_position[0] - quadrant
        servo.move_right(amount_to_move)
    else:
        raise Exception('Unkown quadrant {}'.format(quadrant))

def call_and_get_time(function, args):
    time_start = time.time()
    response = function(*args)

    time_end = time.time()
    time_total = time_end - time_start

    return (response, time_total)

def get_stats_text(time_pass_for_calls):
    text = []
    for (time, _text) in time_pass_for_calls:
        time_str = np.round(time, 2)

        text.append('{} ({})'.format(time_str, _text))
    
    return ', '.join(text)

camera_setup(IS_TEST)
servo = Servo(IS_TEST)
while True:
    time_pass_for_calls = []
    img, total_time = call_and_get_time(capture_camera_image, (IS_TEST,))
    time_pass_for_calls.append((total_time, 'take picture'))

    quadrant, total_time = call_and_get_time(get_face_quadrant_from_image, (img,))
    time_pass_for_calls.append((total_time, 'process picture'))

    if IS_TEST:
        save_image_with_faces(img)

    _, total_time = call_and_get_time(move_servo_based_on_quadrant, (quadrant,))
    time_pass_for_calls.append((total_time, 'turn servo'))

    print('Took {} seconds to run'.format(
        get_stats_text(time_pass_for_calls)
    ))
    print('Currently at position {} with quadrant {}'.format(servo.current_position, quadrant))
    time.sleep(0.2)


atexit.register(shutdown_camera, servo.teardown)