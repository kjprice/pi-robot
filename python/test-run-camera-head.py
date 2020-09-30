#!/usr/bin/python3
# Taken from https://www.youtube.com/watch?v=xHDT4CwjUQE
import RPi.GPIO as GPIO
import time

# Settings
SERVO_PIN = 7 # Can be any IO pins including: 7,11,12,13,15,16,18,22
TIME_WAIT = 2 # seconds


servo = None

print('Waiting for {} seconds'.format(TIME_WAIT))
time.sleep(1)

# Duty can go from 2-12% (0-180 degrees)
DUTY_MIN = 2.2
DUTY_MAX = 11.8

def turn_on():
    global servo
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = GPIO.PWM(SERVO_PIN, 50) # 50 Hz pulse

    servo.start(0)

def turn_off():
    print('Shutting down')
    GPIO.cleanup()

def wait():
    time.sleep(1)

def run_low():
    print('Setting servo to beginning')
    servo.ChangeDutyCycle(DUTY_MIN)

def run_high():
    print('Setting servo to end')
    servo.ChangeDutyCycle(DUTY_MAX)

def run_middle():
    print('Turning back 90 degrees for 2 seconds')
    servo.ChangeDutyCycle(7)

def set_specific_duty(n):
    try:
        num = float(n)
    except ValueError:
        return

    if num < 2:
        print('Number {} is too low. Ignoring'.format(n))
        return
    if num > 12:
        print('Number {} is too high. Ignoring'.format(n))
        return
    
    print('Turning to {}'.format(num))

    servo.ChangeDutyCycle(num)

def run_all_tests():
    run_low()
    wait()
    run_high()
    wait()
    run_middle()
    wait()

# TODO: Allow to switch from position 0-10 (mapped to 2-12) via the keyboard
# TODO: Test what happens when you disconnect/reconnect the servo


instructions = '''
Please type any of the following commands:
Positions: l=low | h=high | m=middle
Positions(any): any number greater than 2
State: on | off | e=exit
Instructions: i = show-instructions
'''

def show_instructions():
    print(instructions)

turn_on()
wait()
show_instructions()

while True:
    x = input()
    if x == '':
        continue

    if x == 'l':
        run_low()
    if x == 'm':
        run_middle()
    if x == 'h':
        run_high()
    if x == 'on':
        turn_on()
    if x == 'off':
        turn_off()
    if x == 'i':
        show_instructions()
    if x == 'e':
        break

    set_specific_duty(x)
    x = ''
        

turn_off()

