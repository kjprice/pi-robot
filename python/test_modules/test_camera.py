import os

import cv2

from modules.image_module import save_image, get_file_path_for_save, load_image, save_image
from modules.process_image_for_servo import extend_image, get_faces
from picamera import PiCamera

camera = PiCamera()

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
