import random

from functools import partial
# from scheduler import AsyncIOScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from waterproject.wlib.Device import Device

class Task:
    def __init__(self, PIN, days_of_week, start_time, end_time, id=None):
        self.PIN = PIN
        self.days_of_week = days_of_week
        self.start_time = start_time
        self.end_time = end_time
        # make a unique id for the task, random number between 1 and 100000
        self.id = id if id else random.randint(1, 100000)    
            
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
    

    



def days_to_cron_numbers(days):
    # Mapping of days to cron numbers
    # apparently this is NOT WORLKing and is an off by 1. 
    # day_mapping = {
    #     'sunday': 0,
    #     'monday': 1,
    #     'tuesday': 2,
    #     'wednesday': 3,
    #     'thursday': 4,
    #     'friday': 5,
    #     'saturday': 6
    # }
    
    day_mapping = {
        'sunday': 6,
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5
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
