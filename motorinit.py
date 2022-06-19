import RPi.GPIO as gpio

STEP = 18
DIR = 15
MODE1 = 21
MODE2 = 20
STBY = 23
LED = 14
    
def initialize():
    # Initializes GPIOs
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(STBY, gpio.OUT)
    gpio.setup(STEP, gpio.OUT)
    gpio.setup(DIR, gpio.OUT)
    gpio.setup(MODE1, gpio.OUT)
    gpio.setup(MODE2, gpio.OUT)
    gpio.setup(LED, gpio.OUT)
    gpio.output(LED, gpio.LOW)

def stop():
    # Setting GPIOs to 0
    gpio.output(STEP, gpio.LOW)
    gpio.output(DIR, gpio.LOW)
    gpio.output(MODE1, gpio.LOW)
    gpio.output(MODE2, gpio.LOW)
    gpio.output(STBY, gpio.LOW)
    gpio.output(LED, gpio.LOW)
    
initialize()
stop()