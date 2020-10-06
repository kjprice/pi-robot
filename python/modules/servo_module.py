import time
import unittest

IS_TEST = False
if __name__ == '__main__':
    IS_TEST = True

# This import will fail on a mac
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    None

# Settings
SERVO_PIN = 7 # Can be any IO pins including: 7,11,12,13,15,16,18,22

def setup_servo_main():

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    servo = GPIO.PWM(SERVO_PIN, 50) # 50 Hz pulse

    return servo

# input will be between 0-1
def calculate_duty_from_image_position(img_position_x):
    # from 0-0.5
    distance_from_center = abs(0.5 - img_position_x)
    ratio_away_from_center = distance_from_center / 0.5

    # Duties needed to go from one side of an image to the other
    duty_per_full_image = 0.35
    half_duty_per_full_image = duty_per_full_image / 2

    duty_change = ratio_away_from_center * half_duty_per_full_image

    return duty_change * 2

# This is the stubbed version of the servo for testing (not real)
class StubServo():
    def start(self, position):
        None
    def ChangeDutyCycle(self, n):
        None

class Servo():
    # Duty can go from 2-12% (0-180 degrees)
    duty_range = [2, 12]
    center = duty_range[0] + ((duty_range[1] - duty_range[0]) // 2)
    current_duty = center
    def __init__(self, is_test):
        if is_test:
            self.servo = StubServo()
        else:
            self.servo = setup_servo_main()
        
        self.servo.start(0)

    def go_to(self, duty):
        if duty < self.duty_range[0] or duty > self.duty_range[1]:
            return

        if duty == self.current_duty:
            return

        self.current_duty = duty

        self.servo.ChangeDutyCycle(duty)
    def reset(self):
        self.go_to(self.center)
    def move_left(self, amount_to_move):
        self.go_to(self.current_duty - amount_to_move)
    def move_right(self, amount_to_move):
        self.go_to(self.current_duty + amount_to_move)
    def teardown(self):
        print('shutting down servo')
        if not IS_TEST:
            GPIO.cleanup()

class TestServoModule(unittest.TestCase):
    def setUp(self):
        self.servo = Servo(IS_TEST)
    def test_calculate_duty_from_image_position(self):
        self.assertEqual(calculate_duty_from_image_position(1), 0.175)
        self.assertEqual(calculate_duty_from_image_position(0), 0.175)
        self.assertEqual(calculate_duty_from_image_position(0.5), 0)
        self.assertEqual(calculate_duty_from_image_position(0.25), 0.0875)

    def test_1_start_servo(self):
        self.assertEqual(self.servo.current_duty, 7)

    def test_3_move_servo(self):
        self.assertEqual(self.servo.current_duty, 7)

        self.servo.move_left(1)
        self.assertEqual(self.servo.current_duty, 6)
        self.servo.move_left(1)
        self.assertEqual(self.servo.current_duty, 5)
        self.servo.reset()
        self.assertEqual(self.servo.current_duty, 7)
        self.servo.move_right(1)
        self.assertEqual(self.servo.current_duty, 8)

        self.servo.go_to(12)
        self.assertEqual(self.servo.current_duty, 12)
        self.servo.move_right(1)
        self.assertEqual(self.servo.current_duty, 12)
        
        self.servo.go_to(2)
        self.assertEqual(self.servo.current_duty, 2)
        self.servo.move_left(1)
        self.assertEqual(self.servo.current_duty, 2)

if IS_TEST:
    unittest.main()