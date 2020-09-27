#!/usr/bin/python3
# Taken from https://www.youtube.com/watch?v=xHDT4CwjUQE
import RPi.GPIO as GPIO
import time

# Settings
SERVO_PIN = 7 # Can be any IO pins including: 7,11,12,13,15,16,18,22
TIME_WAIT = 2 # seconds

GPIO.setmode(GPIO.BOARD)


GPIO.setup(SERVO_PIN, GPIO.OUT)
servo1 = GPIO.PWM(SERVO_PIN, 50) # 50 Hz pulse

servo1.start(0)
print('Waitin for {} seconds'.format(TIME_WAIT))
time.sleep(TIME_WAIT)

print('Rotating 180 degrees in 10 steps')

# Duty can go from 2-12% (0-180 degrees)
DUTY_MIN = 2
DUTY_MAX = 12

duty = DUTY_MIN
while duty <= DUTY_MAX:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty += 1

print('Turning back 90 degrees for 2 seconds')
servo1.ChangeDutyCycle(7)
time.sleep(2)

GPIO.cleanup()