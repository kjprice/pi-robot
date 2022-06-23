#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

# Motor One
# TODO: Switch in1/in2 on the actual board (right now forward/backward are reversed)
in1 = 24
in2 = 23
ena = 27 # Used to be 25
direction = 'forward'

# Motor Two
in3 = 25
in4 = 22
enb = 17

GPIO.setmode(GPIO.BCM)

# Motor One
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

p1=GPIO.PWM(ena,1000)
p1.start(ena)

# Motor Two
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

p2=GPIO.PWM(enb,1000)
p2.start(enb)

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run p-stop l-low m-medium h-high e-exit")
print("w-forward a-left d-right s-backward")
print("\n")    

all_wheels = {
    'left': {
        'name': 'left',
        'in1': in1,
        'in2': in2,
        'en': ena,
        'p': p1
    },
    'right': {
        'name': 'right',
        'in1': in3,
        'in2': in4,
        'en': enb,
        'p': p2
    },
}

def get_wheels():
    return all_wheels.values()


def set_wheels(code):
    global direction
    direction = None
    if code == 'w':
        direction = 'forward'
    if code == 's':
        direction = 'backward'
    if code == 'a':
        direction = 'left'
    if code == 'd':
        direction = 'right'
    
    if direction is None:
        raise ValueError('Unknown code "{}"'.format(code))

    print(direction)

    run()

def stop():
    wheels = get_wheels()
    for wheel in wheels:
        _in1 = wheel['in1']
        _in2 = wheel['in2']

        GPIO.output(_in1,GPIO.LOW)
        GPIO.output(_in2,GPIO.LOW)


def run():
    wheels = get_wheels()

    for wheel in wheels:
        _in1 = wheel['in1']
        _in2 = wheel['in2']
        
        # Going forward or backward
        if direction == 'forward':
            GPIO.output(_in1, GPIO.HIGH)
            GPIO.output(_in2, GPIO.LOW)
        elif direction == 'backward':
            GPIO.output(_in1, GPIO.LOW)
            GPIO.output(_in2, GPIO.HIGH)
        
        # Turning Left Or Right
        elif direction == wheel['name']:
            GPIO.output(_in1, GPIO.HIGH)
            GPIO.output(_in2, GPIO.LOW)
        elif direction != wheel['name']:
            GPIO.output(_in1, GPIO.LOW)
            GPIO.output(_in2, GPIO.LOW)
        else:
            raise Exception('Could not find a match for direction "{}"'.format(direction))
    
    # always reset x so we do not continuously change settings
    x = 'z'

def set_power(power_number): # 0 -1
    for p in [p1, p2]:
        p.ChangeDutyCycle(power_number)

def set_power_by_key(x):
    if x=='l':
        print("low")
        set_power(25)
        return

    elif x=='m':
        print("medium")
        set_power(40)
        return

    elif x=='h':
        print("high")
        set_power(75)
        return

direction = 'forward'

set_power_by_key('l')

while(1):
    x=raw_input()

    if x=='z': # This is default - just ignore
        continue
    
    if x=='r':
        print("run")
        if(direction=='forward'):
            run()
            print("forward")
        else:
            run()
            print("backward")


    elif x=='p':
        print("stop")
        x = 'z'
        stop()
    
    elif x in ['w', 'a', 's', 'd']:
        set_wheels(x)
        x = 'z'
        
        # run()

    elif x in ['l', 'm', 'h']:
        set_power_by_key(x)
        x = 'z'


     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")