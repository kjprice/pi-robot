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
from modules.image_module import save_image, grascale
from modules.process_image_for_servo import get_face_position_x_from_image, extend_image, get_faces
from modules.servo_module import Servo, calculate_duty_from_image_position

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

def save_image_with_faces(img, faces):
    print('img', img.shape)
    texts = ['']
    img_with_faces = extend_image(img, show_faces=True, show_vertical_lines=True, texts=texts, faces=faces)

    save_image(img_with_faces, 'test-face-image.jpg')

time_without_face = None
def set_time_with_out_face():
    global time_without_face
    time_without_face = time.time()

def reset_time_with_out_face():
    global time_without_face
    time_without_face = None

def has_too_much_time_passed_without_face():
    global time_without_face
    if time_without_face is None:
        set_time_with_out_face()
        return False

    new_time = time.time()
    time_diff = new_time - time_without_face

    if time_diff > 3:
        set_time_with_out_face()
        return True

    return False

def move_servo_based_on_face_position_x(face_position_x):
    center_position = [0.45, 0.55]
    # No face
    if face_position_x is None:
        if has_too_much_time_passed_without_face():
            servo.reset()
        return
    
    # if dead center, then stay there
    if face_position_x >= center_position[0] and face_position_x <= center_position[1]:
        return
    
    duty_change = calculate_duty_from_image_position(face_position_x)
    
    if face_position_x < center_position[0]:
        servo.move_left(duty_change)
    elif face_position_x > center_position[1]:
        servo.move_right(duty_change)
    else:
        raise Exception('Unkown face_position_x {}'.format(face_position_x))

    reset_time_with_out_face()

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

    faces, total_time = call_and_get_time(get_faces, (img,))
    time_pass_for_calls.append((total_time, 'get_faces'))

    face_position_x, total_time = call_and_get_time(get_face_position_x_from_image, (img, faces))
    time_pass_for_calls.append((total_time, 'process picture'))

    if IS_TEST:
        save_image_with_faces(img, faces)

    _, total_time = call_and_get_time(move_servo_based_on_face_position_x, (face_position_x,))
    time_pass_for_calls.append((total_time, 'turn servo'))

    print('Took {} seconds to run'.format(get_stats_text(time_pass_for_calls)))
    print('Currently at duty {} with face_position_x {}'.format(servo.current_duty, face_position_x))
    time.sleep(0.2)


atexit.register(shutdown_camera, servo.teardown)