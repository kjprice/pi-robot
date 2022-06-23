from functools import reduce
import unittest

import cv2
import numpy as np

from .image_module import is_image_grayscale, load_test_image


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

# TODO: IMPORTANT - we may want to run all of these in parallel and find the optimal person

# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def calculate_image_clarity(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()
    
def get_person_x_midpoint(person):
    x1, y1, width, height = person['box_points']

    return x1 + (width // 2)

def get_person_person_position_x(img_width, person_box):
    person_x_midpoint = get_person_x_midpoint(person_box)

    # Will be between 0-1
    ratio_person_center_on_image = np.round(person_x_midpoint / img_width, 1)

    # Will return a number between -1 and 1
    return np.round(ratio_person_center_on_image * 2 - 1, 2)

def width(person):
    return person['box_points'][2]

def get_widest_person(people_detected):
    if len(people_detected) == 0:
        return None
    return reduce(lambda a, b: a if width(a) > width(b) else b, people_detected)

    
def get_primary_person(people_detected):
    return get_widest_person(people_detected)

def get_person_position_x_from_image(img, people_detected):
    if people_detected is None or len(people_detected) == 0:
        return None

    primary_person = get_primary_person(people_detected)

    return get_person_person_position_x(img.shape[1], primary_person)

def draw_box(img, object_detected, color=(0,0,255), line_width=1):
    x, y, w, h = object_detected['box_points']
    cv2.rectangle(img, (x, y), (x+w, y+h), color, line_width)

# TODO: This is only needed for faces, we can already have the image "extended" when using imageai
def get_image_with_person_boxes(img, persons):
    if is_image_grayscale(img):
        color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        color_image = img
    if persons is None or len(persons) == 0:
        return color_image

    for person in persons:
        draw_box(color_image, person)
    primary_person = get_primary_person(persons)

    draw_box(color_image, primary_person, color=(0,255,255))
    
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

def draw_primary_person_line(img, persons):
    if persons is None or len(persons) == 0:
        return img

    primary_person = get_primary_person(persons)

    x, y, w, h = primary_person['box_points']
    line_x = int(x + (w /2))

    return image_with_vertical_line(img, line_x)

def draw_texts(img, texts):
    img_height = img.shape[0]
    middle_y = img_height // 2
    for i, text in enumerate(texts):
        y = middle_y + (i * 30)
        img = cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

# Can be used for debugging purposes
# TODO: Need to change all of this
def extend_image(img, show_objects_detected=False, show_vertical_lines=False, texts=None, objects_detected=None):
    if show_objects_detected:
        img = get_image_with_person_boxes(img, objects_detected)
    if show_vertical_lines:
        img = draw_primary_person_line(img, objects_detected)

    if texts is not None:
        img = draw_texts(img, texts)
    
    return img

def display_image(img):
    cv2.imshow('img', img)
    cv2.waitKey()

class TestProcessImages(unittest.TestCase):
    def setUp(self):
        self.test_image = load_test_image()
    def get_person_midpoint(self, x1, x2):
        width = x2 - x1
        return get_person_x_midpoint((x1, -1, width, -1))
    def test_get_person_midpoint(self):
        self.assertEqual(self.get_person_midpoint(40, 60), 50)
        self.assertEqual(self.get_person_midpoint(10, 20), 15)
        self.assertEqual(self.get_person_midpoint(0, 100), 50)
        self.assertEqual(self.get_person_midpoint(30, 50), 40)
    def test_get_person_person_position_xs(self):
        # return
        full_screen_person_position_x = get_person_person_position_x(100, (0, 0, 100, 100))
        self.assertEqual(full_screen_person_position_x, 0)
        mid_right_person_position_x = get_person_person_position_x(100, (50, 60, 0, 0))
        self.assertEqual(mid_right_person_position_x, 0)
        far_left_person_position_x = get_person_person_position_x(100, (10, 20, 30, 40))
        self.assertEqual(far_left_person_position_x, -0.6)
        large_far_left_quandrant = get_person_person_position_x(1000, (0, 50, 900, 900))
        self.assertEqual(large_far_left_quandrant, -0.2)
        far_right_person_position_x = get_person_person_position_x(100, (80, 10, 10, 20))
        self.assertEqual(far_right_person_position_x, 0.6)
    def test_integration_get_person_position_x_from_image(self):
        person_position_x = get_person_position_x_from_image(self.test_image)
        # Mike Pence is near the center, so this will be dead center
        self.assertEqual(person_position_x, -0.4)

# def display_test_image():
#     img = load_test_image()
#     # persons = find_person(img)
#     texts = ['hello', 'world']
#     img = extend_image(img, show_persons=True, show_vertical_lines=True, texts=texts, persons=persons)
#     display_image(img)

if IS_TEST:
    # display_test_image()

    unittest.main()
