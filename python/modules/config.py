import os

DATA_DIR = os.path.join('..', 'data')
TEST_IMAGE_DIR = os.path.join(DATA_DIR, 'test-images')
SAVE_IMAGE_DIR = os.path.join(DATA_DIR, 'images')

MODELS_DIR = os.path.join('..', 'models')
CASCADE_XML_FILEPATH = os.path.join(MODELS_DIR, 'haarcascade_frontalface_default.xml')

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

def get_servo_hostname(is_test):
    if 'SERVO_HOST' in os.environ:
        return os.environ['SERVO_HOST']
    
    if is_test:
        return 'localhost'
    
    return 'pi3misc' # Alternatively "pi3misc.local" could work for the hostname

ensure_directory_exists(SAVE_IMAGE_DIR)
def get_servo_url(is_test):
    return 'http://{}:5000'.format(get_servo_hostname(is_test))
