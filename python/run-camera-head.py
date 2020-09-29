import atexit
import time
import os

from image_module import save_image
from camera_module import capture_camera_image, camera_setup, shutdown_camera
from process_image_for_servo import get_face_quadrant_from_image, get_image_with_face_boxes
from servo_module import Servo

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

def save_image_with_faces(img):
    img_with_faces = get_image_with_face_boxes(img)

    save_image(img_with_faces, 'test-face-image.jpg')

def move_servo_based_on_quadrant(quadrant):
    if quadrant < 0:
        servo.move_left()
    elif quadrant > 0:
        servo.move_right()
    else:
        servo.reset()

camera_setup(IS_TEST)
servo = Servo(IS_TEST)
while True:
    img = capture_camera_image(IS_TEST)

    quadrant = get_face_quadrant_from_image(img)
    if IS_TEST:
        save_image_with_faces(img)
    
    move_servo_based_on_quadrant(quadrant)



atexit.register(shutdown_camera, servo.teardown)