from GlobalConfig import *
from adb_controller import ADBController
from logger import log,Info,logger
import os
import threading
import time
import yaml
from ImageJudge import ImageJudge


class GameWindow:
    def __init__(self,window_name,open_config,in_window_config,cool_down_config, windwow_controller: ADBController):
        self.windwow_controller = windwow_controller
        self.window_name = window_name
        self.father_window = None
        self.child_windows = {}
        self.open_config = open_config
        self.in_window_config = in_window_config
        self.cool_down_config = cool_down_config
        self.open_XY = (open_config["defult_click_point"]["x"],open_config["defult_click_point"]["y"]) if not open_config  is None else None

    def CurrentWindowIsMe(self,enable_cache=True):
        """判断当前窗口是否是我"""

        judge = ImageJudge(self.in_window_config,f"{self.window_name}_in_window")
        # 检查当前窗口是否是我
        # 获取屏幕截图
        screenshot = lambda *agr,**keyword: self.windwow_controller.screenshot(enable_cache,*agr,**keyword)
        existed,x,y = judge.Existed(screenshot)
        self.windwow_controller.op_judge_ok = True
        self.judge_point = (x,y)
        return existed

    def ClikReturnButton(self, task_name=None):
        window_name = "return_button"
        in_window_config_file = f"images/{window_name}_config.yaml"
        with open(in_window_config_file, 'r', encoding='utf-8') as f:
            in_window_config = yaml.safe_load(f)
            in_window_config["config_file"] = in_window_config_file
        # return_button = GameWindow(window_name, None, in_window_config, None, self.windwow_controller)
        judge = ImageJudge(in_window_config,f"{self.window_name}_in_window")
        screenshot = self.windwow_controller.screenshot
        existed,x,y = judge.Existed(screenshot)
        if existed:
            log(f"点击{window_name}按钮")
            self.windwow_controller.tap(x,y)
            
            return True
        else:
            log(f"{window_name}按钮不存在")
            return False
    
    def GetDefultClickPoint(self):
        """获取默认点击点"""
        if self.open_config is None:
            return None
        if "defult_click_point" in self.open_config:
            return self.open_config["defult_click_point"]
        else:
            return None

    def CurrentWindowIsFather(self):
        """判断当前窗口是否是父窗口"""
        if self.father_window is None:
            return False
        return self.father_window.CurrentWindowIsMe()

    def GetCoolDownTime(self,default_cool_down_time=60 * 10):
        """获取冷却时间"""
        if self.cool_down_config is None:
            return default_cool_down_time # 默认冷却时间为10分钟
        # 获取屏幕截图
        container = [None]
        screen = self.windwow_controller.screenshot(enable_cache=False,container=container)
        # 检查屏幕截图是否有效
        if screen is None or screen.size == 0:
            log("获取屏幕截图失败")
            return default_cool_down_time # 默认冷却时间为10分钟
        
        judge = ImageJudge(self.cool_down_config)
        total_seconds = judge.get_countdown_time(screen,original_screen=container[0])

        return total_seconds if total_seconds is not None else default_cool_down_time
        # 获取冷却时间的逻辑

    def check_open_window(self):
        judge = ImageJudge(self.open_config,f"{self.window_name}_open")

        if judge.method == "swipe_check" or judge.method == "swipe_find":
            for i in range(3):
                log(f"第{i+1}次检查{self.window_name}窗口")
                existed,x,y = judge.Existed(self.windwow_controller.screenshot)
                if existed:
                    break
                start_x = self.open_config["swipe"]["start"]["x"]
                start_y = self.open_config["swipe"]["start"]["y"]
                end_x = self.open_config["swipe"]["end"]["x"]
                end_y = self.open_config["swipe"]["end"]["y"]
                duration = self.open_config["swipe"]["duration"]
                self.windwow_controller.swipe(start_x, start_y, end_x, end_y, duration)
                time.sleep(1)
                # 先滑动到窗口位置
            if not existed:
                existed,x,y = judge.Existed(self.windwow_controller.screenshot)
        elif judge.method == "None":
            existed,x,y = judge.Existed(self.windwow_controller.screenshot)
        else:
            existed,x,y = judge.Existed(self.windwow_controller.screenshot)

        return existed, x, y
    def open(self):
        # # 打开游戏窗口的逻辑
        # if not self.CurrentWindowIsFather():
        #     log("当前窗口不是父窗口，无法打开游戏窗口")
        #     return False

        if self.open_config is None:
            raise Exception(f"未配置 {self.window_name} 的 open_config，无法打开窗口")


        existed, x, y = self.check_open_window()
        if self.in_window_config is None:
            if existed:
                self.windwow_controller.tap(x,y)
                self.open_XY =(x,y)
                time.sleep(0.5)
                return True
            else:
                return False

        if not existed:
            if self.CurrentWindowIsMe(enable_cache=False):
                return True
            else:
                log(f"没检测到{self.window_name}窗口打开图标，无法打开{self.window_name}窗口")
                return False
        
        self.windwow_controller.tap(x,y)
        self.open_XY =(x,y)
        for i in range(Operation_interval):
            log(f"第{i+1}次检查游戏窗口")
            task_found = self.CurrentWindowIsMe(enable_cache=False)
            if i == Operation_interval // 2:
                existed, x, y = self.check_open_window()
                if existed:
                    self.windwow_controller.tap(x,y)
            if task_found:
                log(f"{self.window_name}窗口已打开")
                return True
            # time.sleep(0.5)
            
        return False
        

    def return_to_father_window(self):
        pass


    

def RegisterWindow(windows_config,window_controller=None,GameWindows=None):
    """注册窗口"""
    if GameWindows is None:
        GameWindows = {}

    if window_controller is None:
        window_controller = ADBController()
    for window_name,config in windows_config.items():
        in_window_config = f"images/{window_name}_window_config.yaml"
        open_config = f"images/{window_name}_open_config.yaml"
        cool_down_config = f"images/{window_name}_cool_down_config.yaml"
        if not config  is None:
            in_window_config = config.get("in_window_config",in_window_config)
            open_config = config.get("open_config",open_config)

        if os.path.exists(in_window_config):
            with open(in_window_config, 'r', encoding='utf-8') as f:
                in_window_config_obj = yaml.safe_load(f)
                in_window_config_obj["config_file"] = in_window_config
        else:
            in_window_config_obj = None
        if os.path.exists(open_config):
            with open(open_config, 'r', encoding='utf-8') as f:
                open_config_obj = yaml.safe_load(f)
                open_config_obj["config_file"] = open_config
        else:
            open_config_obj = None
            
        if os.path.exists(cool_down_config):
            with open(cool_down_config, 'r', encoding='utf-8') as f:
                cool_down_config_obj = yaml.safe_load(f)
                cool_down_config_obj["config_file"] = cool_down_config
        else:
            cool_down_config_obj = None
        GameWindows[window_name] = GameWindow(window_name,open_config_obj,in_window_config_obj,cool_down_config_obj,window_controller)


    return GameWindows

