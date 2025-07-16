from __future__ import annotations
import yaml
import datetime
import os
class GameTask:
    from GameController import GameController
    def __init__(self, name:str, game_controller:GameController, config_file=None):
        self.name = name
        self.game_controller = game_controller
        self.func = None
        
        if config_file is None:
            config_file = f"config/{self.name}_{self.game_controller.windwow_controller.user_id}.yaml"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_file} 未找到，使用默认配置。")
            self.config = {
                "LastRunTime": None,
                "NextRunTime": None,
                "TodayRunTimes": 0,
                "TodyRemainingTimes": None,
            }
        self.config_file = config_file


    def Before(self):
        if self.game_controller.InReconnectWindow():
            return False  # 如果在重连窗口中，返回False，表示不执行任务
        else:
            return True  # 如果不在重连窗口中，返回True，表示可以执行任务

    def exe(self):
        if self.func is None:
            raise NotImplementedError("You must implement the exe method in the subclass.")
        else:
            return self.func(self.game_controller)

    def After(self):
        self.config["TodayRunTimes"] += 1
        # 更新配置文件
        
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)

    def __call__(self):
        now = datetime.datetime.now()
        last_run_time = self.config.get("LastRunTime", None)
        if last_run_time:
            last_run_dt = datetime.datetime.strptime(last_run_time, "%Y-%m-%d %H:%M:%S")
            today_1am = now.replace(hour=1, minute=0, second=0, microsecond=0)
            if now.hour < 1:
                NewDay = False
            else:
                NewDay = last_run_dt < today_1am
        else:
            NewDay = True
        if NewDay:
            self.config["TodayRunTimes"] = 0
            self.config["TodyRemainingTimes"] = self.config.get("MaxRunTimes", 99)
        self.config["LastRunTime"] = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if not self.Before():
            return 5*60  # 如果Before方法返回False，表示任务不执行，返回冷却时间5分钟
        result = self.exe()
        self.After()
        return result
