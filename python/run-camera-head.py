#!/usr/bin/python3
import atexit
import os
import requests
from requests.exceptions import ConnectionError
import time

import numpy as np


# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.camera_module import image_generator, camera_setup, shutdown_camera
from modules.config import get_bin_folder, get_hostname, get_processing_server_urls, get_servo_url, get_bin_folder
from modules.image_module import save_image
from modules.image_processor import Image_Processor
from modules.server_module import handle_default_server_response

# We do not need too many images - it is ok to throw away some
# TODO: Decide which images to throw away based on if they are more blurry than others
MAX_IMAGES_TO_PROCESS_PER_SECOND = 20

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

servo_url = get_servo_url(IS_TEST)

def get_servo_url_path(path):
    global servo_url
    url = '/'.join([servo_url, path])

    return url

def test_connection_with_servo_server():
    url = get_servo_url_path('testConnection')
    print('Testing connection with servo server on url "{}"'.format(url))
    response = requests.get(url)
    handle_default_server_response(response)
    print('Successfully connected with servo server')

def test_connection_with_image_processing_server(url):
    response = requests.get('{}/testConnection'.format(url))
    text = response.text
    status_code = response.status_code
    if status_code == 200 and text == 'success':
        return True
    return False

def send_hostname_to_processing_server(processing_server_url):
    hostname = get_hostname()

    url_endpoint = '{}/setCameraHostname'.format(processing_server_url)

    response = requests.post(url_endpoint, json={
        "hostname": hostname,
        "bin_dir": get_bin_folder()
    })

    handle_default_server_response(response)

def check_if_processing_server_is_online():
    try:
        for url in get_processing_server_urls():
            print('Attempting to hit url: {}'.format(url))
            if test_connection_with_image_processing_server(url):
                print('Succesfully connected to processing server')

                send_hostname_to_processing_server(url)
                print('Successfully synced hostname with processing server')
                print()

                return True
        return False
    except (ConnectionRefusedError, ConnectionError) as e:
        return False

camera_setup(IS_TEST, grayscale=True)
if not IS_TEST:
    test_connection_with_servo_server()
time.sleep(1)

class CameraHead():
    is_processing_server_online = None
    image_processor = None
    minimum_time_in_seconds_between_images = None
    count_images_discarded = None
    time_started = None
    last_image_received_time = None

    def __init__(self) -> None:
        self.image_processor = Image_Processor()
        self.minimum_time_in_seconds_between_images = 1 / MAX_IMAGES_TO_PROCESS_PER_SECOND
        self.is_processing_server_online = False
        self.count_images_discarded = 0
        self.time_started = time.time()

    # TODO: This method should consider the quality of the image over other images - ie, drop if very blurry
    def should_keep_image(self):
        now = time.time()
        if self.last_image_received_time is None:
            self.last_image_received_time = now
            return True
        
        if now - self.last_image_received_time < self.minimum_time_in_seconds_between_images:
            return False
        
        self.last_image_received_time = now
        return True

    def run(self):
        self.is_processing_server_online = check_if_processing_server_is_online()

        images_count = 0
        for img, time_passed_for_image in image_generator(IS_TEST):
            if not self.should_keep_image():
                self.count_images_discarded += 1
                continue

            images_count += 1
            # TODO: Periodically check to make sure that server is still online (every 10 seconds)
            if self.is_processing_server_online:
                # TODO: Decide whether to make greyscale before saving - compare time savings
                print('Found {} image(s) and dropped {} image(s)'.format(images_count, self.count_images_discarded), end='\r')
                save_image(img, 'image-raw.jpg')
            else:
                self.image_processor.process_message_immediately(img, time_passed_for_image)


if __name__ == "__main__":
    camera_head = CameraHead()
    camera_head.run()

atexit.register(shutdown_camera)