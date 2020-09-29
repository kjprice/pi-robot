import os

import cv2

from image_module import save_image

# This import will fail on a mac
try:
    from picamera import PiCamera
except ModuleNotFoundError:
    None

camera = None
def camera_setup(is_test):
    global camera
    camera = cv2.VideoCapture(0)


def capture_picture_from_webcam():
    _, image = camera.read()
    return image

def capture_camera_image(is_test=True):
    image = None
    if is_test:
        return capture_picture_from_webcam()

def shutdown_camera(is_test):
    print('shutting down')
    if camera is not None:
        camera.release()
