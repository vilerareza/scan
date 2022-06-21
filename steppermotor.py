from time import sleep
import RPi.GPIO as gpio

class StepperMotor(object):
    # RasPi GPIOs - adjust when needed
    STEP = 18
    DIR = 15
    DIR_CW = 0
    DIR_CCW = 1
    MODE1 = 21
    MODE2 = 20
    STBY = 23
    LED = 14
    END_POS = 16

    SPR = 24    # Steps per revolution = 360/15 => As per datasheet
    DEC_RATIO = 5   # Motor deceleration ratio, refer to datasheet

    def __init__(self) -> None:
        self.initialize()
        self.set_mode()
    
    def initialize(self):
        # Initializes GPIOs
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.STBY, gpio.OUT)
        gpio.setup(self.STEP, gpio.OUT)
        gpio.setup(self.DIR, gpio.OUT)
        gpio.setup(self.MODE1, gpio.OUT)
        gpio.setup(self.MODE2, gpio.OUT)
        gpio.setup(self.END_POS, gpio.IN, pull_up_down=gpio.PUD_UP)

    def set_mode(self, mode=1):
        if mode == 1:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.LOW)
            gpio.output(self.MODE2, gpio.LOW)
        elif mode == 4:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.HIGH)
            gpio.output(self.MODE1, gpio.LOW)
            gpio.output(self.MODE2, gpio.HIGH)
        elif mode == 8:
            gpio.output(self.STEP, gpio.HIGH)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.HIGH)
            gpio.output(self.MODE2, gpio.HIGH)
        elif mode == 16:
            gpio.output(self.STEP, gpio.HIGH)
            gpio.output(self.DIR, gpio.HIGH)
            gpio.output(self.MODE1, gpio.HIGH)
            gpio.output(self.MODE2, gpio.HIGH)
        elif mode == 32:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.LOW)
            gpio.output(self.MODE2, gpio.HIGH)
        elif mode == 64:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.HIGH)
            gpio.output(self.MODE1, gpio.HIGH)
            gpio.output(self.MODE2, gpio.HIGH)
        elif mode == 128:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.HIGH)
            gpio.output(self.MODE2, gpio.LOW)
        elif mode == 256:
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.HIGH)
            gpio.output(self.MODE2, gpio.HIGH)
        else:
            print('Mode not valid, use mode 1')
            gpio.output(self.STEP, gpio.LOW)
            gpio.output(self.DIR, gpio.LOW)
            gpio.output(self.MODE1, gpio.LOW)
            gpio.output(self.MODE2, gpio.LOW)
        self.reset()

    def stop(self):
        # Setting GPIOs to 0
        gpio.output(self.STEP, gpio.LOW)
        gpio.output(self.DIR, gpio.LOW)
        gpio.output(self.MODE1, gpio.LOW)
        gpio.output(self.MODE2, gpio.LOW)
        gpio.output(self.STBY, gpio.LOW)
        print ('Motor stopped')
        
    def reset(self):
        # Reset the driver state
        gpio.output(self.STBY, gpio.LOW)
        sleep(0.2)
        gpio.output(self.STBY, gpio.HIGH)

    def home(self, dir = 'f', mode = 1, delay=0.002):
        try:
            print (f'Move to home position...')
            self.set_mode(mode)
            gpio.output(self.DIR, self.DIR_CCW)
            while gpio.input(self.END_POS):    # Check the condition of end position
                gpio.output(self.STEP, gpio.HIGH)
                sleep(delay)
                gpio.output(self.STEP, gpio.LOW)
                sleep (delay)
            print (f'Home position reached...')
            self.stop()
            return True
        except Exception as e:
            print (e)
            self.stop()
            return False

    def move(self, dir = 'f', steps = 1, mode = 1, delay=0.05):
        if dir == 'f':
            try:
                # Move forward
                print (f'Move forward {steps} step(s) with mode 1 / {mode}')
                self.set_mode(mode)
                gpio.output(self.DIR, self.DIR_CW)
                for x in range(steps):
                    if gpio.input(self.END_POS):    # Check the condition of end position:    # Check the condition of end position switch later
                        gpio.output(self.STEP, gpio.HIGH)
                        sleep(delay)
                        gpio.output(self.STEP, gpio.LOW)
                        sleep (delay)
            except Exception as e:
                print (e)
            finally:
                self.stop()

        elif dir == 'r':
            try:
                # Move reverse
                print (f'Move backward {steps} step(s) with mode 1 / {mode}')
                self.set_mode(mode)
                gpio.output(self.DIR, self.DIR_CCW)
                #for x in range(SPR*DEC_RATIO*steps*mode):
                for x in range(steps):
                    if True:    # Check the condition of end position switch later
                        gpio.output(self.STEP, gpio.HIGH)
                        sleep(delay)
                        gpio.output(self.STEP, gpio.LOW)
                        sleep (delay)
            except Exception as e:
                print (e)
            finally:
                self.stop()

        else:
            print ('Direction is not valid')