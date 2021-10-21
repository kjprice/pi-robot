#!/usr/bin/python3
import atexit
import multiprocessing
import os
import requests
from requests.exceptions import ConnectionError
import time

import imagezmq
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.camera_module import image_generator, camera_setup
from modules.config import get_bin_folder, get_hostname, get_servo_url
from modules.image_processor import Image_Processor
from modules.server_module import handle_default_server_response

# We do not need too many images - it is ok to throw away some
# TODO: Decide which images to throw away based on if they are more blurry than others
MAX_IMAGES_TO_PROCESS_PER_SECOND = 6
GET_IMAGE_ENDPOINT = '/getImage'
FOLDER_TO_SAVE_TO = 'images-captured'

# If false, we will use pub/sub; the two patterns behave completely differently https://github.com/jeffbass/imagezmq/blob/48614483298b782b37dffdddd6b75b9ae0ee525c/docs/req-vs-pub.rst
REQ_REP = True

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

PORT = os.environ['PORT']

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

def get_image_url():
    return 'http://{}:{}{}'.format(get_hostname(), PORT, GET_IMAGE_ENDPOINT)

def send_hostname_to_processing_server(processing_server_url):
    hostname = get_hostname()

    url_endpoint = '{}/setCameraHostname'.format(processing_server_url)

    response = requests.post(url_endpoint, json={
        "hostname": hostname,
        "bin_dir": get_bin_folder(),
        "img_url": get_image_url()
    })

    handle_default_server_response(response)

def check_if_processing_server_is_online():
    # TODO: We probably want to bring this logic back in the future
    return True
    # try:
    #     for url in get_processing_server_urls():
    #         print('Attempting to hit url: {}'.format(url))
    #         if test_connection_with_image_processing_server(url):
    #             print('Succesfully connected to processing server')

    #             send_hostname_to_processing_server(url)
    #             print('Successfully synced hostname with processing server')
    #             print()

    #             return True
    #     return False
    # except (ConnectionRefusedError, ConnectionError) as e:
    #     return False

def get_image_sender():
    if REQ_REP:
        return imagezmq.ImageSender(connect_to='tcp://kj-macbook.lan:6666', REQ_REP=True)
    else:
        return imagezmq.ImageSender(connect_to='tcp://*:6666', REQ_REP=False)

class CameraHead():
    is_processing_server_online = None
    image_processor = None
    count_images_discarded = None
    time_started = None

    def __init__(self) -> None:
        self.image_processor = Image_Processor()
        self.is_processing_server_online = False
        self.count_images_discarded = 0
        self.time_started = time.time()

    def run(self):
        camera_setup(IS_TEST, grayscale=True)

        time.sleep(1) # Give time for camera to warm up
        self.is_processing_server_online = check_if_processing_server_is_online()

        # if not self.is_processing_server_online and not IS_TEST:
        #     test_connection_with_servo_server()

        images_count = 0
        sender = get_image_sender()

        rpi_name = get_hostname() # send RPi hostname with each image

        for img, time_passed_for_image in image_generator(IS_TEST):
            time_start = time.time() - time_passed_for_image
            images_count += 1
            # TODO: Periodically check to make sure that server is still online (every 10 seconds)
            if self.is_processing_server_online:
                # TODO: Decide whether to make greyscale before saving - compare time savings
                sender.send_image(rpi_name, img)
                print('Found {} image(s) and dropped {} image(s)'.format(images_count, self.count_images_discarded), end='\r')
            else:
                self.image_processor.process_message_immediately(img, time_passed_for_image, time_start)

async_process = None
camera_head = CameraHead()
async_process = multiprocessing.Process(target=camera_head.run, name="Process_Images")
async_process.start()
