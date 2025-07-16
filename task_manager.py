
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import *
from apscheduler.schedulers.base import STATE_RUNNING, STATE_PAUSED, STATE_STOPPED


from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import time

from Task_Alliance import Task_Alliance


from apscheduler.executors.pool import ThreadPoolExecutor


from GameController import *
import tkinter as tk

job_name_dic = {}

def get_task_name(task):
    if hasattr(task, '__name__'):
        return task.__name__
    elif hasattr(task, '__class__'):
        return task.__class__.__name__
    else:
        return str(task)

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
        if self.scheduler.state == STATE_PAUSED or self.scheduler.state == STATE_STOPPED:
            log(f"{self.name} 调度器已暂停，设置10s后执行任务")
            self.set_run_time(10)
            return

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
        if type(run_time) == datetime:
            next_run_time = run_time
        else:
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
        self.runtime_list = run_time_list_temp

    def schedule_task_now(self):
        """
        Schedule the task to run at a specific time.
        """
        # Schedule the task to run every 5 minutes
        self.set_run_time(1)
        # self.scheduler.add_job(self.execute_task, trigger='date', run_date=datetime.now(), misfire_grace_time=3600)
    
from adb_controller import ADBController

class AllTaskController:
    def __init__(self, scheduler, user_id=0):
        self.scheduler = scheduler
        self.user_id = user_id
        self.tasks = []
        self.init_tasks()

def get_next_run_times():
    run_times = []
    for job in Job_name_cache.values():
        if Executing_job != job["name"]:
            run_times.append((job["name"], job["next_run_time"]))
    run_times.sort(key=lambda x: x[1])
    return run_times

def get_current_running_jobs():

    running_jobs = []
    for job in submitted_jobs.values():
        running_jobs.append((job, "pending"))
    return running_jobs
    for job in scheduler.get_jobs():
        if job.next_run_time and job.next_run_time <= datetime.now():
            running_jobs.append((job.id, "正在执行"))
    return running_jobs

def update_task_tree(tree):
    for row in tree.get_children():
        tree.delete(row)
    run_times = get_next_run_times()
    running_jobs = get_current_running_jobs()
    shown_ids = set()
    if Executing_job is not None:
        tree.insert("", "end", values=(Executing_job, "Executing"))
    for job_name, status in running_jobs:
        # job_name = job_name_dic.get(job_id,job_id)
        tree.insert("", "end", values=(job_name, status))
        shown_ids.add(job_name)
    for job_name, next_run in run_times:
        if job_name not in shown_ids:
            # job_name = job_name_dic.get(job_id,job_id)
            tree.insert("", "end", values=(job_name, str(next_run)))
            # shown_ids.add(job_id)


def ScheduleAllTask(scheduler,user_id_list=None ):
    if user_id_list is None:
        user_id_list = [0, 10, 12]  # Default user IDs if none provided
    exe_list = []

    # scheduler = BackgroundScheduler(executors=executors)

    for user_id in user_id_list:
        # window_controller = WindowsController()
        window_controller = ADBController(user_id)
        GameController_test = GameController(window_controller)
        # window_controller.active()
        # GameController_test.GoToCity()

        task_executor_new = lambda task,**kwargs: task_executor(scheduler,task,befor=window_controller.active, user_id=user_id,**kwargs)

        game_controller = GameController_test 
        if user_id == 0:
            GoToCxd = None
        else:
            GoToCxd = game_controller.GoToCXD
        GoToCxd = None
        exe = task_executor_new(game_controller.Task_WarehouseRewards,after=GoToCxd)
        game_controller.running_task["Task_WarehouseRewards"] = exe
        exe_list.append(exe)
        exe = task_executor_new(Task_Alliance,arg=game_controller)
        game_controller.running_task["Task_Alliance"] = exe
        exe_list.append(exe)
       
        exe = task_executor_new(game_controller.Task_AdventureRewards)
        game_controller.running_task["Task_AdventureRewards"] = exe
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_collection,after=GoToCxd)
        game_controller.running_task["Task_collection"] = exe
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_Reconnect)
        game_controller.running_task["Task_Reconnect"] = exe
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_train,after=GoToCxd)
        game_controller.running_task["Task_train"] = exe
        exe_list.append(exe)
        exe = task_executor_new(game_controller.Task_HeroRecruit)
        game_controller.running_task["Task_HeroRecruit"] = exe
        exe_list.append(exe)

        if user_id == 10:
            # exe = task_executor_new(game_controller.Task_RefreshAllianceMobilization)
            # game_controller.running_task["Task_RefreshAllianceMobilization"] = exe
            # exe_list.append(exe)
            exe = task_executor_new(game_controller.Task_AttackIceBeast,after=GoToCxd)
            game_controller.running_task["Task_AttackIceBeast"] = exe
            exe_list.append(exe)
            exe = task_executor_new(game_controller.Task_Intelligence,after=GoToCxd)
            game_controller.running_task["Task_Intelligence"] = exe
            exe_list.append(exe)
            game_controller.auto_join_rally = True
            

    try:
        print("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        scheduler.shutdown()


def SetSchedulerAndTaskListWindow():
    global submitted_jobs
    global Job_name_cache
    global Executing_job
    global scheduler
    global running_jobs



    user_id_list = [0,10,12]

    executors = {
    'default': ThreadPoolExecutor(1)  # 限制只能一个任务同时执行
    }
    scheduler = BackgroundScheduler(executors=executors)
    
    
    submitted_jobs = {}
    running_jobs = []
    Job_name_cache = {}
    Executing_job = None

    def job_listener(event):
        global running_jobs
        global Executing_job
        if event.code == EVENT_JOB_SUBMITTED:
            job = scheduler.get_job(event.job_id)  # Ensure the job is registered
            job_name = job.name if job else "Unknown Job"
            job_name = Job_name_cache.pop(event.job_id,"Unknown Job")["name"]
            submitted_jobs[event.job_id] = job_name
            running_jobs.append((event.job_id, job_name))
            Executing_job = running_jobs[0][1] if running_jobs else None
        elif event.code in (EVENT_JOB_EXECUTED, EVENT_JOB_ERROR):
            job = scheduler.get_job(event.job_id)  # Ensure the job is registered
            job_name = job.name if job else "Unknown Job"
            if event.job_id in submitted_jobs:
                del submitted_jobs[event.job_id]
            running_jobs = [(jid, jname) for jid, jname in running_jobs if jid != event.job_id]
            Executing_job = running_jobs[0][1] if running_jobs else None
        elif event.code == EVENT_JOB_REMOVED:
            job = scheduler.get_job(event.job_id)  # Ensure the job is registered

        elif event.code == EVENT_JOB_ADDED:
            job = scheduler.get_job(event.job_id)  # Ensure the job is registered
            job_name = job.name if job else "Unknown Job"
            next_run_time = job.next_run_time if job else "Unknown Time"
            Job_name_cache[event.job_id] = {"name":job_name, "next_run_time": next_run_time}

    scheduler.add_listener(job_listener)

    ScheduleAllTask(scheduler, user_id_list)

    return scheduler


if __name__ == "__main__":

    


    
    root = tk.Tk()
    root.title("任务下次执行时间")

    from tkinter import ttk
    tree = ttk.Treeview(root, columns=("任务ID", "下次执行时间"), show="headings")
    tree.heading("任务ID", text="任务ID")
    tree.heading("下次执行时间", text="下次执行时间")
    tree_pack_opts = {'fill': tk.BOTH, 'expand': True}
    tree.pack(**tree_pack_opts)
    SetSchedulerAndTaskListWindow()
    def refresh_tree():
        update_task_tree(tree)
        root.after(1000, refresh_tree)

    refresh_tree()

    

    root.mainloop()