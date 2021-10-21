import cv2
import os

try:
    from modules.config import TEST_IMAGE_DIR, SAVE_IMAGE_DIR
except ModuleNotFoundError:
    from config import TEST_IMAGE_DIR, SAVE_IMAGE_DIR

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur_image(img):
    return cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)

# Only works with grayscale (one channel)
def increase_contrast(img):
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    return clahe.apply(img)

def is_image_grayscale(img):
    if len(img.shape) == 2:
        return True
    channels_count = img.shape[2]
    return channels_count == 1


def process_image(img):
    # TODO: Try bluring image
    if not is_image_grayscale(img):
        img = grayscale(img)
    # img = blur_image(img)
    # img = increase_contrast(img)
    return img
    # return cv2.normalize(grayscale_img)

def load_image(path, gray=True):
    img_arr = cv2.imread(path)
    if gray:
        return grayscale(img_arr)
    return img_arr

def load_test_image():
    test_image_path = os.path.join(TEST_IMAGE_DIR, 'image-raw.jpg')
    # test_image_path = os.path.join(TEST_IMAGE_DIR, 'barack-obama-and-donald-trump.jpg')
    # test_image_path = os.path.join(TEST_IMAGE_DIR, 'kj-face.png')

    return load_image(test_image_path)

# TODO: Write code to automatically create filename when "name" is None
def get_file_path_for_save(name = None):
    return os.path.join(SAVE_IMAGE_DIR, name)

def save_image(img, name = None):
    filepath = get_file_path_for_save(name)
    cv2.imwrite(filepath, img)