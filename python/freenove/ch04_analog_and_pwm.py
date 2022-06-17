print('hiya')

import time

import RPi.GPIO as GPIO

LED_PIN = 12
FREQUENCY = 500

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)

def start_pwm():
    p = GPIO.PWM(LED_PIN, FREQUENCY)
    p.start(0)

    return p

def run():
    p = start_pwm()
    for i in range(5):
        for dc in range (0, 101, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        time.sleep(0.5)
        for dc in range (100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        time.sleep(0.5)


def close():
    GPIO.cleanup()

setup()
run()
close()