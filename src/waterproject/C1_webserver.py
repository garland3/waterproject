# conda activate waterproject
import platform
import time
computer_name = platform.node()
print(computer_name)


from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from helper import Device, TaskListManager, devices,  log_file, Task, setup_gpio
from waterproject.wlib.Device import Device, setup_gpio, create_devices
from waterproject.wlib.Task import Task   
from waterproject.wlib.TaskListManager import TaskListManager
from waterproject.wlib.Utilities import log_file

devices = create_devices()
setup_gpio(devices)


task_list_manager = TaskListManager(devices=devices)

# ----------------------- FastAPI -----------------------
app = FastAPI()

templates = Jinja2Templates(directory="src/waterproject/templates")

def common_return(request):
    # get the  day of the week  and time to the second and add it to the context
    current_time = time.strftime("%A %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices, "current_time": current_time})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return common_return(request)
    
# show log
@app.get("/log_download")
async def log_download():
    return FileResponse(log_file, filename=log_file, media_type='text/csv')

# reload the schedule from disk
@app.get("/reload_schedule")
async def reload_schedule(request: Request):
    task_list_manager.reload_tasks()
    return common_return(request)



# -------------------------------------------------
#                Turn On/Off PIN/Device
# -------------------------------------------------
@app.post("/toggle/{pin}")
async def toggle_device(pin: int, request: Request):
    global devices
    for device in devices:
        if device.pin == pin:
            device.toggle()
            break
    #  send the user to index function
    return common_return(request)
    


# -------------------------------------------------
#                      Show Schedule and Tasks
# -------------------------------------------------

def common_response_for_schedule(request):
    current_time = time.strftime("%A %H:%M:%S")
    task_list_manager.add_location_to_tasks(devices)
    return templates.TemplateResponse("set_schedule.html", {"request": request, "devices": devices, 
                                                            "tasks":task_list_manager.tasks, 
                                                            "current_time": current_time})   


@app.get("/schedule", response_class=HTMLResponse)
async def schedule(request: Request):
    # loop though the tasks and match the PIN to the device name
    # use setattribute to add the device name to the task
    # add_location_to_tasks()
    return common_response_for_schedule(request) 

# -------------------------------------------------
#                      Set a  Tasks
# -------------------------------------------------
@app.post("/post_task")
async def set_schedule(request: Request):
    form = await request.form()
    pin = int(form["PIN"])
    day_of_week = form["selected-days"]
    print("Day of week", day_of_week    )
    start_time = form["time-of-day"]
    end_time = form["end-time"]
    
    for device in devices:
        if device.pin == pin:
            task = Task(device.pin, day_of_week, start_time, end_time)
            task_list_manager.add_task(task)
            break
    return common_response_for_schedule(request)
# -------------------------------------------------
# -------------------- Schedule/Task -------------------
#                      DELETE
# -------------------------------------------------
@app.get("/delete_task/{ID}", response_class=HTMLResponse)
async def delete_task(ID: int, request: Request):
    task_list_manager.delete_task(ID)
    return common_response_for_schedule(request)