import RPi.GPIO as gpio
import time

LED = 14

def led_init(pin):
    # Initializes GPIOs
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(pin, gpio.OUT)

def led_on(pin):
    gpio.output(pin, gpio.HIGH)

def led_off(pin):
    gpio.output(pin, gpio.LOW)

led_init(LED)
led_on(LED)
time.sleep(5)
led_off(LED)
print ('LED test completed')

