import RPi.GPIO as GPIO
import time

# Pin Definitions
led_pins = [12, 25, 23, 18]  # List of GPIO pins connected to LEDs

# Time variables
on_time = 3  # Time to keep the LED on
off_time = 1  # Time to keep the LED off

# Setup
GPIO.setmode(GPIO.BCM)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Blink function
def blink_leds(pins, on_duration, off_duration):
    for pin in pins:
        print(f"Turning on PIN {pin}")
        GPIO.output(pin, GPIO.HIGH)  # Turn LED on
        time.sleep(on_duration)      # Wait for on_duration seconds
        print(f"Turning off PIN {pin}")
        GPIO.output(pin, GPIO.LOW)   # Turn LED off
        time.sleep(off_duration)     # Wait for off_duration seconds

try:
    print("start up sleep dwell")
    time.sleep(5)
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)  # Turn PIN off

    blink_leds(led_pins, on_time, off_time)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
