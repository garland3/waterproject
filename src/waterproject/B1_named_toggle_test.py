import RPi.GPIO as GPIO
import time

# Pin Definitions
PIN_POWER_CABLE_SOLENOID = 12
PIN_VALVE_1 = 25
PIN_VALVE_2 = 23
PIN_VALVE_3 = 18

# Device to pin mapping
device_pins = {
    "power_cable_solenoid": PIN_POWER_CABLE_SOLENOID,
    "valve_1": PIN_VALVE_1,
    "valve_2": PIN_VALVE_2,
    "valve_3": PIN_VALVE_3
}

# Time variables
on_time = 3  # Time to keep the LED on
off_time = 1  # Time to keep the LED off

def setup_pins(pins):
    GPIO.setmode(GPIO.BCM)
    for pin in pins.values():
        GPIO.setup(pin, GPIO.OUT)

def blink_leds(pins, on_duration, off_duration):
    for device, pin in pins.items():
        print(f"Turning on {device} (PIN {pin})")
        GPIO.output(pin, GPIO.LOW)   # Turn device on (inverted logic)
        time.sleep(on_duration)      # Wait for on_duration seconds
        print(f"Turning off {device} (PIN {pin})")
        GPIO.output(pin, GPIO.HIGH)  # Turn device off (inverted logic)
        time.sleep(off_duration)     # Wait for off_duration seconds

def main():
    setup_pins(device_pins)
    try:
        print("Start up sleep dwell")
        time.sleep(5)
        for pin in device_pins.values():
            GPIO.output(pin, GPIO.HIGH)  # Ensure all pins are off initially

        blink_leds(device_pins, on_time, off_time)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
