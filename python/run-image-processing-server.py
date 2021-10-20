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

CACHE_FILE_NAME = 'camera_server_info.json'

# Global variables
camera_hostname = None
camera_image_endpoint = None
async_process = None

ALLOWED_HOSTNAMES = [
  'pirobot',
  'kj-macbook.lan', # KJ Macbook
]

## ASYNC OPERATIONS ##
def continuously_find_and_process_images():
    image_processor = Image_Processor()
    images_count = 0
    image_hub = imagezmq.ImageHub(open_port='tcp://*:6666')

    while True:
        rpi_name, image = image_hub.recv_image()
        cv2.imshow(rpi_name, image) # 1 window for each RPi
        cv2.waitKey(1)
        images_count += 1

        if image is not None:
            image_processor.process_message_immediately(image, 0)
        image_hub.send_reply(b'OK')
continuously_find_and_process_images()
