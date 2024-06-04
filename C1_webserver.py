# conda activate waterproject
import platform
computer_name = platform.node()
print(computer_name)
if computer_name!="DESKTOP-7DC3UA9":
    import RPi.GPIO as GPIO
else:
    from myfake import GPIO


import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
import os


class Device:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.state = False
        self.turn_on_times=[]
        self.turn_off_times=[]

    def toggle(self):
        self.state = not self.state
        GPIO.output(self.pin, GPIO.LOW if self.state else GPIO.HIGH)

devices = [
    Device("power_cable_solenoid", 12),
    Device("valve_1", 25),
    Device("valve_2", 23),
    Device("valve_3", 18)
]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for device in devices:
    GPIO.setup(device.pin, GPIO.OUT)
    GPIO.output(device.pin, GPIO.HIGH)  # Ensure all pins are off initially
    

def load_schedule(file_path='schedule.json'):
    if not os.path.exists(file_path):
        return devices
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for device_data in data:
        device = next((d for d in devices if d.name == device_data["name"] and d.pin == device_data["pin"]), None)
        if device:
            device.turn_on_times = device_data["turn_on_times"]
            device.turn_off_times = device_data["turn_off_times"]
    
    return devices

def write_schedule(devices, file_path='schedule.json'):
    data = []
    for device in devices:
        data.append({
            "name": device.name,
            "pin": device.pin,
            "turn_on_times": device.turn_on_times,
            "turn_off_times": device.turn_off_times
        })
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


# ----------------------- FastAPI -----------------------

app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

@app.post("/toggle/{pin}")
async def toggle_device(pin: int, request: Request):
    for device in devices:
        if device.pin == pin:
            device.toggle()
            break
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})

