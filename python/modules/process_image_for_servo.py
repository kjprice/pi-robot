import unittest
import cv2

from modules.image_module import load_test_image
from modules.config import CASCADE_XML_FILEPATH

face_cascade = cv2.CascadeClassifier(CASCADE_XML_FILEPATH)

IS_TEST = False
if __name__ == '__main__':
    IS_TEST = True

def get_faces(img):
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    return faces

def get_quadrant_thresholds(img_length):
    return list(range(0, img_length+1, img_length // 5))

def get_face_x_midpoint(face):
    x1, y1, x2, y2 = face

    offset = (x2 - x1) // 2

    return x1 + offset

# Will return one of [-2, -1, 0, 1, 2]
def get_face_quadrant(img_length, face):
    quadrant_thresholds = get_quadrant_thresholds(img_length)
    midpoint = img_length // 2

    x1, y1, x2, y2 = face
    farthest_left = abs(midpoint - x1)
    farthest_right = abs(midpoint - x2)
    face_x_midpoint = get_face_x_midpoint(face) 

    quadrant_start = -2
    for i in range(len(quadrant_thresholds) - 1):
        left, right = quadrant_thresholds[i:i+2]
        if face_x_midpoint >= left and face_x_midpoint < right:
            return i + quadrant_start
    
    return 2

def get_face_quadrant_from_image(img):
    faces = get_faces(img)

    face_quadrants = []
    for face in faces:
        face_quadrants.append(get_face_quadrant(img.shape[0], face))
    
    infinity = float('inf')
    most_center_quadrant = infinity
    for face_quadrant in face_quadrants:
        if abs(face_quadrant) < abs(most_center_quadrant):
            most_center_quadrant = face_quadrant
    
    if most_center_quadrant == infinity:
        return None

    return most_center_quadrant

def get_image_with_face_boxes(img):
    img_copy = img.copy()

    faces = get_faces(img)
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return img_copy

# To see what the image looks on the boxes
def display_image_and_boxes(img, boxes):
    img_with_faces = get_image_with_face_boxes(img)
    cv2.imshow('img', img_with_faces)
    cv2.waitKey()

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
    def test_get_quadrant_thresholds(self):
        self.assertEqual(get_quadrant_thresholds(100), [0, 20, 40, 60, 80, 100])
    def test_get_face_quadrants(self):
        # return
        full_screen_quadrant = get_face_quadrant(100, (0, 0, 100, 100))
        self.assertEqual(full_screen_quadrant, 0)
        mid_right_quadrant = get_face_quadrant(100, (50, 60, 50, 60))
        self.assertEqual(mid_right_quadrant, 0)
        far_left_quadrant = get_face_quadrant(100, (10, 20, 30, 40))
        self.assertEqual(far_left_quadrant, -1)
        large_far_left_quandrant = get_face_quadrant(1000, (10, 50, 850, 900))
        self.assertEqual(large_far_left_quandrant, 0)
        far_right_quadrant = get_face_quadrant(100, (80, 10, 90, 30))
        self.assertEqual(far_right_quadrant, 2)
    def test_integration_get_face_quadrant_from_image(self):
        quadrant = get_face_quadrant_from_image(self.test_image)
        # Mike Pence is near the center, so this will be dead center
        self.assertEqual(quadrant, 0)

if IS_TEST:
    unittest.main()
