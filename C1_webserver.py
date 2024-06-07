# conda activate waterproject
import platform
import time
computer_name = platform.node()
print(computer_name)
if computer_name!="DESKTOP-7DC3UA9":
    import RPi.GPIO as GPIO
else:
    from myfake import GPIO


from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
import os

log_file = "log.csv"


class Device:
    def __init__(self, name, pin, location):
        self.name = name
        self.pin = pin
        self.location = location
        self.state = False
        self.turn_on_times=[]
        self.turn_off_times=[]

    def toggle(self):
        self.state = not self.state
        GPIO.output(self.pin, GPIO.LOW if self.state else GPIO.HIGH)
        # append the name, pin, location, state and time to the log file, put quotes around the name and location, use the full date and time
        # seperate with commas
        with open(log_file, "a") as f:
            f.write(f'"{self.name}", {self.pin}, "{self.location}", {self.state}, {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            # f.write(f'"{self.name}", {self.pin}, "{self.location}", {self.state}, {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
            

devices = [
    Device("power_cable_solenoid", 12, ""),
    Device("valve_1", 25, "Middle Garden"),
    Device("valve_2", 23, "Rock Wall Garden"),
    Device("valve_3", 18, "Grape Garden"),
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

def common_return(request):
    # get the  day of the week  and time to the second and add it to the context
    current_time = time.strftime("%A %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices, "current_time": current_time})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return common_return(request)
    

@app.post("/toggle/{pin}")
async def toggle_device(pin: int, request: Request):
    for device in devices:
        if device.pin == pin:
            device.toggle()
            break
    #  send the user to index function
    return common_return(request)
    
# show log
@app.get("/log_download")
async def log_download():
    return FileResponse(log_file, filename='log.csv')



@app.get("/schedule", response_class=HTMLResponse)
async def schedule(request: Request):
    return templates.TemplateResponse("set_schedule.html", {"request": request, "devices": devices})    






