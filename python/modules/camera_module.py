import os
import time

import cv2
import numpy as np

from modules.image_module import get_file_path_for_save, load_image, grayscale

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
        print('Warming up camera')
        camera.start_preview()
    return camera

def pi_image_generator(grayscale): # TODO: Make grayscale
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

def capture_picture_from_webcam(run_grayscale = False):
    _, image = camera.read()

    if run_grayscale:
        return grayscale(image)
    
    return image

def webcam_image_generator(grayscale=True):
    while True:
        yield (capture_picture_from_webcam(grayscale), 0)

# TODO: If processing takes longer than taking the picture, then the generator creates a queue of images to be processed
# TODO: Use VideoStream (as shown in https://github.com/jeffbass/imagezmq)
def image_generator(is_test=False, grayscale=True):
    if is_test:
        return webcam_image_generator(grayscale)

    return pi_image_generator(grayscale)

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

def image_bytes_to_array(image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1

    return img_np
