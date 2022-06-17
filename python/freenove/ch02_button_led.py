
import RPi.GPIO as GPIO
import time

from typing import Callable

LED_PIN = 11
BUTTON_PIN = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def alert_ready():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)

def light_when_pressed():
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

def run_for_duration(callback: Callable, seconds: int):
    t_start = time.time()
    while True:
        t_end = time.time()
        if (t_end - t_start) > seconds:
            break

        callback()
        

def close():
    GPIO.cleanup()

setup()

alert_ready()

run_for_duration(light_when_pressed, 5)

close()