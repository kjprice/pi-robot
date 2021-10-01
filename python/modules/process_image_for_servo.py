from functools import reduce
import unittest

import cv2
import numpy as np

try:
    from modules.image_module import load_test_image
    from modules.config import get_face_classifiers
except ModuleNotFoundError:
    from image_module import load_test_image
    from config import get_face_classifiers


# TODO: Add all of the models
face_cascades = get_face_classifiers()

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

def find_faces_in_any_classifier(img):
    for classifier in face_cascades:
        faces = classifier.detectMultiScale(img, 1.1, 4)
        if len(faces) > 0:
            return faces
    
    return None
        
    
def get_faces(img):
    faces = find_faces_in_any_classifier(img)
    return faces

def find_person(img):
    faces = get_faces(img)
    if faces is not None and len(faces) > 0:
        return faces
    
    return None

def get_face_x_midpoint(face):
    x1, y1, width, height = face

    return x1 + (width // 2)

def get_face_face_position_x(img_width, face_box):
    face_x_midpoint = get_face_x_midpoint(face_box)
    return np.round(face_x_midpoint / img_width, 1)

def width(face):
    return face[2]

def get_widest_face(faces):
    return reduce(lambda a, b: a if width(a) > width(b) else b, faces)

    
def get_primary_face(faces):
    return get_widest_face(faces)

def get_face_position_x_from_image(img, faces=None):
    if faces is None:
        faces = find_person(img)
    if faces is None or len(faces) == 0:
        return None

    primary_face = get_primary_face(faces)

    return get_face_face_position_x(img.shape[1], primary_face)

def draw_box(img, box, color=(0,0,255), line_width=1):
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x+w, y+h), color, line_width)

def get_image_with_face_boxes(img, faces):
    color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if faces is None or len(faces) == 0:
        return color_image

    for face in faces:
        draw_box(color_image, face)
    primary_face = get_primary_face(faces)

    draw_box(color_image, primary_face, color=(0,255,255))
    
    return color_image

def image_with_vertical_lines(img, line_x_list):
    img_height = img.shape[0]
    for line_x in line_x_list:
        start = (line_x, 0)
        end = (line_x, img_height)
        img = cv2.line(img, start, end, (255, 255, 255), 1)
    
    return img

def draw_opaque_rectange(img, box):
    x1, y1, width, height = box
    x2 = x1 + width
    y2 = y1 + height
    sub_img = img[y1:y2, x1:x2]

    # White box
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
    box_with_opaque_color = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

    img[y1:y2, x1:x2] = box_with_opaque_color

# expects x_ratio_start to be between 0-1
def box_of_selected_area(img, x_ratio_start):
    if x_ratio_start is None:
        return img
    start_region = x_ratio_start - 0.05

    x = int(start_region * img.shape[1])
    y = 0
    height = img.shape[0]
    width = int(0.1 * img.shape[1])
    box = (x, y, width, height)

    # mutates the object
    draw_opaque_rectange(img, box)

    return img


def draw_texts(img, texts):
    img_height = img.shape[0]
    middle_y = img_height // 2
    for i, text in enumerate(texts):
        y = middle_y + (i * 30)
        img = cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

# Can be used for debugging purposes
def extend_image(img, show_faces=False, show_vertical_lines=False, texts=None, faces=None):
    if faces is None:
        faces = find_person(img)
    if show_faces:
        img = get_image_with_face_boxes(img, faces)
    if show_vertical_lines:
        x_positions = x_positions_in_image(img)
        img = image_with_vertical_lines(img, x_positions)
        region_selected = get_face_position_x_from_image(img, faces)
        img = box_of_selected_area(img, region_selected)
    if texts is not None:
        img = draw_texts(img, texts)
    
    return img

def display_image(img):
    cv2.imshow('img', img)
    cv2.waitKey()

def calculate_degreee_from_duty(duty):
    duty_range = DUTY_MAX - DUTY_MIN
    degree = ((duty - DUTY_MIN) / duty_range) * 180
    return degree

def calculate_duty_from_degree(degree):
    duty_range = DUTY_MAX - DUTY_MIN
    duty = (degree / 180) * duty_range + DUTY_MIN

    return np.round(duty, 2)

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
        self.assertEqual(full_screen_face_position_x, 0.5)
        mid_right_face_position_x = get_face_face_position_x(100, (50, 60, 0, 0))
        self.assertEqual(mid_right_face_position_x, 0.5)
        far_left_face_position_x = get_face_face_position_x(100, (10, 20, 30, 40))
        self.assertEqual(far_left_face_position_x, 0.2)
        large_far_left_quandrant = get_face_face_position_x(1000, (0, 50, 900, 900))
        self.assertEqual(large_far_left_quandrant, 0.4)
        far_right_face_position_x = get_face_face_position_x(100, (80, 10, 10, 20))
        self.assertEqual(far_right_face_position_x, 0.8)
    def test_integration_get_face_position_x_from_image(self):
        face_position_x = get_face_position_x_from_image(self.test_image)
        # Mike Pence is near the center, so this will be dead center
        self.assertEqual(face_position_x, 0.3)
    def test_calculate_degreee_from_duty(self):
        self.assertEqual(calculate_degreee_from_duty(7), 90)
        self.assertEqual(calculate_degreee_from_duty(2), 0)
        self.assertEqual(calculate_degreee_from_duty(10.5), 153)
        self.assertEqual(calculate_degreee_from_duty(12), 180)
    def test_calculate_duty_from_degree(self):
        self.assertEqual(calculate_duty_from_degree(0), 2)
        self.assertEqual(calculate_duty_from_degree(90), 7)
        self.assertEqual(calculate_duty_from_degree(94), 7.22)
        self.assertEqual(calculate_duty_from_degree(180), 12)

def display_test_image():
    img = load_test_image()
    faces = find_person(img)
    texts = ['hello', 'world']
    img = extend_image(img, show_faces=True, show_vertical_lines=True, texts=texts, faces=faces)
    display_image(img)

if IS_TEST:
    display_test_image()

    unittest.main()
