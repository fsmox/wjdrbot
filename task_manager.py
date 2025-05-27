
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import time


from apscheduler.executors.pool import ThreadPoolExecutor

class task_executor:
    def __init__(self,scheduler, task, arg=None,befor=None, after=None):
        self.scheduler = scheduler
        self.befor = befor
        self.after = after
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
            if self.befor is not None:
                self.befor()
            if self.arg is not None:
                count_down = self.task(self.arg)
            else:
                count_down = self.task()
            if not self.after is None:
                self.after()
            self.fail_count = 0
        except Exception as e:
            print(f"Error executing task: {e}")
            self.fail_count += 1
            if self.fail_count >= self.max_fail_count:
                print(f"Task failed {self.fail_count} times. Stopping execution.")
                return
            else:
                count_down = 60 * 2 * self.fail_count  # Increase the countdown time exponentially
        if type(count_down) == list:
            for time in count_down:
                next_run_time = datetime.now() + timedelta(seconds=count_down)
                print(f"Next run time: {next_run_time}")
                # Schedule the next run
                self.scheduler.add_job(self.execute_task, trigger='date', run_date=next_run_time, misfire_grace_time=20*60)
        else:
            next_run_time = datetime.now() + timedelta(seconds=count_down)
            print(f"Next run time: {next_run_time}")
            # Schedule the next run
            self.scheduler.add_job(self.execute_task, trigger='date', run_date=next_run_time, misfire_grace_time=20*60)

    def schedule_task_now(self):
        """
        Schedule the task to run at a specific time.
        """
        # Schedule the task to run every 5 minutes
        self.scheduler.add_job(self.execute_task, trigger='date', run_date=datetime.now(), misfire_grace_time=3600)
    
from adb_controller import ADBController

if __name__ == "__main__":
    from GameController import *
    user_id_list = [10,12]
    Run_num = 1
    exe_list = []
    executors = {
    'default': ThreadPoolExecutor(1)  # 限制只能一个任务同时执行
    }
    scheduler = BackgroundScheduler(executors=executors)


    for user_id in user_id_list:
        # window_controller = WindowsController()
        window_controller = ADBController(user_id)
        GameController_test = GameController(window_controller)
        GameController_test.GoToCity()

        task_executor_new = lambda task,**kwargs: task_executor(scheduler,task,befor=window_controller.active, **kwargs)

        game_controller = GameController_test 
        GoToCxd = game_controller.GoToCXD
        exe = task_executor_new(game_controller.Task_WarehouseRewards,after=GoToCxd)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_AllianceTechnology)
        exe_list.append(exe)
        # exe = task_executor(scheduler,game_controller.Task_RefreshAllianceMobilization,GoToCXD=GoToCxd)
        # exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_AdventureRewards)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_collection,after=GoToCxd)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_Reconnect)
        exe_list.append(exe)

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
