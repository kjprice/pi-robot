from enum import Enum
import json
import os

import cv2
import socket


DATA_DIR = os.path.join('data')
TEST_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')
SAVE_IMAGE_DIR = os.path.join(DATA_DIR, 'images')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')
FIGURES_DIR = os.path.join(DATA_DIR, 'figures')

STATIC_DIR = os.path.join('web-app', 'build')

MODELS_DIR = os.path.join('..', 'models')

SOCKET_IO_SERVER_HOSTNAME = 'kj-macbook.lan'
SOCKET_IO_SERVER_PORT = 9898
SOCKET_IO_HOST_URI = 'http://{}:{}'.format(SOCKET_IO_SERVER_HOSTNAME, SOCKET_IO_SERVER_PORT)

SOCKET_ROOMS = ('image_processing_server', 'camera_head', 'browsers')

RESNET_MODEL_FILEPATH = os.path.join(MODELS_DIR, 'resnet50_coco_best_v2.1.0.h5')
class LOG_DIR_BASES(str, Enum):
    IMAGE_PROCESSING_TIME = 'image_processing_time'
    CAMERA_HEAD_SERVER = 'camera_head_server'
    IMAGE_PROCESSING_SERVER = 'image_processing_server'

class SERVER_NAMES(str, Enum):
    CAMERA_HEAD = 'camera_head'
    IMAGE_PROCESSING = 'image_processing_server'
    @classmethod
    def to_dict(cls):
        obj = {}
        for item in cls:
            obj[item.name] = item.value
        return obj

class CLASSIFICATION_MODELS(str, Enum):
    RESNET_COCO = 'resnet50_coco_best'
    FACES_ONLY = 'haarcascade_frontalface'

DEFAULT_CLASSIFICATION_MODEL = CLASSIFICATION_MODELS.FACES_ONLY

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

def get_figure_filepath(filename):
    return os.path.join(FIGURES_DIR, filename)

def save_plot(filename, plot):
    fig = plot.get_figure()
    filepath = get_figure_filepath(filename)
    fig.savefig(filepath)

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
ensure_directory_exists(LOGS_DIR)
ensure_directory_exists(FIGURES_DIR)

def setup_log_directories():
    for log_base_dir in LOG_DIR_BASES:
        directory_path = os.path.join(LOGS_DIR, log_base_dir.value)
        ensure_directory_exists(directory_path)
setup_log_directories()

def get_log_dir_by_server_name(server_name: SERVER_NAMES):
    if server_name == SERVER_NAMES.CAMERA_HEAD:
        return LOG_DIR_BASES.CAMERA_HEAD_SERVER
    if server_name == SERVER_NAMES.IMAGE_PROCESSING:
        return LOG_DIR_BASES.IMAGE_PROCESSING_SERVER
    
    raise ValueError('Unknown server_name: {}'.format(server_name))
        

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

def get_log_filepath(base_dir: LOG_DIR_BASES, file_name: str):
    return os.path.join(LOGS_DIR, base_dir.value, file_name)

def write_log_info(base_dir: LOG_DIR_BASES, file_name: str, text, mode='w'):
    filepath = get_log_filepath(base_dir, file_name)
    with open(filepath, mode) as f:
        f.write(text + '\n')

def append_log_info(base_dir: LOG_DIR_BASES, file_name: str, text: str):
    write_log_info(base_dir, file_name, text, mode='a')

def get_cache_info(file_name):
    cache_filepath = get_cache_filepath(file_name)
    if not os.path.isfile(cache_filepath):
        return None

    with open(cache_filepath, 'r') as f:
        return json.load(f)

def write_static_config(content_obj):
    filename = 'server_config.json'
    filepath = os.path.join(STATIC_DIR, filename)
    with open (filepath, 'w') as f:
        json.dump(content_obj, f)