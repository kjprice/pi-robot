import atexit
import os

from flask import Flask, request
from flask_cors import CORS

from ..modules.servo_module import Servo

app = Flask(__name__)
CORS(app)

IS_TEST = False
if 'IS_TEST' in os.environ:
    IS_TEST = True

def main():
    @app.route('/testConnection')
    def test_connection():
        return 'success'

    servo = Servo(IS_TEST)

    @app.route('/resetServo', methods=['POST'])
    def reset_servo():
        servo.reset()
        return 'success'

    @app.route('/setServoPosition', methods=['POST'])
    def receive_servo_position():
        print('1. received data')
        data = request.get_json()

        duty = data['duty']

        print('2. decoded data')
        old_duty = servo.current_duty
        print('Moving From {} to {}'.format(old_duty, duty))

        servo.move(duty)

        print('3. set servo')
        new_duty = servo.current_duty
        print('Currently at duty {}'.format(new_duty))

        return 'success'

    atexit.register(servo.teardown)

if __name__ == '__main__':
    main()