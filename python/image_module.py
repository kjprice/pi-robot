import cv2
import os

from config import TEST_IMAGE_DIR, SAVE_IMAGE_DIR

def load_image(path, gray=True):
    img_arr = cv2.imread(path)
    if gray:
        return cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    return img_arr

def load_test_image():
    test_image_path = os.path.join(TEST_IMAGE_DIR, 'barack-obama-and-donald-trump.jpg')

    return load_image(test_image_path)

def save_image(img, name = None):
    filepath = os.path.join(SAVE_IMAGE_DIR, name)
    cv2.imwrite(filepath, img)