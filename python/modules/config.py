import os

import cv2

DATA_DIR = os.path.join('..', 'data')
TEST_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')
SAVE_IMAGE_DIR = os.path.join(DATA_DIR, 'images')

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

ensure_directory_exists(SAVE_IMAGE_DIR)
def get_servo_url(is_test):
    return 'http://{}:5000'.format(get_servo_hostname(is_test))
