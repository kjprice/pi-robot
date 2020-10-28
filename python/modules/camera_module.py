import os
import time

import cv2

from modules.image_module import save_image, get_file_path_for_save, load_image, grascale

# This import will fail on a mac
try:
    from picamera import PiCamera
    import picamera.array
except ModuleNotFoundError:
    None

camera = None
def camera_setup(is_test=False, framerate=30, grayscale=False, resolution=(640, 480)):
    global camera
    if is_test:
        camera = cv2.VideoCapture(0)
    else:
        # Can be 1080p or 720p
        # camera = PiCamera(resolution='720p')
        camera = PiCamera()
        camera.resolution = resolution
        if grayscale:
            camera.color_effects = (128,128) # turn camera to black and white
        camera.framerate = framerate

    return camera

def image_generator():
    print('Warming up camera')
    camera.start_preview()
    time.sleep(0.5)
    with picamera.array.PiRGBArray(camera) as stream:
        # Using "array.PiRGBArray" the stream will have an "array" property
        for img_PiRGB in camera.capture_continuous(stream, 'rgb',
                                                use_video_port=True):
            start = time.time()
            img = img_PiRGB.array
            end = time.time()
            total_time = end-start
            yield img, total_time

            stream.seek(0)


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
