import RPi.GPIO as GPIO
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

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

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in device_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Ensure all pins are off initially

# Create templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "devices": device_pins})

@app.post("/toggle/{device_name}/{action}")
async def toggle_device(device_name: str, action: str, request: Request):
    pin = device_pins.get(device_name)
    if pin is not None:
        if action == "on":
            GPIO.output(pin, GPIO.LOW)  # Turn device on (inverted logic)
        elif action == "off":
            GPIO.output(pin, GPIO.HIGH)  # Turn device off (inverted logic)
    message =  {"device": device_name, "action": action}
    return templates.TemplateResponse("index.html", {"request": request, "devices": device_pins, "message":message})


# @app.on_event("shutdown")
def shutdown_event():
    GPIO.cleanup()

def startup_event():
    print("starting up")

app.add_event_handler("shutdown", shutdown_event)
app.add_event_handler("startup", startup_event)

#if __name__ == "__main__":
#    import uvicorn
#    print("running localhost port 8000")
#    uvicorn.run(app, host="0.0.0.0", port=8000)
