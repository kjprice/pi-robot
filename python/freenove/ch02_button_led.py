
import RPi.GPIO as GPIO
import time

LED_PIN = 11
BUTTON_PIN = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def run_during_seconds(seconds: int):
    t_start = time.time()
    while True:
        t_end = time.time()
        if (t_end - t_start) > seconds:
            break

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)

def close():
    GPIO.cleanup()

setup()

run_during_seconds(5)

close()