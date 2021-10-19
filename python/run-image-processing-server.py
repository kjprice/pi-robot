#!/usr/bin/python3

import multiprocessing
import os
import time

from flask import Flask, request
from flask_cors import CORS
import requests

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.config import get_cache_info, set_cache_info
from modules.camera_module import image_bytes_to_array
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

# This will try to set the last camer server used - speeds up starting up server
def set_default_camera_server():
    server_cache_info = get_cache_info(CACHE_FILE_NAME)
    print('server_cache_info', server_cache_info)
    if server_cache_info is None:
        return
    
    hostname = server_cache_info['hostname_of_camera_server']
    get_image_endpoint = None
    if 'camera_image_endpoint' in server_cache_info:
        get_image_endpoint = server_cache_info['camera_image_endpoint']
    startup(hostname, get_image_endpoint)

## ROUTES ##
@app.route('/setCameraHostname', methods=['POST'])
def set_hostname_of_camera_server():
    data = request.get_json()
    hostname = data['hostname']
    camera_image_endpoint = data['img_url']

    if hostname not in ALLOWED_HOSTNAMES:
        return 'Unknown hostname {}'.format(hostname)
  
    startup(hostname, camera_image_endpoint)

    return 'success'

@app.route('/testConnection')
def test_connection():
    return 'success'

## ASYNC OPERATIONS ##
def continuously_find_and_process_images():
    image_processor = Image_Processor()
    images_count = 0
    while True:
        images_count += 1
        if camera_hostname is not None:
            time_start = time.time()
            try:
                img = pull_image_from_camera_server()
            except requests.exceptions.ConnectionError:
                print('Could not pull image from server - connection refused - stopping now')
                return
            time_end = time.time()
            time_total = time_end - time_start
            if img is not None:
                image_processor.process_message_immediately(img, time_total)

def set_async_process():
    global async_process
    async_process = multiprocessing.Process(target=continuously_find_and_process_images, name="Process_Images")
    async_process.start()

def stop_async_process():
    global async_process
    if async_process is None:
        return
    
    async_process.terminate()
    async_process = None

def reset_async_process():
    stop_async_process()
    set_async_process()

# Now we pull the image over http
# TODO: Compress request
# TODO: Determine how long this takes to run
def pull_image_from_camera_server():
    global camera_image_endpoint
    if camera_image_endpoint is None:
        return
    response = requests.get(camera_image_endpoint, stream=True)

    if len(response.content) == 0:
        print('Response from camera server is empty - no image found')
        return None

    image_array = image_bytes_to_array(response.content)

    return image_array

def set_cache_server_info(hostname_of_camera_server, get_image_endpoint):
    set_cache_info(CACHE_FILE_NAME, {
        'hostname_of_camera_server': hostname_of_camera_server,
        'camera_image_endpoint': get_image_endpoint
    })


def startup(hostname_of_camera_server, get_image_endpoint):
    global camera_hostname, camera_image_endpoint
    set_cache_server_info(hostname_of_camera_server, get_image_endpoint)

    camera_hostname = hostname_of_camera_server
    camera_image_endpoint = get_image_endpoint

    reset_async_process()

set_default_camera_server()