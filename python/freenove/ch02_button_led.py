
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

# Ch 2.1 
def light_when_pressed():
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)

# Ch 2.2
# Keep light on or off until button is pressed
def table_lamp():
    class TableLamp():
        button_state = GPIO.LOW
        def __init__(self) -> None:
            self.button_state = GPIO.LOW
            self.set_led()
            GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=self.button_press, bouncetime=300)
        def button_press(self, channel):
            if channel != BUTTON_PIN:
                raise Exception('Expected pin on channel {} to be pressed'.format(channel))
            
            self.button_state = GPIO.HIGH if self.button_state == GPIO.LOW else GPIO.LOW
            print(channel, LED_PIN, self.button_state)
            self.set_led()
            
        def set_led(self):
            GPIO.output(LED_PIN, self.button_state)

    TableLamp()

def run_for_duration(seconds: int, call_once: Callable = None, call_continuously: Callable = None ):
    t_start = time.time()
    if call_once:
        call_once()

    while True:
        t_end = time.time()
        if (t_end - t_start) > seconds:
            break

        if call_continuously:
            call_continuously()
        

def close():
    GPIO.cleanup()

setup()

alert_ready()

# run_for_duration(5, call_continuously=light_when_pressed)
run_for_duration(5, call_once=table_lamp)

close()