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

MODELS_DIR = os.path.join('models')

ACTIVE_PROCESSES_PATH = os.path.join(DATA_DIR, 'processes.json')

JSON_CONFIG_FILEPATH = 'config.json'

def get_hostname():
    return socket.gethostname()

# https://www.delftstack.com/howto/python/get-ip-address-python/#use-the-socket-getsockname-funtion-to-get-the-local-ip-address-in-python
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# TODO: Move to config.json
SOCKET_IO_SERVER_HOSTNAME = get_hostname()
SOCKET_IO_SERVER_PORT = 9898

SOCKET_IO_HOST_URI = 'http://{}:{}'.format(SOCKET_IO_SERVER_HOSTNAME, SOCKET_IO_SERVER_PORT)
SOCKET_IO_HOST_URI_LOCAL = 'http://{}:{}'.format(get_local_ip(), SOCKET_IO_SERVER_PORT)

# TODO: Move to config.json
SOCKET_ROOMS = ('image_processing_server', 'camera_head', 'browsers', 'raspi_poller', 'security_camera', 'security_camera_output')

RESNET_MODEL_FILEPATH = os.path.join(MODELS_DIR, 'resnet50_coco_best_v2.1.0.h5')

# TODO: Move to config
class LOG_DIR_BASES(str, Enum):
    IMAGE_PROCESSING_TIME = 'image_processing_time'
    CAMERA_HEAD_SERVER = 'camera_head_server'
    IMAGE_PROCESSING_SERVER = 'image_processing_server'
    RASPI_POLLER = 'raspi_poller'
    JOB_PROCESSER = 'job_processor'
    # TODO: There are two folders of logs - consolidate how we log
    SECURITY_CAMERA = 'security_camera'
    PYTHON_SIMPLE_SERVER = 'python_simple_server'

class SERVER_NAMES(str, Enum):
    CAMERA_HEAD = 'camera_head'
    IMAGE_PROCESSING = 'image_processing_server'
    RASPI_POLLER = 'raspi_poller'
    JOB_PROCESSER = 'job_processor'
    SECURITY_CAMERA = 'security_camera'
    PYTHON_SIMPLE_SERVER = 'python_simple_server'

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


def get_processing_server_urls():
    urls = []
    for hostname in POSSIBLE_PROCESSING_SERVER_HOSTNAMES:
        urls.append('http://{}:5000'.format(hostname))

    return urls
    
# if SERVO_ENV_KEY  in os.environ:
#     SERVER_HOST = os.environ[SERVO_ENV_KEY]
#     print('Found the servo hostname "{}" from the environment variable {}'.format(SERVER_HOST, SERVO_ENV_KEY))
# else:
#     print('No environment set for {}. You can set this environment variable to change the hostname (connecting to the servo server).'.format(SERVO_ENV_KEY))

def ensure_directory_exists(directory):
    try:
        return os.makedirs(directory)
    except:
        return None
ensure_directory_exists(SAVE_IMAGE_DIR)
ensure_directory_exists(CACHE_DIR)
ensure_directory_exists(LOGS_DIR)
ensure_directory_exists(FIGURES_DIR)
ensure_directory_exists(STATIC_DIR)


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
    if server_name == SERVER_NAMES.RASPI_POLLER:
        return LOG_DIR_BASES.RASPI_POLLER
    if server_name == SERVER_NAMES.JOB_PROCESSER:
        return LOG_DIR_BASES.JOB_PROCESSER
    if server_name == SERVER_NAMES.SECURITY_CAMERA:
        return LOG_DIR_BASES.SECURITY_CAMERA
    if server_name == SERVER_NAMES.PYTHON_SIMPLE_SERVER:
        return LOG_DIR_BASES.PYTHON_SIMPLE_SERVER
    
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

def load_json_config():
    with open(JSON_CONFIG_FILEPATH, 'r') as f:
        return json.load(f)

def get_port_by_name_from_config(port_name: str):
    config = load_json_config()
    ports = config['ports']
    return ports[port_name]

def get_port_by_process_name_from_config(port_name: str):
    config = load_json_config()
    ports = config['portsByProcess']
    return ports[port_name]
