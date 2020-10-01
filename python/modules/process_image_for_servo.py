import unittest

import cv2
import numpy as np

try:
    from modules.image_module import load_test_image
    from modules.config import CASCADE_XML_FILEPATH
except ModuleNotFoundError:
    from image_module import load_test_image
    from config import CASCADE_XML_FILEPATH
face_cascade = cv2.CascadeClassifier(CASCADE_XML_FILEPATH)

IS_TEST = False
if __name__ == '__main__':
    IS_TEST = True

DUTY_MIN = 2
DUTY_MAX = 12

def get_faces(img):
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    return faces

def get_face_x_midpoint(face):
    x1, y1, x2, y2 = face

    offset = (x2 - x1) // 2

    return x1 + offset

# Will return one of [-2, -1, 0, 1, 2]
def get_face_quadrant(img_length, face_box):
    face_x_midpoint = get_face_x_midpoint(face_box) 
    return np.round(face_x_midpoint / img_length, 1)

def get_most_center_quadrant(face_quadrants):
    infinity = float('inf')
    most_center_quadrant = infinity
    for face_quadrant in face_quadrants:
        if abs(face_quadrant - 0.5) < abs(most_center_quadrant):
            most_center_quadrant = face_quadrant
    
    if most_center_quadrant == infinity:
        return None
    
    return most_center_quadrant

def get_face_quadrant_from_image(img):
    faces = get_faces(img)

    face_quadrants = []
    for face in faces:
        face_quadrants.append(get_face_quadrant(img.shape[0], face))

    return get_most_center_quadrant(face_quadrants)

def get_image_with_face_boxes(img):
    color_image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    faces = get_faces(color_image)
    for (x, y, w, h) in faces:
        cv2.rectangle(color_image, (x, y), (x+w, y+h), (0, 0, 255), 1)
    
    return color_image

# To see what the image looks on the boxes
def display_image(img, show_faces=False, vertical_lines=None):
    if show_faces:
        img = get_image_with_face_boxes(img)
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
        return get_face_x_midpoint((x1, -1, x2, -1))
    def test_get_face_midpoint(self):
        self.assertEqual(self.get_face_midpoint(40, 60), 50)
        self.assertEqual(self.get_face_midpoint(10, 20), 15)
        self.assertEqual(self.get_face_midpoint(0, 100), 50)
        self.assertEqual(self.get_face_midpoint(30, 50), 40)
    def test_get_face_quadrants(self):
        # return
        full_screen_quadrant = get_face_quadrant(100, (0, 0, 100, 100))
        self.assertEqual(full_screen_quadrant, 0.5)
        mid_right_quadrant = get_face_quadrant(100, (50, 60, 50, 60))
        self.assertEqual(mid_right_quadrant, 0.5)
        far_left_quadrant = get_face_quadrant(100, (10, 20, 30, 40))
        self.assertEqual(far_left_quadrant, 0.2)
        large_far_left_quandrant = get_face_quadrant(1000, (0, 50, 900, 900))
        self.assertEqual(large_far_left_quandrant, 0.4)
        far_right_quadrant = get_face_quadrant(100, (80, 10, 90, 30))
        self.assertEqual(far_right_quadrant, 0.8)
    def test_integration_get_face_quadrant_from_image(self):
        quadrant = get_face_quadrant_from_image(self.test_image)
        # Mike Pence is near the center, so this will be dead center
        self.assertEqual(quadrant, 0.6)
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

if IS_TEST:
    img = load_test_image()

    unittest.main()
