import RPi.GPIO as GPIO
import time

# Pin Definitions
led_pin = 12  # GPIO pin connected to the LED

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Blink function
def blink_led():
    GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
    time.sleep(1)                    # Wait for 1 second
    GPIO.output(led_pin, GPIO.LOW)   # Turn LED off
    time.sleep(1)                    # Wait for 1 second
    print(f"PIN {led_pen} OFF")

try:
    while True:
        blink_led()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
