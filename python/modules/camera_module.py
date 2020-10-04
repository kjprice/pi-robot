import os

import cv2

from modules.image_module import save_image, get_file_path_for_save, load_image, grascale

# This import will fail on a mac
try:
    from picamera import PiCamera
except ModuleNotFoundError:
    None

camera = None
def camera_setup(is_test):
    global camera
    if is_test:
        camera = cv2.VideoCapture(0)
    else:
        # Can be 1080p or 720p
        camera = PiCamera(resolution='720p')



def capture_picture_from_webcam():
    _, image = camera.read()
    return grascale(image)

def capture_pircture_from_pi_camera():
    img_filepath = get_file_path_for_save('pi-camera.jpg')
    camera.capture(img_filepath)

    return load_image(img_filepath)


def capture_camera_image(is_test=True):
    image = None
    if is_test:
        return capture_picture_from_webcam()
    
    return capture_pircture_from_pi_camera()

def shutdown_camera(is_test):
    print('shutting down')
    if camera is not None:
        camera.release()
