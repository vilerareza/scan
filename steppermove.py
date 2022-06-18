import argparse
from time import sleep
import RPi.GPIO as gpio

# Argument handler
parser = argparse.ArgumentParser()
parser.add_argument('steps', type = int, default = 1)
parser.add_argument('mode', type = int, default = 1)
parser.add_argument('delay', type = float, default = 0.05)
parser.add_argument("--reverse", help="move to reverse direction", action="store_true")
parser.add_argument("--reset", help="reset position", action="store_true")

args = parser.parse_args()
# GPIOs
STEP = 18
DIR = 15
DIR_CW = 1
DIR_CCW = 0
MODE1 = 21
MODE2 = 20
STBY = 23
LED = 14
END_POS = 16

SPR = 24    # Steps per revolution = 360/15 => As per datasheet
DEC_RATIO = 5   # Motor deceleration ratio
reverse = args.reverse
reset = args.reset
steps = int(args.steps)
delay = args.delay
mode = 1

# Parsing args
# Mode
if (args.mode == 1 or args.mode == 4 or args.mode == 8 or args.mode == 16 or args.mode == 32 or args.mode == 64 or args.mode == 128 or args.mode ==256):
    mode = args.mode
    print (f'Mode: {mode}')
else:
    mode = 1
    print ('Mode invalid. Use mode 1')
# Movement direction
if args.reverse:
    reverse = True
    print ('Reverse movement')
else:
    reverse = False
# Reset position
if args.reset:
    print ('Reset position')
# Delay
# if delay <0.01:
#     delay = 0.01

def reset():
    gpio.output(STBY, gpio.LOW)
    sleep(0.2)
    gpio.output(STBY, gpio.HIGH)

def set_mode(mode):
    if mode == 1:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.LOW)
        gpio.output(MODE1, gpio.LOW)
        gpio.output(MODE2, gpio.LOW)
    elif mode == 4:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.HIGH)
        gpio.output(MODE1, gpio.LOW)
        gpio.output(MODE2, gpio.HIGH)
    elif mode == 8:
        gpio.output(STEP, gpio.HIGH)
        gpio.output(DIR, gpio.LOW)
        gpio.output(MODE1, gpio.HIGH)
        gpio.output(MODE2, gpio.HIGH)
    elif mode == 16:
        gpio.output(STEP, gpio.HIGH)
        gpio.output(DIR, gpio.HIGH)
        gpio.output(MODE1, gpio.HIGH)
        gpio.output(MODE2, gpio.HIGH)
    elif mode == 32:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.LOW)
        gpio.output(MODE1, gpio.LOW)
        gpio.output(MODE2, gpio.HIGH)
    elif mode == 64:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.HIGH)
        gpio.output(MODE1, gpio.HIGH)
        gpio.output(MODE2, gpio.HIGH)
    elif mode == 128:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.LOW)
        gpio.output(MODE1, gpio.HIGH)
        gpio.output(MODE2, gpio.LOW)
    elif mode == 256:
        gpio.output(STEP, gpio.LOW)
        gpio.output(DIR, gpio.LOW)
        gpio.output(MODE1, gpio.HIGH)
        gpio.output(MODE2, gpio.HIGH)

def init():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(STBY, gpio.OUT)
    gpio.setup(STEP, gpio.OUT)
    gpio.setup(DIR, gpio.OUT)
    gpio.setup(MODE1, gpio.OUT)
    gpio.setup(MODE2, gpio.OUT)
    # Set Mode
    set_mode(mode)
    # Reset
    reset()

def stop():
    gpio.output(STEP, gpio.LOW)
    gpio.output(DIR, gpio.LOW)
    gpio.output(MODE1, gpio.LOW)
    gpio.output(MODE2, gpio.LOW)
    gpio.output(STBY, gpio.LOW)
    #gpio.cleanup()

if not reverse:
    try:
        init()
        # Move forward
        print (f'Move forward {steps} steps with mode 1 / {mode}')
        gpio.output(DIR, DIR_CW)
        #for x in range(SPR*DEC_RATIO*steps*mode):
        for x in range(steps):
            if True:    # Check the condition of end position switch later
                gpio.output(STEP, gpio.HIGH)
                sleep(delay)
                gpio.output(STEP, gpio.LOW)
                sleep (delay)
    
    except Exception as e:
        print (e)

    finally:
        stop()

else:
    try:
        init()
        # Move reverse
        print (f'Move backward {steps} steps')
        gpio.output(DIR, DIR_CCW)
        #for x in range(SPR*DEC_RATIO*steps*mode):
        for x in range(steps):
            if True:    # Check the condition of end position switch later
                gpio.output(STEP, gpio.HIGH)
                sleep(delay)
                gpio.output(STEP, gpio.LOW)
                sleep (delay)
    
    except Exception as e:
        print (e)

    finally:
        stop()