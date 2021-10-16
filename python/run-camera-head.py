#!/usr/bin/python3
import atexit
import multiprocessing
import os
import requests
from requests.exceptions import ConnectionError
import time

import flask
from flask import Flask
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()

from modules.camera_module import image_generator, camera_setup
from modules.config import ensure_directory_exists, get_bin_folder, get_hostname, get_processing_server_urls, get_servo_url, SAVE_IMAGE_DIR 
from modules.image_module import save_image
from modules.image_processor import Image_Processor
from modules.server_module import handle_default_server_response

# We do not need too many images - it is ok to throw away some
# TODO: Decide which images to throw away based on if they are more blurry than others
MAX_IMAGES_TO_PROCESS_PER_SECOND = 6
GET_IMAGE_ENDPOINT = '/getImage'
FOLDER_TO_SAVE_TO = 'images-captured'

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

PORT = os.environ['PORT']

servo_url = get_servo_url(IS_TEST)

def get_most_recent_saved_image_filepath():
    directory_path = os.path.join(SAVE_IMAGE_DIR, FOLDER_TO_SAVE_TO)
    file_objects = os.listdir(directory_path)
    file_objects_paths = [os.path.join(directory_path, filename) for filename in file_objects]
    file_paths = list(filter(os.path.isfile, file_objects_paths))
    file_paths.sort(key=lambda f: os.path.getmtime(f))
    oldest_sorted_filepaths = file_paths[::-1]
    return oldest_sorted_filepaths[0]

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
class CameraHead():
    FILENAMES_FOR_SAVING = ['A.jpg', 'B.jpg', 'C.jpg', 'D.jpg']
    index_of_last_filename_used = 0
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

        self.ensure_save_filepath_exists()

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
    
    def get_alternating_filename(self) -> str:
        current_index_for_filename = self.index_of_last_filename_used + 1
        if current_index_for_filename == len(self.FILENAMES_FOR_SAVING):
            current_index_for_filename = 0
        
        self.index_of_last_filename_used = current_index_for_filename

        return self.FILENAMES_FOR_SAVING[current_index_for_filename]
    
    def ensure_save_filepath_exists(self):
        ensure_directory_exists(os.path.join(SAVE_IMAGE_DIR, FOLDER_TO_SAVE_TO))

    def create_image_filepath(self, filename):
        return os.path.join(FOLDER_TO_SAVE_TO, filename)
    
    def alternate_save_image_for_later(self, img):
        filename = self.get_alternating_filename()
        save_image(img, self.create_image_filepath(filename))

    def run(self):
        camera_setup(IS_TEST, grayscale=True)

        time.sleep(1) # Give time for camera to warm up
        self.is_processing_server_online = check_if_processing_server_is_online()

        if not self.is_processing_server_online and not IS_TEST:
            test_connection_with_servo_server()

        images_count = 0
        for img, time_passed_for_image in image_generator(IS_TEST):
            if not self.should_keep_image():
                self.count_images_discarded += 1
                continue

            images_count += 1
            # TODO: Periodically check to make sure that server is still online (every 10 seconds)
            if self.is_processing_server_online:
                print('Found {} image(s) and dropped {} image(s)'.format(images_count, self.count_images_discarded), end='\r')
            else:
                self.image_processor.process_message_immediately(img, time_passed_for_image)

            # TODO: Decide whether to make greyscale before saving - compare time savings
            self.alternate_save_image_for_later(img)

async_process = None
camera_head = CameraHead()
async_process = multiprocessing.Process(target=camera_head.run, name="Process_Images")
async_process.start()

## ROUTES ##
@app.route(GET_IMAGE_ENDPOINT)
def get_image():
    oldest_image_path = get_most_recent_saved_image_filepath()
    with open(oldest_image_path, 'rb') as f:
        resp = flask.Response(f.read())
        resp.headers['Content-Type'] = 'image/jpg'
        return resp

print('Image endpoint available at: {}'.format(get_image_url()))