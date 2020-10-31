import os
import time

import cv2

from modules.image_module import save_image, get_file_path_for_save, load_image, grayscale

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

def pi_image_generator():
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

def webcam_image_generator():
    while True:
        yield (capture_picture_from_webcam(), 0)

def image_generator(is_test=False):
    if is_test:
        return webcam_image_generator()

    return pi_image_generator()

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
