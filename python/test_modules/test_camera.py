import os
import time

import cv2
import numpy as np

from modules.camera_module import camera_setup, image_generator
from modules.image_module import save_image, get_file_path_for_save, load_image, save_image
from modules.process_image_for_servo import extend_image, get_faces

camera = camera_setup()


# TODO: store in ram (list)
# TODO: always pull the last image
# TODO: delete all other items
# TODO: Discover the best framerate
# TODO: Discover the best resolution

def test_fast_image_capture():
    # camera.resolution = (1024, 768)
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()

    seconds_to_run = 2
    count = 0

    for img in image_generator():
        save_image(img, 'pirgb-{}.jpg'.format(count))
        count += 1
        if time.time() - start > seconds_to_run:
            break
    finish = time.time()
    print()
    print('Captured %d frames at %.2ffps' % (
        count,
        count / (finish - start)))

def capture_pircture_from_pi_camera():
    img_filepath = get_file_path_for_save('pi-camera.jpg')
    camera.capture(img_filepath)

    return load_image(img_filepath)

def capture_camera_image(is_test=True):
    return capture_pircture_from_pi_camera()

def shutdown_camera(is_test):
    print('shutting down')
    if camera is not None:
        camera.release()

def save_test_image(img, n, duty):
    texts = ['duty: {}'.format(str(duty))]
    img = extend_image(img, show_vertical_lines=True, texts=texts)

    filename = 'test-{}.jpg'.format(str(n))
    save_image(img, filename)
