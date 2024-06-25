import json
import platform
from waterproject.wlib.Utilities import log_file
import time
computer_name = platform.node()
if computer_name=="DESKTOP-7DC3UA9" or computer_name=='desktop':
    from waterproject.wlib.myfake import GPIO
else:
    import RPi.GPIO as GPIO
    
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class Device:
    def __init__(self, name, pin, location):
        self.name = name
        self.pin = pin
        self.location = location
        self.state = False
        self.turn_on_times=[]
        self.turn_off_times=[]
        
    def set_state(self, state_int:int):
        """State must be an int of 0 or 1, 0 is off, 1 is on"""
        
        self.state = True if state_int == 1 else False

        # NOTE. This seems backwards.  But is correct
        value = GPIO.LOW if self.state  else GPIO.HIGH
        
        GPIO.output(self.pin, value)
        self.write_log()
        print(f"Set state {self.name} to {self.state}")

        
    def write_log(self):    
        # append the name, pin, location, state and time to the log file, put quotes around the name and location, use the full date and time
        # seperate with commas
        with open(log_file, "a") as f:
            f.write(f'"{self.name}", {self.pin}, "{self.location}", {self.state}, {time.strftime("%Y-%m-%d %H:%M:%S")}\n')


    def toggle(self):
        self.state = not self.state
        # NOTE. This seems backwards.  But is correct
        GPIO.output(self.pin, GPIO.LOW if self.state else GPIO.HIGH)
        self.write_log()
            
# def create_devices():
#     devices = [
#         Device("power_cable_solenoid", 12, "Top of Water Containers"),
#         Device("valve_1", 25, "Middle Garden"),
#         Device("valve_2", 23, "Rock Wall Garden"),
#         Device("valve_3", 18, "Grape Garden"),
#     ]
#     return devices
def create_devices(file_path="devices.json"):
    with open(file_path, 'r') as f:
        data = json.load(f)
    devices = [Device(device['name'], device['pin'], device['location']) for device in data]
    return devices

# Setup GPIO
def setup_gpio(devices):
    GPIO.setmode(GPIO.BCM)
    for device in devices:
        GPIO.setup(device.pin, GPIO.OUT)
        GPIO.output(device.pin, GPIO.HIGH)  # Ensure all pins are off initially