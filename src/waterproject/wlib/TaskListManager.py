
from functools import partial
import json
import os
import platform
import random
import time
    


        
# from scheduler import AsyncIOScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from waterproject.wlib.Device import Device
from waterproject.wlib.Task import Task

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

        
        
class TaskListManager:
    # hold a list of task
    # allow adding, deleting, and updating tasks
    # read and write the tasks to using the load and write schedule functions
    def __init__(self, tasks: list[Task]=[], 
                 load_from_file=True, devices: list[Device]=None , 
                 file_path='schedule.json'):
        self.tasks = tasks
        self.file_path = file_path
        assert devices is not None, "Devices must be provided"
        self.devices = devices
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.scheduler.start()
        if load_from_file:
            self.reload_tasks()
            
            
    def add_task(self, task: Task, write_to_file=True):
        """Add and write a task to the schedule"""
        task.add_task_to_schedule(self.scheduler, self.devices)
        self.tasks.append(task)
        if write_to_file:
            self.write_schedule()
        
    def delete_task(self, task_id: int):
        """Delete a task from the schedule"""
        for task in self.tasks:
            if task.ID == task_id:
                task.remove_task_from_schedule()
                self.tasks.remove(task)
                self.write_schedule()
                break
    
    def reload_tasks(self):
        """REad the schedule from the file
        and load it into the tasks list"""
        if not os.path.exists(self.file_path):
            print("No schedule file found")
            self.tasks = []
            return 

        with open(self.file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error loading schedule file")
                self.tasks = []
                return
                
        # zero out the task list
        self.tasks = []
        for task_data in data:
            task = Task(
                PIN=task_data["PIN"],
                days_of_week=task_data["days_of_week"],
                start_time=task_data["start_time"],
                end_time=task_data["end_time"],
                id=task_data["id"]
                
            )
            self.add_task(task, write_to_file=False)
        
        
    def write_schedule(self):   
        """Write the schedule to the file"""
        # _write_schedule(self.tasks)    
        data = []
        for task in self.tasks:
            data.append({
                "PIN": task.PIN,
                "days_of_week": task.days_of_week,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "id": task.ID
            })
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print("Wrote schedule to file")
        
        
    def add_location_to_tasks(self, devices: list[Device]):
        for task in self.tasks:
            for device in devices:
                if device.pin == task.PIN:  
                    if task.PIN == device.pin:
                        setattr(task, "location", device.location)
                        break