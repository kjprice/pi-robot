from functools import reduce
import unittest

import cv2
import numpy as np

try:
    from modules.image_module import is_image_grayscale, load_test_image
except ModuleNotFoundError:
    from image_module import is_image_grayscale, load_test_image


IS_TEST = False
if __name__ == '__main__':
    IS_TEST = True

DUTY_MIN = 2
DUTY_MAX = 12

def x_positions_in_image(img):
    img_width = float(img.shape[1])

    postions_less_than_1 = np.arange(0.1, 1.0, 0.1)

    x_positions = map(lambda a: int(a * img_width), postions_less_than_1)

    return x_positions

# TODO: IMPORTANT - we may want to run all of these in parallel and find the optimal face

# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def calculate_image_clarity(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()
    
def get_face_x_midpoint(face):
    x1, y1, width, height = face

    return x1 + (width // 2)

def get_face_face_position_x(img_width, face_box):
    face_x_midpoint = get_face_x_midpoint(face_box)

    # Will be between 0-1
    ratio_face_center_on_image = np.round(face_x_midpoint / img_width, 1)

    # Will return a number between -1 and 1
    return np.round(ratio_face_center_on_image * 2 - 1, 2)

def width(face):
    return face[2]

def get_widest_face(faces):
    return reduce(lambda a, b: a if width(a) > width(b) else b, faces)

    
def get_primary_face(faces):
    return get_widest_face(faces)

def get_face_position_x_from_image(img, faces):
    if faces is None or len(faces) == 0:
        return None

    primary_face = get_primary_face(faces)

    return get_face_face_position_x(img.shape[1], primary_face)

def draw_box(img, box, color=(0,0,255), line_width=1):
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x+w, y+h), color, line_width)

def get_image_with_face_boxes(img, faces):
    if is_image_grayscale(img):
        color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        color_image = img
    if faces is None or len(faces) == 0:
        return color_image

    for face in faces:
        draw_box(color_image, face)
    primary_face = get_primary_face(faces)

    draw_box(color_image, primary_face, color=(0,255,255))
    
    return color_image

def image_with_vertical_line(img, line_x):
    img_height = img.shape[0]
    start = (line_x, 0)
    end = (line_x, img_height)
    img = cv2.line(img, start, end, (255, 255, 255), 1)
    
    return img

def image_with_vertical_lines(img, line_x_list):
    for line_x in line_x_list:
        img = image_with_vertical_line(img, line_x)
    
    return img

def draw_primary_face_line(img, faces):
    if faces is None:
        return img

    primary_face = get_primary_face(faces)

    x, y, w, h = primary_face
    line_x = int(x + (w /2))

    return image_with_vertical_line(img, line_x)

def draw_opaque_rectange(img, box):
    x1, y1, width, height = box
    x2 = x1 + width
    y2 = y1 + height
    sub_img = img[y1:y2, x1:x2]

    # White box
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
    box_with_opaque_color = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

    img[y1:y2, x1:x2] = box_with_opaque_color

def draw_texts(img, texts):
    img_height = img.shape[0]
    middle_y = img_height // 2
    for i, text in enumerate(texts):
        y = middle_y + (i * 30)
        img = cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

# Can be used for debugging purposes
def extend_image(img, show_faces=False, show_vertical_lines=False, texts=None, faces=None):
    if show_faces:
        img = get_image_with_face_boxes(img, faces)
    if show_vertical_lines:
        img = draw_primary_face_line(img, faces)

    if texts is not None:
        img = draw_texts(img, texts)
    
    return img

def display_image(img):
    cv2.imshow('img', img)
    cv2.waitKey()

class TestProcessImages(unittest.TestCase):
    def setUp(self):
        self.test_image = load_test_image()
    def get_face_midpoint(self, x1, x2):
        width = x2 - x1
        return get_face_x_midpoint((x1, -1, width, -1))
    def test_get_face_midpoint(self):
        self.assertEqual(self.get_face_midpoint(40, 60), 50)
        self.assertEqual(self.get_face_midpoint(10, 20), 15)
        self.assertEqual(self.get_face_midpoint(0, 100), 50)
        self.assertEqual(self.get_face_midpoint(30, 50), 40)
    def test_get_face_face_position_xs(self):
        # return
        full_screen_face_position_x = get_face_face_position_x(100, (0, 0, 100, 100))
        self.assertEqual(full_screen_face_position_x, 0)
        mid_right_face_position_x = get_face_face_position_x(100, (50, 60, 0, 0))
        self.assertEqual(mid_right_face_position_x, 0)
        far_left_face_position_x = get_face_face_position_x(100, (10, 20, 30, 40))
        self.assertEqual(far_left_face_position_x, -0.6)
        large_far_left_quandrant = get_face_face_position_x(1000, (0, 50, 900, 900))
        self.assertEqual(large_far_left_quandrant, -0.2)
        far_right_face_position_x = get_face_face_position_x(100, (80, 10, 10, 20))
        self.assertEqual(far_right_face_position_x, 0.6)
    def test_integration_get_face_position_x_from_image(self):
        face_position_x = get_face_position_x_from_image(self.test_image)
        # Mike Pence is near the center, so this will be dead center
        self.assertEqual(face_position_x, -0.4)

def display_test_image():
    img = load_test_image()
    faces = find_person(img)
    texts = ['hello', 'world']
    img = extend_image(img, show_faces=True, show_vertical_lines=True, texts=texts, faces=faces)
    display_image(img)

if IS_TEST:
    # display_test_image()

    unittest.main()
