import json
import os

import cv2
import socket


DATA_DIR = os.path.join('..', 'data')
TEST_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')
SAVE_IMAGE_DIR = os.path.join(DATA_DIR, 'images')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')

MODELS_DIR = os.path.join('..', 'models')

IMG_FACE_CLASSIFIER_FILENAMES = [
    'haarcascade_frontalface_default.xml',
    'haarcascade_frontalface_alt.xml',
    'haarcascade_frontalface_alt2.xml',
    'haarcascade_frontalface_alt_tree.xml'
]

CASCADE_XML_FILEPATH = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

SERVER_HOST = None

SERVO_ENV_KEY = 'SERVO_HOST'

POSSIBLE_PROCESSING_SERVER_HOSTNAMES = [
    'kj-macbook.lan' # KJ's Macbook
]

def get_hostname():
    return socket.gethostname()

def get_processing_server_urls():
    urls = []
    for hostname in POSSIBLE_PROCESSING_SERVER_HOSTNAMES:
        urls.append('http://{}:5000'.format(hostname))

    return urls
    
if SERVO_ENV_KEY  in os.environ:
    SERVER_HOST = os.environ[SERVO_ENV_KEY]
    print('Found the servo hostname "{}" from the environment variable {}'.format(SERVER_HOST, SERVO_ENV_KEY))
else:
    print('No environment set for {}. You can set this environment variable to change the hostname (connecting to the servo server).'.format(SERVO_ENV_KEY))

def ensure_directory_exists(directory):
    try:
        return os.makedirs(directory)
    except:
        return None
ensure_directory_exists(SAVE_IMAGE_DIR)
ensure_directory_exists(CACHE_DIR)

def get_classifier_path(filename):
    directory = cv2.data.haarcascades
    return os.path.join(directory, filename)

def get_face_classifier_filepaths():
    return list(map(get_classifier_path, IMG_FACE_CLASSIFIER_FILENAMES))

def get_face_classifiers():
    filepaths = get_face_classifier_filepaths()
    print('filepaths', len(filepaths))

    return list(map(cv2.CascadeClassifier, filepaths))

def get_servo_hostname(is_test):
    if 'SERVO_HOST' in os.environ:
        return os.environ['SERVO_HOST']
    
    if is_test:
        return 'localhost'
    
    return 'pi3misc' # Alternatively "pi3misc.local" could work for the hostname

def get_servo_url(is_test):
    return 'http://{}:5000'.format(get_servo_hostname(is_test))

def get_bin_folder():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    # Go up two directories
    dname_pieces = dname.split(os.path.sep)
    parent_directory_pieces = dname_pieces[:-2]
    dname_base = os.path.sep.join(parent_directory_pieces)

    bin_dir = os.path.join(dname_base, 'bin')
    return bin_dir

def get_cache_filepath(file_name):
    return os.path.join(CACHE_DIR, file_name)

def set_cache_info(file_name, cache_info):
    cache_filepath = get_cache_filepath(file_name)
    with open(cache_filepath, 'w') as f:
        json.dump(cache_info, f)

def get_cache_info(file_name):
    cache_filepath = get_cache_filepath(file_name)
    if not os.path.isfile(cache_filepath):
        return None

    with open(cache_filepath, 'r') as f:
        return json.load(f)
