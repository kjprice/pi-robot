import os
import time

import cv2
import numpy as np
from pynput import keyboard, mouse

from .modules.morse_code.morse_code import MorseCode

def image_to_brightness_data(image):
    return image.mean()


def detect_morse_from_images():
    TEST_IMAGES_PATH = os.path.join('..', 'data', 'test_morse_images')

    for img_name in os.listdir(TEST_IMAGES_PATH):
        img_path = os.path.join(TEST_IMAGES_PATH, img_name)
        img = cv2.imread(img_path)

        data = image_to_brightness_data(img)
        print('{}: {}'.format(img_name, data))

def detect_morse_from_keypress():
    while True:
        # https://stackoverflow.com/questions/40649634/determine-length-of-keypress-in-python
        def on_key_release(key): #what to do on key-release
            time_taken = round(time.time() - t, 2) #rounding the long decimal float
            print("The key",key," is pressed for",time_taken,'seconds')
            return False #stop detecting more key-releases

        def on_key_press(key): #what to do on key-press
            return False #stop detecting more key-presses

        with keyboard.Listener(on_press = on_key_press) as press_listener: #setting code for listening key-press
            press_listener.join()

        t = time.time() #reading time in sec

        with keyboard.Listener(on_release = on_key_release) as release_listener: #setting code for listening key-release
            release_listener.join()
class MorseCodeMouseClick():
    morse_code = None
    def __init__(self) -> None:
        self.morse_code = MorseCode()
    
    def listen(self):
        print('Left click on mouse to add action, any other mouse button will quit')
        with mouse.Listener(
            on_click=self.on_click,
        ) as listener:
            listener.join()

    def create_event(self, pressed: bool):
        # If button is pressed, then we want to store how long the button was not pressed (ie "not active")
        active = not pressed
        self.morse_code.add_event(active)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            self.create_event(pressed)
            words = self.morse_code.translate_data()
            print(words)
        elif button == mouse.Button.x2:
            if pressed:
                print('Pressed "{}". Restarting'.format(button))
                self.morse_code = MorseCode()
        else:
            print()
            print('Pressed "{}". Quiting'.format(button))
            return False

# detect_morse_from_images()
# detect_morse_from_keypress()
if __name__ == '__main__':
    MorseCodeMouseClick().listen()
