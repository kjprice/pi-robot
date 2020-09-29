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

# This is the actual servo setup
def setup_servo_main():

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    servo = GPIO.PWM(SERVO_PIN, 50) # 50 Hz pulse

    return servo

# This is the stubbed version of the servo for testing (not real)
class StubServo():
    def start(self, position):
        None
    def ChangeDutyCycle(self, n):
        None

class Servo():
    # Duty can go from 2-12% (0-180 degrees)
    duty_range = [2, 12]
    current_position = 0
    possible_positions = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    def __init__(self, is_test):
        if is_test:
            self.servo = StubServo()
        else:
            self.servo = setup_servo_main()
        
        self.servo.start(0)

    def go_to(self, position):
        if position not in self.possible_positions:
            return

        if position == self.current_position:
            return

        self.current_position = position

        duty = position + 7
        self.servo.ChangeDutyCycle(duty)
    def reset(self):
        self.go_to(0)
    def move_left(self):
        self.go_to(self.current_position - 1)
    def move_right(self):
        self.go_to(self.current_position + 1)
    def teardown(self):
        print('shutting down servo')
        if not IS_TEST:
            GPIO.cleanup()

class TestServoModule(unittest.TestCase):
    def setUp(self):
        self.servo = Servo(IS_TEST)
    def test_1_start_servo(self):
        self.assertEqual(self.servo.current_position, 0)
    def test_2_servo_positions(self):
        first_position = self.servo.possible_positions[0]
        last_position = self.servo.possible_positions[-1]

        self.assertEqual(first_position + 7, self.servo.duty_range[0])
        self.assertEqual(last_position + 7, self.servo.duty_range[-1])

    def test_3_move_servo(self):
        self.assertEqual(self.servo.current_position, 0)

        self.servo.move_left()
        self.assertEqual(self.servo.current_position, -1)
        self.servo.move_left()
        self.assertEqual(self.servo.current_position, -2)
        self.servo.reset()
        self.assertEqual(self.servo.current_position, 0)
        self.servo.move_right()
        self.assertEqual(self.servo.current_position, 1)

        self.servo.go_to(5)
        self.assertEqual(self.servo.current_position, 5)
        self.servo.move_right()
        self.assertEqual(self.servo.current_position, 5)
        
        self.servo.go_to(-5)
        self.assertEqual(self.servo.current_position, -5)
        self.servo.move_left()
        self.assertEqual(self.servo.current_position, -5)

if IS_TEST:
    unittest.main()