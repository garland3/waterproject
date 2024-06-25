
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from waterproject.wlib.Device import Device
from waterproject.wlib.Task import Task
from functools import partial

class TaskInterface:
    def __init__(self, scheduler: AsyncIOScheduler, devices: list[Device]):
        self.scheduler = scheduler
        self.devices = devices

    def add_task(self, task: Task):
        """Add the task to the scheduler"""
        for device in self.devices:
            if device.pin == task.PIN:
                fn_set_state_on = partial(device.set_state, state_int=1)
                cron_days = task.cron_days()
                cron_start_time_hour = task.cron_start_time_hour()
                cron_start_time_minute = task.cron_start_time_minute()
                cron_end_time_hour = task.cron_end_time_hour()
                cron_end_time_minute = task.cron_end_time_minute()
                task.scheduler_job_on = self.scheduler.add_job(
                    fn_set_state_on,
                    'cron',
                    day_of_week=cron_days,
                    hour=cron_start_time_hour,
                    minute=cron_start_time_minute,
                    replace_existing=True
                )
                print(f"Added job ON {task.PIN}, cron_days={cron_days}, cron_start_time_hour={cron_start_time_hour}, cron_start_time_minute={cron_start_time_minute}, cron_end_time_hour={cron_end_time_hour}, cron_end_time_minute={cron_end_time_minute}")
                
                fn_set_state_off = partial(device.set_state, state_int=0)
                task.scheduler_job_off = self.scheduler.add_job(
                    fn_set_state_off,
                    'cron',
                    day_of_week=cron_days,
                    hour=cron_end_time_hour,
                    minute=cron_end_time_minute,
                    replace_existing=True
                )
                break
            
    def remove_task(self, task: Task):
        """Remove the task from the scheduler"""
        if task.scheduler_job_on:
            task.scheduler_job_on.remove()
            print(f"Removed job ON {task.id}, {task.PIN}, {task.days_of_week}, {task.start_time}, {task.end_time}")
        if task.scheduler_job_off:
            task.scheduler_job_off.remove()
            print(f"Removed job OFF {task.id}, {task.PIN}, {task.days_of_week}, {task.start_time}, {task.end_time}")