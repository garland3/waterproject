from functools import partial
import json
import os
import platform
import random
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
computer_name = platform.node()
# print(computer_name)
if computer_name!="DESKTOP-7DC3UA9":
    import RPi.GPIO as GPIO
else:
    from myfake import GPIO
    
log_file = "log.csv"
    
def days_to_cron_numbers(days):
    # Mapping of days to cron numbers
    day_mapping = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6
    }
    
    # Split the input string and map the days to their numbers
    day_list = days.lower().split(',')
    # convert to int and add to a list
    # sort
    # convert to string
    # cron_numbers = [str(day_mapping[day.strip()]) for day in day_list if day.strip() in day_mapping]
    cron_numbers_int_list = [day_mapping[day.strip()] for day in day_list if day.strip() in day_mapping]
    cron_numbers_int_list.sort()
    cron_numbers = [str(day) for day in cron_numbers_int_list]
    
    # Join the numbers into a comma-separated string
    return ','.join(cron_numbers)


class Task:
    def __init__(self, PIN, days_of_week, start_time, end_time, id=None):
        self.PIN = PIN
        self.days_of_week = days_of_week
        self.start_time = start_time
        self.end_time = end_time
        # make a unique ID for the task, random number between 1 and 100000
        if id:
            self.ID = id
        else:
            self.ID = random.randint(1, 100000)
            
        self.scheduler_job_on = None
        self.scheduler_job_off = None

    def __repr__(self):
        return (f"Task(PIN='{self.PIN}', days_of_week={self.days_of_week}, "
                f"start_time='{self.start_time}', end_time='{self.end_time}')")


    def cron_days(self):
        return days_to_cron_numbers(self.days_of_week)
    
    def cron_start_time_hour(self):
        """return the int hour of the start time"""
        return int(self.start_time.split(":")[0])
    
    def cron_start_time_minute(self):
        """return the int minute of the start time"""
        return int(self.start_time.split(":")[1])
    
    def cron_end_time_hour(self):
        """return the int hour of the end time"""
        return int(self.end_time.split(":")[0])
    
    def cron_end_time_minute(self):   
        """return the int minute of the end time"""
        return int(self.end_time.split(":")[1])
    
    def add_task_to_schedule(self,scheduler: AsyncIOScheduler, devices: list):
        """Add the task to the scheduler"""
        for device in devices:
            if device.pin == self.PIN:
                fn_set_state_on = partial( device.set_state, 1)
                
                cron_days = self.cron_days()
                cron_start_time_hour = self.cron_start_time_hour()
                cron_start_time_minute = self.cron_start_time_minute()
                cron_end_time_hour = self.cron_end_time_hour()
                cron_end_time_minute = self.cron_end_time_minute()
                self.scheduler_job_on = scheduler.add_job(
                   fn_set_state_on,
                    'cron',
                    day_of_week=cron_days,
                    hour=cron_start_time_hour,
                    minute=cron_start_time_minute,
                    replace_existing=True
                )
                # use the vars above to print out. 
                print(f"Added job ON {self.PIN}, cron_days={cron_days}, cron_start_time_hour={cron_start_time_hour}, cron_start_time_minute={cron_start_time_minute}, cron_end_time_hour={cron_end_time_hour}, cron_end_time_minute={cron_end_time_minute}")
                                
                fn_set_state_off = partial( device.set_state, 0)
                self.scheduler_job_off = scheduler.add_job(
                    fn_set_state_off,
                    'cron',
                    day_of_week=cron_days,
                    hour=cron_end_time_hour,
                    minute=cron_end_time_minute,
                    replace_existing=True
                )
                break   
            
    def remove_task_from_schedule(self):
        """Remove the task from the scheduler"""
        if self.scheduler_job_on:
            self.scheduler_job_on.remove()
            print(f"Removed job ON {self.ID}, {self.PIN}, {self.days_of_week}, {self.start_time}, {self.end_time}")
        if self.scheduler_job_off:
            self.scheduler_job_off.remove()                
            print(f"Removed job OFF {self.ID}, {self.PIN}, {self.days_of_week}, {self.start_time}, {self.end_time}")
            
            
            
    
    

class Device:
    def __init__(self, name, pin, location):
        self.name = name
        self.pin = pin
        self.location = location
        self.state = False
        self.turn_on_times=[]
        self.turn_off_times=[]
        
    def set_state(self, state:int):
        """State must be an int of 0 or 1, 0 is off, 1 is on"""
        
        self.state = state
        if self.state  ==0:
            value = GPIO.LOW 
        elif self.state ==1:
            value = GPIO.HIGH
        else:
            raise ValueError("Invalid state")
        
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
        GPIO.output(self.pin, GPIO.LOW if self.state else GPIO.HIGH)
        self.write_log()
            

devices = [
    Device("power_cable_solenoid", 12, "Top of Water Containers"),
    Device("valve_1", 25, "Middle Garden"),
    Device("valve_2", 23, "Rock Wall Garden"),
    Device("valve_3", 18, "Grape Garden"),
]


# Setup GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for device in devices:
        GPIO.setup(device.pin, GPIO.OUT)
        GPIO.output(device.pin, GPIO.HIGH)  # Ensure all pins are off initially
        





        
        
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
            self.tasks = []
            return 

        with open(self.file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error loading schedule file")
                self.tasks = []
                return
                
                
        tasks = []
        for task_data in data:
            task = Task(
                PIN=task_data["PIN"],
                days_of_week=task_data["days_of_week"],
                start_time=task_data["start_time"],
                end_time=task_data["end_time"],
                id=task_data["id"]
                
            )
            self.add_task(task, write_to_file=False)
        
        self.tasks = tasks
        
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