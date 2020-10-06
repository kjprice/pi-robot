#!/usr/bin/python3
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time

import RPi.GPIO as GPIO

# This must be done before we bring in our modules because they depend on the correct directory
def cd_to_this_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
cd_to_this_directory()


from test_modules.test_camera import capture_camera_image, save_test_image
from modules.camera_module import camera_setup 
# Settings
SERVO_PIN = 7 # Can be any IO pins including: 7,11,12,13,15,16,18,22


servo = None
running_slowly = False
current_duty = 7 # Right in the middle

# Duty can go from 2-12% (0-180 degrees)
DUTY_MIN = 2.2
DUTY_MAX = 11.8

def turn_servo(duty):
    global current_duty
    if duty < 2:
        print('Number {} is too low. Ignoring'.format(n))
        return
    if duty > 12:
        print('Number {} is too high. Ignoring'.format(n))
        return
    
    current_duty = duty
    servo.ChangeDutyCycle(duty)

def turn_on():
    global servo
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = GPIO.PWM(SERVO_PIN, 50) # 50 Hz pulse

    servo.start(0)

def turn_off():
    print('Shutting down')
    GPIO.cleanup()

def wait(seconds=1):
    time.sleep(seconds)

def run_low():
    print('Setting servo to beginning')
    turn_servo(DUTY_MIN)

def run_high():
    print('Setting servo to end')
    turn_servo(DUTY_MAX)

def run_middle():
    print('Turning back 90 degrees for 2 seconds')
    turn_servo(7)

def start_running_slowly():
    global running_slowly
    print('starting to run slowly')

    running_slowly = True

def stop_running_slowly():
    global running_slowly
    print('ending process to run slowly')

    running_slowly = False

should_stop_immediately = False
async def try_to_run_slowly(future):
    global current_duty, running_slowly, should_stop_immediately
    while True:
        if should_stop_immediately:
            future.set_result('Exiting "Running Slowly" command')
            break
        if running_slowly:
            turn_servo(current_duty + 0.02)
        await asyncio.sleep(0.02)
    

def set_specific_duty(n):
    try:
        num = float(n)
    except ValueError:
        return

    print('Turning to {}'.format(num))

    turn_servo(num)

def run_all_tests():
    run_low()
    wait()
    run_high()
    wait()
    run_middle()
    wait()

def get_number_of_pictures_to_take(x):
    if x == 'p5':
        return 5
    if x == 'p10':
        return 10

    return None

def take_pictures(x):
    n = get_number_of_pictures_to_take(x)
    for i in range(n):
        print('Taking picture {} of {}'.format(i, n), end='\r')
        img = capture_camera_image()
        save_test_image(img, i, current_duty)
    print('Finished taking pictures')

instructions = '''
Please type any of the following commands:
Servo Instructions:
    Positions: l=low | h=high | m=middle
    Positions(any): any number greater than 2
    Routine: s=take pictures slowly
    State: on | off | e=exit
    Instructions: i = show-instructions
Camera Instructions:
    Take Pictures: p5="5 pictures" | p10="10 pictures"

'''

def show_instructions():
    print(instructions)

turn_on()
turn_servo(current_duty)
wait()
show_instructions()

async def ainput(prompt: str = ""):
    # TODO: remove the "print" stuff
    with ThreadPoolExecutor(1, "AsyncInput", lambda x: print(x, end="", flush=True), (prompt,)) as executor:
        return (await asyncio.get_event_loop().run_in_executor(
            executor, sys.stdin.readline
        )).rstrip()

async def handle_user_input(future):
    global should_stop_immediately
    while True:
        x = await ainput('')

        if x == '':
            continue

        if x in ['p5', 'p10']:
            take_pictures(x)
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
            should_stop_immediately = True
            future.set_result('closing user input')
            break
        if x == 's':
            start_running_slowly()
        else: # If any other key was typed we want to stop running slowly
            stop_running_slowly()

        # This is a catch all to see if the user provided a specific number
        set_specific_duty(x)
        x = ''

loop = asyncio.get_event_loop()

user_input_future = asyncio.Future()
asyncio.ensure_future(handle_user_input(user_input_future))

run_slowly_future = asyncio.Future()
asyncio.ensure_future(try_to_run_slowly(run_slowly_future))

loop.run_until_complete(asyncio.gather(
    user_input_future,
    run_slowly_future
))

turn_off()

