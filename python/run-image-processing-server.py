#!/usr/bin/python3

# TODO (here):
# - Process image
# - Send info to servo server

from base64 import b64decode
from flask import Flask, request
from flask_cors import CORS
from gzip import decompress
import multiprocessing
import os
import time

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.config import get_hostname
from modules.camera_module import image_bytes_to_array
from modules.image_processor import Image_Processor


app = Flask(__name__)
CORS(app)

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True
  
# Global variables
camera_hostname = None
camera_bin_dir = None
async_process = None

ALLOWED_HOSTNAMES = [
  'kj-macbook.lan', # KJ Macbook
  'pirobot',
]

## ROUTES ##
@app.route('/setCameraHostname', methods=['POST'])
def set_hostname_of_camera_server():
    data = request.get_json()
    hostname = data['hostname']
    bin_dir = data['bin_dir']

    if hostname not in ALLOWED_HOSTNAMES:
        return 'Unknown hostname {}'.format(hostname)
  
    startup(hostname, bin_dir)

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
            img = pull_image_from_camera_server()
            # TODO: Do something with the img
            image_processor.process_message_immediately(img, 0)

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

def get_shell_script_to_pull_zipped_image():
    base_script = 'sh {}/return_image.sh'.format(camera_bin_dir)
    if camera_hostname == get_hostname():
        return base_script
    
    return 'ssh {} "{}"'.format(camera_hostname, base_script)

def pull_image_from_camera_server():
    shell_script = get_shell_script_to_pull_zipped_image()
    shell_script = '{}'.format(shell_script) # Unzip output
    stream = os.popen(shell_script)
    output = stream.read()

    zipped_image_bytes = b64decode(output)
    image_bytes = decompress(zipped_image_bytes)

    image_array = image_bytes_to_array(image_bytes)

    return image_array

def startup(hostname_of_camera_server, bin_dir_of_camera_server):
    global camera_hostname, camera_bin_dir

    camera_hostname = hostname_of_camera_server
    camera_bin_dir = bin_dir_of_camera_server

    reset_async_process()