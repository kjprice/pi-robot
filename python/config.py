import os

DATA_DIR = os.path.join('..', 'data')
TEST_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')
SAVE_IMAGE_DIR = os.path.join(DATA_DIR, 'images')

MODELS_DIR = os.path.join('..', 'models')
CASCADE_XML_FILEPATH = os.path.join(MODELS_DIR, 'haarcascade_frontalface_default.xml')

def ensure_directory_exists(directory):
    try:
        return os.makedirs(directory)
    except:
        return None

ensure_directory_exists(SAVE_IMAGE_DIR)
