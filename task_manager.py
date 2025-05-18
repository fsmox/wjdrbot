
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import time


from apscheduler.executors.pool import ThreadPoolExecutor

class task_executor:
    def __init__(self,scheduler, task, arg=None):
        self.scheduler = scheduler
        self.task = task
        self.arg = arg
        self.schedule_task_now()
        self.fail_count = 0
        self.max_fail_count = 5
    def execute_task(self):
        """
        Execute the task immediately.
        """
        
        try:
            if self.arg is not None:
                count_down = self.task(self.arg)
            else:
                count_down = self.task()
            self.fail_count = 0
        except Exception as e:
            print(f"Error executing task: {e}")
            self.fail_count += 1
            if self.fail_count >= self.max_fail_count:
                print(f"Task failed {self.fail_count} times. Stopping execution.")
                return
            else:
                count_down = 60 * 2 * self.fail_count  # Increase the countdown time exponentially
            
        next_run_time = datetime.now() + timedelta(seconds=count_down)
        print(f"Next run time: {next_run_time}")
        # Schedule the next run
        self.scheduler.add_job(self.execute_task, trigger='date', run_date=next_run_time, misfire_grace_time=3600)

    def schedule_task_now(self):
        """
        Schedule the task to run at a specific time.
        """
        # Schedule the task to run every 5 minutes
        self.scheduler.add_job(self.execute_task, trigger='date', run_date=datetime.now(), misfire_grace_time=3600)
    


if __name__ == "__main__":
    from GameController import *

    window_controller = WindowsController()
    GameController_test = GameController(window_controller)
    window_controller2 = WindowsController()
    GameController_test2 = GameController(window_controller2)
    exe_list = []


    # GameWindows1 = RegisterWindow(GameWindows_test,window_controller=window_controller)
    GameController_test.GoToCity()
    # GameWindows2 = RegisterWindow(GameWindows_test,window_controller=window_controller2)
    GameController_test2.GoToCity()
    # Create a scheduler instance
    executors = {
    'default': ThreadPoolExecutor(1)  # 限制只能一个任务同时执行
    }
    scheduler = BackgroundScheduler(executors=executors)
    # Create an instance of the task_executor with the test_task

    
    game_controller = GameController_test 
    executor_Task_WarehouseRewards = task_executor(scheduler,game_controller.Task_WarehouseRewards)
    exe_list.append(executor_Task_WarehouseRewards)
    exe = task_executor(scheduler,game_controller.Task_AllianceTechnology)
    exe_list.append(exe)
    exe = task_executor(scheduler,game_controller.Task_RefreshAllianceMobilization)
    exe_list.append(exe)
    exe = task_executor(scheduler,game_controller.Task_AdventureRewards)
    exe_list.append(exe)

    game_controller = GameController_test2
    executor_Task_WarehouseRewards = task_executor(scheduler,game_controller.Task_WarehouseRewards)
    exe_list.append(executor_Task_WarehouseRewards)
    exe = task_executor(scheduler,game_controller.Task_AllianceTechnology)
    exe_list.append(exe)
    exe = task_executor(scheduler,game_controller.Task_RefreshAllianceMobilization)
    exe_list.append(exe)
    exe = task_executor(scheduler,game_controller.Task_AdventureRewards)
    exe_list.append(exe)
    # Start the scheduler
    try:
        print("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        scheduler.shutdown()

    # 保持运行
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

    # Uncomment the following lines to test the second task
    # executor_2 = task_executor(test_task_2)
    # executor_2.start()
