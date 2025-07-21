from Task import GameTask

class MercenaryPrestigeTask(GameTask):
    def __init__(self, game_controller, run_times=10):
        super().__init__("MercenaryPrestige", game_controller)
        self.config["MaxRunTimes"] = run_times  # 设置最大运行次数
        self.config["TodayRunTimes"] = 0  # 初始化今天运行次数

    def exe(self):

        for i in range(5):
            window = self.game_controller.GetWindow(f"MercenaryPrestige_Step{i+1}")
            
            if i == 4:
                cool_down = window.GetCoolDownTime(default_cool_down_time=60)
                cool_down *= 2
                
            window.open()
        if self.config["TodayRunTimes"] >= self.config["MaxRunTimes"]:
            cool_down = 24 * 60 * 60  # 如果今天剩余次数大于最大运行次数，设置冷却时间为24小时
        return cool_down
    

def ScehduleMercenaryPrestigeTask():
    from GameController import GameController
    game_controller = GameController()
    task = MercenaryPrestigeTask(game_controller)
    
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    from task_manager import task_executor
    exe = task_executor(scheduler, task)
    game_controller.running_task["MercenaryPrestige"] = exe

    return scheduler

if __name__ == "__main__":

    scheduler = ScehduleMercenaryPrestigeTask()
    scheduler.start()
    try:
        while True:
            pass  # Keep the script running to allow the scheduler to run tasks
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

