#!/usr/bin/python3
import atexit
import os
import requests
import time

import numpy as np


# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.camera_module import image_generator, camera_setup, shutdown_camera
from modules.config import get_servo_url
from modules.image_module import save_image, process_image
from modules.process_image_for_servo import get_face_position_x_from_image, extend_image, find_person
from modules.servo_module import calculate_duty_from_image_position

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

servo_url = get_servo_url(IS_TEST)

def get_servo_url_path(path):
    global servo_url
    url = '/'.join([servo_url, path])

    return url

def handle_servo_server_response(response):
    text = response.text
    status_code = response.status_code
    if response.status_code != 200:
        raise Exception('Unkown status code "{}" with text "{}"'.format(status_code, text))
    if text != 'success':
        raise Exception('"success" not retrieved from server. Instead, received "{}"'.format(text))

def send_servo_duty(duty_change, direction):
    url = get_servo_url_path('setServoPosition')

    print('Sending request to "{}"'.format(url))

    response = requests.post(url, json={
        "duty": duty_change,
        "direction": direction
    })

    handle_servo_server_response(response)

def send_reset_servo():
    url = get_servo_url_path('resetServo')
    print('resetting servo')
    response = requests.post(url)
    handle_servo_server_response(response)

def test_connection_with_servo_server():
    url = get_servo_url_path('testConnection')
    print('Testing connection with servo server on url "{}"'.format(url))
    response = requests.get(url)
    handle_servo_server_response(response)
    print('Successfully connected with servo server')

def save_image_with_faces(img, faces, face_position_x):
    texts = [
        'Face Position: {}'.format(face_position_x)
    ]
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
            send_reset_servo()
        return
    
    # if dead center, then stay there
    if face_position_x >= center_position[0] and face_position_x <= center_position[1]:
        return
    
    duty_change = calculate_duty_from_image_position(face_position_x)
    
    if face_position_x < center_position[0]:
        send_servo_duty(duty_change, 'left')
    elif face_position_x > center_position[1]:
        send_servo_duty(duty_change, 'right')
    else:
        raise Exception('Unkown face_position_x {}'.format(face_position_x))

    reset_time_with_out_face()

def call_and_get_time(function, args):
    time_start = time.time()
    response = function(*args)

    time_end = time.time()
    time_total = time_end - time_start

    return (response, time_total)

MAX_ITEMS_FOR_TOTAL_TIMES = 10
def fps(times):
    total_time = np.sum(times)

    if total_time == 0:
        return 0

    _fps = len(times) / total_time

    return int(_fps)

def calculate_time_spent_average(total_times):
    if len(total_times) == 0:
        return -1
    
    avg = np.mean(total_times)
    return np.round(avg, 2)

def get_stats_text(time_pass_for_calls):
    text = []
    for (time, _text) in time_pass_for_calls:
        time_str = np.round(time, 2)

        text.append('{} ({})'.format(time_str, _text))
    
    return ', '.join(text)

camera_setup(IS_TEST, grayscale=True)
if not IS_TEST:
    test_connection_with_servo_server()
time.sleep(1)

class Camera_Head:
    time_pass_for_calls = []
    total_time_list_faces = []
    total_time_list_no_faces = []

    def limit_total_time_stored(self):
        if len(self.total_time_list_faces) > MAX_ITEMS_FOR_TOTAL_TIMES:
            del self.total_time_list_faces[0] # Delete oldest item
        if len(self.total_time_list_no_faces) > MAX_ITEMS_FOR_TOTAL_TIMES:
            del self.total_time_list_no_faces[0] # Delete oldest item

    def log_processing_time(self):
        mean_time_faces = calculate_time_spent_average(self.total_time_list_faces)
        mean_time_no_faces = calculate_time_spent_average(self.total_time_list_no_faces)

        fps_faces = fps(self.total_time_list_faces)

        sum_total_time_faces = np.round(np.sum(self.total_time_list_faces), 2)

        print('Takes {} seconds total (average  of {} seconds) to run {} images with faces ({} fps) and {} to run {} imags WITHOUT faces'.format(sum_total_time_faces, mean_time_faces, len(self.total_time_list_faces), fps_faces, mean_time_no_faces, len(self.total_time_list_no_faces)))

    def on_image_receive(self, img, time_passed_for_image):
        time_all_start = time.time()
        self.time_pass_for_calls.append((time_passed_for_image, 'take picture'))
        
        img, total_time = call_and_get_time(process_image, (img,))
        self.time_pass_for_calls.append((total_time, 'clean img'))

        faces, total_time = call_and_get_time(find_person, (img,))
        self.time_pass_for_calls.append((total_time, 'find_person'))

        # TODO: Clean image (make sharper perhaps) to better find faces
        # TODO: Try to find pedestrians as well
        face_position_x, total_time = call_and_get_time(get_face_position_x_from_image, (img, faces))
        self.time_pass_for_calls.append((total_time, 'process picture'))


        if not IS_TEST:
            _, total_time = call_and_get_time(move_servo_based_on_face_position_x, (face_position_x,))
            self.time_pass_for_calls.append((total_time, 'turn servo'))

        self.log_processing_time()

        save_image_with_faces(img, faces, face_position_x)
        time_all_end = time.time()
        time_all_total = (time_all_end - time_all_start)
        if faces is not None and len(faces) > 0:
            self.total_time_list_faces.append(time_all_total)
        else:
            self.total_time_list_no_faces.append(time_all_total)
        
        self.limit_total_time_stored()

if __name__ == "__main__":
    camera_head = Camera_Head()
    for img, time_passed_for_image in image_generator(IS_TEST):
        camera_head.on_image_receive(img, time_passed_for_image)    


atexit.register(shutdown_camera)