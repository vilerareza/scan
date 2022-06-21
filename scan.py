from steppermotor import StepperMotor
from undistorter import Undistorter
import stack
import subprocess
import cv2 as cv
import argparse
import json
from threading import Condition, Thread
import time

import RPi.GPIO as gpio

# Argument handler
parser = argparse.ArgumentParser()
parser.add_argument('pattern', type = str)
parser.add_argument('filename', type = str)
jsonDecoder = json.JSONDecoder()
# Unpack
args = parser.parse_args()
argPattern = args.pattern.replace("\'", "\"")
# Pattern
pattern = json.loads(argPattern)    # example: [{'dir':'f', 'steps': 1, 'mode':1, 'delay':0.05}]
# File Name
#fileName = args.filename

rawDir = "img_raw"
outDir = "img_corrected"
#unDistorter = Undistorter(calFile='cal_data.p')
unDistorter = Undistorter(calFile='camera_cal.p')
stepperMotor = StepperMotor()
LED = 14
t_hold_stbl = 1.5   # Stepper motor rest time (s) when camera is capturing.
t_hold_shot = 5
capture_timeout = 25
t_capture = Thread()
condition = Condition()

def led_init(pin):
    # Initializes GPIOs
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, gpio.LOW)

def led_on(pin):
    gpio.output(pin, gpio.HIGH)

def led_off(pin):
    gpio.output(pin, gpio.LOW)

def clear_output_dir(outDir):
    try:
        subprocess.run(['rm', '-f', f'{outDir}/*'])
    except Exception as e:
        print (f'Clearing image output directory failed: {e}')

def capture(rawDir, rawFile, outFile, condition):
    # Capture
    subprocess.run(['libcamera-still', '--denoise', 'off', '--shutter', '70000', '--gain', '0', '--awb', 'cloudy', '--immediate', '--rawfull', '-e', 'png', '-o', f'{rawDir}/{rawFile}'])
    try:
        img = cv.imread(f'{rawDir}/{rawFile}')
        img_cor = unDistorter.undistort(img)
        cv.imwrite(f'{outDir}/{outFile}.png', img_cor)
        with condition:
            condition.notify_all()
    except:
        print ('Raw image to undistort not found')

def start_capture_thread(rawDir, rawFile, outFile, condition):
    t_capture = Thread(target = capture, args = (rawDir, rawFile, outFile, condition))
    t_capture.start()

def start_scanning():
    try:
        t1 = time.time()
        # Clearing the result directory
        clear_output_dir(outDir)
        # Move from home position
        if stepperMotor.home():
            # Illumination on
            led_init(LED)
            led_on(LED)
            # Start pattern
            for i in range(len(pattern)):
                stepperMotor.move(dir = pattern[i]['dir'], steps = pattern[i]['steps'], mode = pattern[i]['mode'], delay=pattern[i]['delay'])
                # Stop for capturing
                time.sleep(t_hold_stbl)
                print (f'Movement stop, capturing...{i}')
                if i > 0:
                    # No need to wait for first move
                    with condition:
                        # wait until the last capture is completed
                        condition.wait(timeout = capture_timeout)
                start_capture_thread(rawDir, 'temp.png', str(i) , condition)
                time.sleep(t_hold_shot)
                print (f'Capture complete...{i}')
            # Illumination off
            with condition:
                # wait until the last capture is completed
                condition.wait(timeout = capture_timeout)
            led_off(LED)
            t2 = time.time()
            print (f'Scan complete. Timelapse: {str(t2-t1)}s')
            # Back to home position
            stepperMotor.home()
            stepperMotor.stop()
            return True

    except Exception as e:
        print (e)
        led_off(LED)
        stepperMotor.stop()
        return False
        
if start_scanning():
    stack.post_process()
else:
    print ('Failure during scanning.')


