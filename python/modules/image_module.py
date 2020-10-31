import cv2
import os

try:
    from modules.config import TEST_IMAGE_DIR, SAVE_IMAGE_DIR
except ModuleNotFoundError:
    from config import TEST_IMAGE_DIR, SAVE_IMAGE_DIR

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def process_image(img):
    grayscale_img = grayscale(img)
    return grayscale_img
    # return cv2.normalize(grayscale_img)

def load_image(path, gray=True):
    img_arr = cv2.imread(path)
    if gray:
        return grayscale(img_arr)
    return img_arr

def load_test_image():
    test_image_path = os.path.join(TEST_IMAGE_DIR, 'barack-obama-and-donald-trump.jpg')
    # test_image_path = os.path.join(TEST_IMAGE_DIR, 'kj-face.png')

    return load_image(test_image_path)

def get_file_path_for_save(name = None):
    return os.path.join(SAVE_IMAGE_DIR, name)

def save_image(img, name = None):
    filepath = get_file_path_for_save(name)
    cv2.imwrite(filepath, img)