# conda activate waterproject
import platform
import time
computer_name = platform.node()
print(computer_name)

import subprocess
from fastapi import FastAPI, Request, Response
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

def common_return(request, message = None):
    # get the  day of the week  and time to the second and add it to the context
    current_time = time.strftime("%A %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices, "current_time": current_time, "message": message})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return common_return(request)
    
# show log
@app.get("/log_download")
async def log_download():
    return FileResponse(log_file, filename=log_file, media_type='text/csv')

@app.get("/log_display")
async def log_display():
    with open(log_file, 'r') as f:
        log_content = f.read()
    html_content = f"<html><body><pre>{log_content}</pre></body></html>"
    return HTMLResponse(content=html_content, media_type="text/html")

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

def common_response_for_schedule(request, existing_task = None):
    current_time = time.strftime("%A %H:%M:%S")
    task_list_manager.add_location_to_tasks(devices)
    return templates.TemplateResponse("set_schedule.html", {"request": request, "devices": devices, 
                                                            "tasks":task_list_manager.tasks, 
                                                            "current_time": current_time, 
                                                            'existing_task': existing_task})   


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
@app.get("/delete_task/{id}", response_class=HTMLResponse)
async def delete_task(id: int, request: Request):
    task_list_manager.delete_task(id)
    return common_response_for_schedule(request)


# ----------- EDIT TASK ----------- NOT FINISHED
@app.get("/edit_task/{id}", response_class=HTMLResponse)
async def delete_task(id: int, request: Request):
    # delete the existing task and then add a new one
    task_list_manager.delete_task(id)
    return common_response_for_schedule(request)
    # common_response_for_schedule(request) 




# ------------------------------------------------- Do a git pull. EAsier than logging in to the raspberry pi on terminal
@app.get("/update_code")
async def update_code(request: Request):
    try:
        r = subprocess.run(["git", "pull", "origin", 'main'], check=True)
        response = ""
        if r.stderr:
            response += r.stderr.decode('utf-8')
        if r.stdout:
            response += r.stdout.decode('utf-8')
        # return Response(status_code=200, content="Code updated successfully.")
        return common_return(request, message=f"Process completed successfully: {response}. Server will restart")
    except subprocess.CalledProcessError as e:
        return Response(status_code=500, content=f"Error updating code: {e}")
