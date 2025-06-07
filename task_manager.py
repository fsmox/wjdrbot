
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import time


from apscheduler.executors.pool import ThreadPoolExecutor

job_name_dic = {}

class task_executor:
    def __init__(self,scheduler, task, arg=None,user_id=0,befor=None, after=None):

        self.scheduler = scheduler
        self.befor = befor
        self.after = after
        self.task = task
        self.arg = arg

        self.fail_count = 0
        self.max_fail_count = 5
        self.job_count = 0
        self.Job_id_list = []
        self.runtime_list = []
        self.name=self.get_task_name()
        self.name = f"{self.name}_{user_id}"
        self.schedule_task_now()

    def get_task_name(self):
        if hasattr(self.task, '__name__'):
            return self.task.__name__
        elif hasattr(self.task, '__class__'):
            return self.task.__class__.__name__
        else:
            return str(self.task)

    def execute_task(self):
        """
        Execute the task immediately.
        """
        count_down = 5*60
        self.job_count -= 1
        Info(f"{self.name}开始执行")
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
            logger.error(f"Error executing task: {e}")
            self.fail_count += 1
            if self.fail_count >= self.max_fail_count:
                logger.error(f"Task failed {self.fail_count} times. Stopping execution.")
                return
            else:
                count_down = 60 * 2 * self.fail_count  # Increase the countdown time exponentially
        if type(count_down) == list:
            for time in count_down:
                self.set_run_time(time)
        else:
            self.set_run_time(count_down)
        if self.job_count == 0:
            self.set_run_time(5*60)
        Info(f"{self.name}执行结束")
    def set_run_time(self,run_time):
        now = datetime.now()
        next_run_time = now + timedelta(seconds=run_time)
        run_time_list_temp = []
        min_space = timedelta(hours=1)
        for run_time in self.runtime_list:
            if run_time > now:
                run_time_list_temp.append(run_time)
                space = abs(next_run_time - run_time) 
                min_space = min(min_space,space) 

        if min_space < timedelta(minutes=10):
            log(f"{self.name} skip Next run time: {next_run_time}")
        else:
            run_time_list_temp.append(next_run_time)
            log(f"{self.name} Next run time: {next_run_time}")
            job = self.scheduler.add_job(self.execute_task, trigger='date', name=self.name,run_date=next_run_time, misfire_grace_time=3600)
            # jod_id = job.id
            # job_name_dic[jod_id] = self.name
            self.job_count += 1
            update_task_window()
        self.runtime_list = run_time_list_temp

    def schedule_task_now(self):
        """
        Schedule the task to run at a specific time.
        """
        # Schedule the task to run every 5 minutes
        self.set_run_time(0)
        # self.scheduler.add_job(self.execute_task, trigger='date', run_date=datetime.now(), misfire_grace_time=3600)
    
from adb_controller import ADBController


def get_next_run_times():
    run_times = []
    for job in scheduler.get_jobs():
        if job.pending:
            run_times.append((job.name, "pending"))
        else:
            run_times.append((job.name, job.next_run_time))
    return run_times

def get_current_running_jobs():

    running_jobs = []
    return running_jobs
    for job in scheduler.get_jobs():
        if job.next_run_time and job.next_run_time <= datetime.now():
            running_jobs.append((job.id, "正在执行"))
    return running_jobs

def update_task_window():
    for row in tree.get_children():
        tree.delete(row)
    run_times = get_next_run_times()
    running_jobs = get_current_running_jobs()
    shown_ids = set()
    for job_name, status in running_jobs:
        # job_name = job_name_dic.get(job_id,job_id)
        tree.insert("", "end", values=(job_name, status))
        shown_ids.add(job_name)
    for job_name, next_run in run_times:
        if job_name not in shown_ids:
            # job_name = job_name_dic.get(job_id,job_id)
            tree.insert("", "end", values=(job_name, str(next_run)))
            # shown_ids.add(job_id)
    # for job_id in list(job_name_dic.keys()):
    #     job_id = str(job_id)
    #     if scheduler.get_job(job_id) is None:
    #         del job_name_dic[job_id]
    # root.after(2000, update_task_window)


runtimes = 0
def TestFunc():
    print("TestFunc is running")
    time.sleep(2)
    print("TestFunc finished")

    global runtimes

    runtimes += 1
    if runtimes == 1:
        return [1,2,3,4,5]
    else:
        return []

if __name__ == "__main__":
    from GameController import *
    import tkinter as tk
    from tkinter import ttk

    
    root = tk.Tk()
    root.title("任务下次执行时间")
    tree = ttk.Treeview(root, columns=("任务ID", "下次执行时间"), show="headings")
    tree.heading("任务ID", text="任务ID")
    tree.heading("下次执行时间", text="下次执行时间")
    tree.pack(fill=tk.BOTH, expand=True)


    user_id_list = [0,10,12]
    Run_num = 1
    exe_list = []
    executors = {
    'default': ThreadPoolExecutor(1)  # 限制只能一个任务同时执行
    }
    scheduler = BackgroundScheduler(executors=executors)
    # test = task_executor(scheduler, TestFunc)


    for user_id in user_id_list:
        # window_controller = WindowsController()
        window_controller = ADBController(user_id)
        GameController_test = GameController(window_controller)
        window_controller.active()
        GameController_test.GoToCity()

        task_executor_new = lambda task,**kwargs: task_executor(scheduler,task,befor=window_controller.active, user_id=user_id,**kwargs)

        game_controller = GameController_test 
        if user_id == 0:
            GoToCxd = None
        else:
            GoToCxd = game_controller.GoToCXD

        GoToCxd = None
        exe = task_executor_new(game_controller.Task_WarehouseRewards,after=GoToCxd)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_Alliance)
        exe_list.append(exe)
        # exe = task_executor(scheduler,game_controller.Task_RefreshAllianceMobilization,GoToCXD=GoToCxd)
        # exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_AdventureRewards)
        exe_list.append(exe)
        # exe = task_executor_new(game_controller.Task_collection,after=GoToCxd)
        # exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_Reconnect)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_train,after=GoToCxd)
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_HeroRecruit)
        exe_list.append(exe)
        if user_id == 10:
            exe = task_executor_new(game_controller.Task_AttackIceBeast,after=GoToCxd)
            exe_list.append(exe)
            exe = task_executor_new(game_controller.Task_Intelligence,after=GoToCxd)
            exe_list.append(exe)

    try:
        print("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        scheduler.shutdown()

    # # 保持运行
    # try:
    #     while True:
    #         pass
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()

    # Uncomment the following lines to test the second task
    # executor_2 = task_executor(test_task_2)
    # executor_2.start()



    # update_task_window()
    root.mainloop()