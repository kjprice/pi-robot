#!/usr/bin/python3

import os
import time

import cv2
from flask import Flask
from flask_cors import CORS
import imagezmq

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.image_processor import Image_Processor


app = Flask(__name__)
CORS(app)

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

# If false, we will use pub/sub; the two patterns behave completely differently https://github.com/jeffbass/imagezmq/blob/48614483298b782b37dffdddd6b75b9ae0ee525c/docs/req-vs-pub.rst
REQ_REP = True

CACHE_FILE_NAME = 'camera_server_info.json'

# Global variables
camera_hostname = None
camera_image_endpoint = None
async_process = None

ALLOWED_HOSTNAMES = [
  'pirobot',
  'kj-macbook.lan', # KJ Macbook
]

def get_image_hub():
    print('REQ_REP', REQ_REP)
    if REQ_REP:
        # This listens to this machine's port
        return imagezmq.ImageHub(open_port='tcp://*:6666', REQ_REP=True)
    else:
        # This connects to another machine's port
        return imagezmq.ImageHub(open_port='tcp://pirobot:6666', REQ_REP=False)

## ASYNC OPERATIONS ##
def continuously_find_and_process_images():
    image_processor = Image_Processor()
    images_count = 0
    image_hub = get_image_hub()

    while True:
        time_start = time.time()
        time_to_pull = None
        rpi_name, image = image_hub.recv_image()
        time_end = time.time()
        time_to_pull = time_end - time_start
        cv2.imshow(rpi_name, image) # 1 window for each RPi
        cv2.waitKey(1)
        images_count += 1

        if image is not None:
            image_processor.process_message_immediately(image, time_to_pull)
        
        if REQ_REP:
            image_hub.send_reply(b'OK')

continuously_find_and_process_images()
