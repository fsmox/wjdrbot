from GlobalConfig import *
from windows_controller import WindowsController
from logger import log,Info,logger
import cv2
from datetime import datetime, timedelta
import os
import threading
import time
import yaml
import pytesseract
from enum import Enum

from GameWindow import GameWindow,RegisterWindow

lock = threading.Lock()

config_base_high = 900
config_base_width = 506

config_reconnect ={
    "picture_path": "images/reconnect.png",
    "threshold":0.8,
}
config_popup = {
    "picture_path": "images/close_popup.png",
    "threshold": 0.8,
}
left = 430
top = 820
width = 56
height = 76
region_city = {
          "left": 430 , # 左边界X坐标
          "top": 820 , # 上边界Y坐标
          "right": 430+56 ,# 右边界X坐标
          "bottom": 820+70 ,# 下边界Y坐标 
            }

config_city = {
    "picture_path": "images/city.png",
    "region": region_city,
    "threshold": 0.8,
    }

left = 430
top = 820
width = 56
height = 76
region_world = {
        "left": 430, # 左边界X坐标
        "top": 820, # 上边界Y坐标
        "right": 430+56,# 右边界X坐标
        "bottom": 820+76,# 下边界Y坐标 
                }
config_world = {
    "picture_path": "images/world.png",
    "region": region_world,
    "threshold": 0.8,
    }
left = 446
top = 92
width = 46
height = 46
region_RutineTask = {
          "left": 446 , # 左边界X坐标
          "top": top , # 上边界Y坐标
          "right": left+width ,# 右边界X坐标
          "bottom": top+height ,# 下边界Y坐标 
            }
config_RoutineTask = {
    "defult_location": {
        "x": left+width//2,
        "y": top+height//2, 
    },
    "picture_path": "images/routine_task.png",
    "threshold": 0.8,
}

file_name = "routine_task_return"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_RutineTask_return = yaml.safe_load(f)
config_RutineTask_return = {
    "defult_location": {    
        "x": region_RutineTask_return["defult_location"]["x"],
        "y": region_RutineTask_return["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.8,
    "region": region_RutineTask_return,
}

file_name = "alliance_mobilization"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_alliance_mobilization = yaml.safe_load(f)
config_alliance_mobilization = {
    "defult_location": {    
        "x": region_alliance_mobilization["defult_location"]["x"],
        "y": region_alliance_mobilization["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.7,
    "region": region_alliance_mobilization,
}

file_name = "alliance_mobilization_window"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_alliance_mobilization_window = yaml.safe_load(f)
config_alliance_mobilization_window = {
    "defult_location": {    
        "x": region_alliance_mobilization_window["defult_location"]["x"],
        "y": region_alliance_mobilization_window["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.7,
    "region": region_alliance_mobilization_window,
}

file_name = "Zdy_left"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_Zdy_left = yaml.safe_load(f)
config_Zdy_left = {
    "defult_location": {    
        "x": region_Zdy_left["defult_location"]["x"],
        "y": region_Zdy_left["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.6,
    "region": region_Zdy_left,
}
file_name = "Zdy_right"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_Zdy_right = yaml.safe_load(f)
config_Zdy_right = {
    "defult_location": {    
        "x": region_Zdy_right["defult_location"]["x"],
        "y": region_Zdy_right["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.6,
    "region": region_Zdy_right,
}

file_name = "refresh_task_button"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_refresh_task_button = yaml.safe_load(f)

config_refresh_task_button = {
    "defult_location": {    
        "x": region_refresh_task_button["defult_location"]["x"],
        "y": region_refresh_task_button["defult_location"]["y"], 
        "close_x": region_refresh_task_button["defult_location"]["x"],
        "close_y": region_refresh_task_button["defult_location"]["y"] + 100,
        "double_confirm_x": 356,
        "double_confirm_y": region_refresh_task_button["defult_location"]["y"],
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.8,
    "region": region_refresh_task_button,
}

file_name = "return_button"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_return_button = yaml.safe_load(f)
config_return_button = {
    "defult_location": {    
        "x": region_return_button["defult_click_point"]["x"],
        "y": region_return_button["defult_click_point"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.8,
    "region": region_return_button["region"],
}


file_name = "alliance_icon"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_alliance_icon = yaml.safe_load(f)
config_alliance_icon = {
    "defult_location": {    
        "x": region_alliance_icon["defult_location"]["x"],
        "y": region_alliance_icon["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.8,
    "region": region_alliance_icon,
}

file_name = "alliance_window"
with open(f'images/{file_name}_config.yaml', 'r', encoding='utf-8') as f:
    region_alliance_window = yaml.safe_load(f)
config_alliance_window = {
    "defult_location": {    
        "x": region_alliance_window["defult_location"]["x"],
        "y": region_alliance_window["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.65,
    "region": region_alliance_window,
}

class TaskResult(Enum):
    SUCCESS = 1
    ERROR = 2
    CONTINUE = 3

class GameController:
    def __init__(self, windwow_controller:WindowsController=None):
        if windwow_controller is None:
            self.windwow_controller = WindowsController()
        else:
            self.windwow_controller = windwow_controller
        self.game_state = "initial"
        self.player_score = 0
        self.level = 1
        self.save_images = save_images  # 是否保存图片
        self.save_path = r"C:\SoftDev\wjdrbot_temp_Data\temp"
        self.set_game_windows()

        self.HeroRecruit_faild_num = 0

    def set_game_windows(self):
        GameWindows_test = {
            "city":None,
            "world":None,
            "left_window":None,
            "warehouse_rewards":None,
            "close_button":None,
        }
        # type: dict[str, GameWindow]
        self.GameWindows: dict[str, GameWindow] = RegisterWindow(GameWindows_test, window_controller=self.windwow_controller)

    def GetWindow(self, window_name) -> 'GameWindow':
        return self.RegisterWindow(window_name)

    def RegisterWindow(self, window_name, config=None) -> 'GameWindow':
        """注册窗口"""
        if window_name in self.GameWindows:
            pass


        
            # log(f"窗口 {window_name} 已经注册")
        else:
            RegisterWindow({window_name: config}, window_controller=self.windwow_controller, GameWindows=self.GameWindows)
            log(f"窗口 {window_name} 注册成功")
        return self.GameWindows[window_name]

    def Reconnect(self,task_name=None):
        return self.find_and_click_image(config_reconnect["picture_path"], config_reconnect["threshold"], notify=True, task_name=task_name)
        # 重新连接游戏逻辑

    def ClosePopup(self, task_name=None):
        return self.find_and_click_image(config_popup["picture_path"], config_popup["threshold"], notify=True, task_name=task_name)
    
    def ReturnToCity(self, task_name=None):
        """返回城市"""
        # 获取屏幕截图
        # with lock:
        world_exists = self.check_image(config_world["picture_path"], config_world["region"], config_world["threshold"], notify=True, task_name=task_name, real_time_show=False)
        if world_exists:
            return True
        city_exists = self.check_image(config_city["picture_path"], config_city["region"], config_city["threshold"], notify=True, task_name=task_name, real_time_show=False)
        if city_exists:
            x = (config_city['region']['left'] + config_city['region']['right']) // 2
            y = (config_city['region']['top'] + config_city['region']['bottom']) // 2
            log(f"图像匹配成功，点击位置: ({x}, {y})")
            self.windwow_controller.tap(x, y)
        
        return_city = False
        for _ in range(Operation_interval):
            time.sleep(1)
            world_exists = self.check_image(config_world["picture_path"], config_world["region"], config_world["threshold"], notify=True, task_name=task_name, real_time_show=False)
            if world_exists:
                return_city = True
                break
        return return_city
    
    def GetRoutineTask_location(self, task_name=None):
        """获取常规任务位置"""
        defult_location = config_RoutineTask["defult_location"]
        defult_x = int(defult_location["x"])
        defult_y = int(defult_location["y"])
        return defult_x,defult_y

        # 获取屏幕截图
        screen = self.windwow_controller.screenshot()
        # 检查屏幕截图是否有效
        if screen is None or screen.size == 0:
            log("获取屏幕截图失败")
            return defult_x,defult_y
        
        self.find_and_click_image()

    def ClikReturnButton(self, task_name=None):
        """点击返回按钮"""
        
        # with lock:
        existed = self.check_image(config_return_button["picture_path"], config_return_button["region"], config_return_button["threshold"], notify=True, task_name=task_name, real_time_show=False)
        if not existed:
            log("返回按钮不存在")
            return False
        self.windwow_controller.tap(config_return_button["defult_location"]["x"], config_return_button["defult_location"]["y"])
            
        return True

    def CloseRoutineTask(self, task_name=None):
        return self.ClikReturnButton(task_name=task_name)


    def NowWindowIsRoutineTask(self):
        return self.check_image(config_RutineTask_return["picture_path"], config_RutineTask_return["region"], config_RutineTask_return["threshold"], notify=True, task_name="常规活动返回按钮", real_time_show=False)

    def OpenRoutineTask(self, task_name=None):
        """打开常规任务"""
        x, y = self.GetRoutineTask_location(task_name)
        self.windwow_controller.tap(x, y)
        seccess = False
        for i in range(Operation_interval):
            time.sleep(1)
            log(f"第{i+1}次检查常规任务返回按钮")
            task_found = self.check_image(config_RutineTask_return["picture_path"], config_RutineTask_return["region"], config_RutineTask_return["threshold"], notify=True, task_name="常规活动返回按钮", real_time_show=False)
            if task_found:
                log(f"常规任务图像匹配成功，点击位置: ({x}, {y})")
                seccess = True
                break
        return seccess
    
    def OpenAlliance_mobilization(self, task_name=None):
        """打开联盟总动员"""
        if not self.NowWindowIsRoutineTask():
            log("当前窗口不是常规任务窗口，无法打开联盟总动员")
            return False
        if self.check_image(config_alliance_mobilization_window["picture_path"], config_alliance_mobilization_window["region"], config_alliance_mobilization_window["threshold"], notify=True, task_name=task_name, real_time_show=False):
            log("联盟总动员窗口已打开")
            return True
        
        seccess = False
        for i in range(3):
            log(f"尝试打开联盟总动员第{i+1}次")
            # with lock:
            self.windwow_controller.swipe(253, 100, 500, 100,200)  # 快速右滑将界面拉到最左
            time.sleep(2)
            find = self.find_and_click_image(config_alliance_mobilization["picture_path"], config_alliance_mobilization["threshold"], notify=False, task_name=task_name)
            if find:
                time.sleep(5)
            if self.check_image(config_alliance_mobilization_window["picture_path"], config_alliance_mobilization_window["region"], config_alliance_mobilization_window["threshold"], notify=True, task_name=task_name, real_time_show=False):
                log("联盟总动员窗口已打开")
                break
        return seccess
    def RefreshAllianceMobilization(self,location_config, task_name=None):
        """刷新联盟总动员左侧列表"""
        if not self.check_image(config_alliance_mobilization_window["picture_path"], config_alliance_mobilization_window["region"], config_alliance_mobilization_window["threshold"], notify=True, task_name=task_name, real_time_show=False):
            log("当前窗口不是联盟总动员窗口，无法刷新")
            return False
        
        if self.__AllianceMobilizationIsCooldown(location_config["region"], task_name=task_name):
            log("联盟总动员任务正在冷却中，无法刷新")
            return False
        
        TaskOnGoing = self.__AllianceTaskIsDoing(location_config["region"], task_name=task_name)
        if TaskOnGoing:
            log("联盟任务正在进行中，无法刷新")
            return False
        
        if self.__AllianceMobilizationTaskIs520Or860(location_config["region"], task_name=task_name):
            log("已经为大拳头不需要刷新")
            return True
        
        self.windwow_controller.tap(location_config["defult_location"]["x"], location_config["defult_location"]["y"])
        time.sleep(1)
        if not self.__RefreshTaskButtonExsited(task_name=task_name):
            log("刷新按钮不存在,关闭刷新窗口")
            self.windwow_controller.tap(config_refresh_task_button["defult_location"]["close_x"], config_refresh_task_button["defult_location"]["close_y"])
            time.sleep(1)
            return False
        else:
            log("刷新按钮已存在，点击刷新按钮")
            self.windwow_controller.tap(config_refresh_task_button["defult_location"]["x"], config_refresh_task_button["defult_location"]["y"])
            time.sleep(1)
        self.windwow_controller.tap(config_refresh_task_button["defult_location"]["double_confirm_x"], config_refresh_task_button["defult_location"]["double_confirm_y"])
        time.sleep(1)

        
    def RefreshAllianceMobilization_right(self, task_name=None):
        return self.RefreshAllianceMobilization(config_Zdy_right, task_name=task_name)
        
    
    def RefreshAllianceMobilization_left(self, task_name=None):
        return self.RefreshAllianceMobilization(config_Zdy_left, task_name=task_name)

    def Task_RefreshAllianceMobilization(self):
        self.ReturnToCity()
        self.OpenRoutineTask()
        self.OpenAlliance_mobilization()
        self.RefreshAllianceMobilization_left()
        self.RefreshAllianceMobilization_right()
        self.CloseRoutineTask()

        return 2*60    
    def __RefreshTaskButtonExsited(self, task_name=None):
        exsited = self.check_image(config_refresh_task_button["picture_path"], config_refresh_task_button["region"], config_refresh_task_button["threshold"], notify=True, task_name=task_name, real_time_show=False)
        return exsited
    
    def __AllianceTaskIsDoing(self,region, task_name=None):
        screen = self.windwow_controller.screenshot()
        cropped_img = screen[region['top']:region['bottom'], region['left']:region['right']]
        exsited = self.find_image_in_image(cropped_img,"images/alliance_task_coin.png",  0.8)[0]
        return not exsited

    def __GetAlliaceTaskScore(self,img, task_name=None):
        OCR_region = {
            "left": 68 , # 左边界X坐标
            "top": 140 , # 上边界Y坐标
            "right": 125 ,# 右边界X坐标
            "bottom": 160 ,# 下边界Y坐标 
                }
        try:
            OCR_img = img[OCR_region['top']:OCR_region['bottom'], OCR_region['left']:OCR_region['right']]
            # 转换为灰度图
            gray = cv2.cvtColor(OCR_img, cv2.COLOR_BGR2GRAY)

            # 二值化处理，使用自适应阈值以提高文字识别率
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )

            # 使用OCR识别文字，配置为识别数字和冒号
            text = pytesseract.image_to_string(
                binary,
                config='--psm 7 -c tessedit_char_whitelist=+0123456789:'
            ).strip()
            score = int(text)
            score = score if score > 40 and  score < 2500 else 0

        except Exception as e:
            
            log(f"获取联盟任务分数失败: {e}")
            score = 0
        return score

    def __AllianceMobilizationTaskIs520Or860(self,region, task_name=None):

        img = self.windwow_controller.screenshot()
        cropped_img = img[region['top']:region['bottom'], region['left']:region['right']]
        score = self.__GetAlliaceTaskScore(cropped_img, task_name=task_name)
        IsTraining = self.check_image("images/zdy_860.png", region, 0.8, notify=True, task_name=task_name, real_time_show=False)
        if (score == 520 or score == 860) and IsTraining:
            log(f"联盟任务分数为{score}，符合条件")
            return True
        else:
            log(f"联盟任务分数为{score}，不符合条件")
            return False

    def __AllianceMobilizationIsCooldown(self,region, task_name=None):
        return self.check_image("images/Zdy_cool_down.png", region, 0.8, notify=True, task_name=task_name, real_time_show=False)
    

    def Task_Alliance(self):
        cool_time_error = 5*60
        for i in range(1,14):
            name = f"alliance_Step{i}"
            window = self.GetWindow(name)
            if window.open():
                if i == 4:
                    x , y = window.open_XY
                    self.windwow_controller.long_press(x , y, 5*1000)
                if i==8:
                    Step9 =f"alliance_Step9"
                    Step9 = self.GetWindow(Step9)
                    if not Step9.CurrentWindowIsMe():
                        for _ in range(20):
                            if not window.open():
                                break
            else:
                if 8 <= i <= 10:
                    pass
                else:
                    window.ClikReturnButton()
                    window.ClikReturnButton()
                    return cool_time_error
                
        return 2 * 60 * 60
        
    
    def Task_AdventureRewards(self):

        if self.InReconnectWindow():
            return 5*60

        """领取探险奖励"""

        click_point_list = [
            {"x": 44, "y": 848},
            {"x": 428, "y": 640},
            {"x": 240, "y": 640},
            {"x": 240, "y": 640},
        ]

        GameWindows = self.GameWindows
        defult_count_down = 60 * 60 * 5  # 默认冷却时间为10分钟
        city = GameWindows["city"]
        world = self.GetWindow("world")
        if( city.CurrentWindowIsMe() or  
            world.CurrentWindowIsMe() ):
            pass
        else:
            if not city.open():
                return 60*5
        
        for point in click_point_list:
            x, y = point["x"], point["y"]
            city.windwow_controller.tap(x, y)
            time.sleep(2)
        self.GameWindows["world"].ClikReturnButton()
        # self.GoToCity()
        return defult_count_down
    
    canned_collected_AM = False
    canned_collected_PM = False
    def Task_WarehouseRewards(self):
        """领取仓库奖励"""
        cool_time_error = 5*60

        window_sequence = [
            self.InReconnectWindow,
            self.ReturnToCity,
            self.__OpenLeftWinow_City,
            "warehouse",
            "warehouse_rewards",
        ]
        # if not hasattr(self, 'canned_collected_AM'):
        #     self.canned_collected_AM = False
        #     self.canned_collected_PM = False

        if self.InReconnectWindow():
            return cool_time_error

        if not self.GoToCity():
            return cool_time_error
        
        if not self.__OpenLeftWinow_City():
            return cool_time_error
        
        warehouse = self.GetWindow("warehouse")

        if not warehouse.open():
            return cool_time_error
        
        warehouse_rewards = self.GetWindow("warehouse_rewards")

        if not warehouse_rewards.open():
            return cool_time_error
        
        conunt_down = warehouse_rewards.GetCoolDownTime()
        DefultClickPoint = warehouse_rewards.GetDefultClickPoint()
        warehouse_rewards.windwow_controller.tap(DefultClickPoint["x"],DefultClickPoint["y"])
        conunt_down = min(conunt_down, 2*60*60)
        conunt_down = max(conunt_down, 2*60)

        def collect_canned():
            canned = self.GetWindow("canned")
            warehouse = self.GetWindow("warehouse")
            for i in range(3):
                if canned.open():
                    x,y = canned.judge_point
                    self.windwow_controller.tap(x,y)
                    log("收取体力成功")
                    return True
            else:
                log("收取体力失败")
                return False

        now_time_hour = datetime.now().hour
        # now_time_hour = 16
        if now_time_hour < 6:
            self.canned_collected_AM = False
            self.canned_collected_PM = False
        elif now_time_hour >= 13:
            self.canned_collected_AM = True
        
        if ( not self.canned_collected_AM  and ( 9 < now_time_hour ) ):
            if collect_canned():
                self.canned_collected_AM = True
        elif ( not self.canned_collected_PM  and ( 15 < now_time_hour < 19  ) ):
            if collect_canned():
                self.canned_collected_PM = True

        Info("仓库任务正常结束")
        log(f"冷却时间: {conunt_down}秒")
        return conunt_down
    
    # 获取空闲行军队列数量
    def ExsitedFreeArmyQueue(self):
        left_window = self.GetWindow("left_window")
        left_window_city = self.GetWindow("left_window_city")
        left_window_world = self.GetWindow("left_window_world")
        world = self.GetWindow("world")
        FreeArmyQueue = self.GetWindow("FreeArmyQueue")
        close_left_window = self.GetWindow("CloseLeftWindow")

        left_window.open()
        time.sleep(0.5)
        if not left_window_world.open():
            log("左侧窗口打开失败")
            return False
        if FreeArmyQueue.CurrentWindowIsMe():
            re = True
        else:
            re = False
        
        close_left_window.open()
        
        return re
    
    def Task_AttackIceBeast(self):
        """
        攻击冰原巨兽任务
        """
        cool_time_error = 5 * 60
        if self.InReconnectWindow():
            return cool_time_error

        self.GoToCity()

        stamina_threshold = self.GetWindow("stamina_threshold")
        if not stamina_threshold.CurrentWindowIsMe():
            return 60 * 60
        
        if not self.__OpenLeftWinow_World():
            return cool_time_error
        
        FreeArmyQueueNum = self.__CheckFreeArmyQueueNum()
        if FreeArmyQueueNum == 0:
            log("暂无行军队列")
            return cool_time_error
        
        window_sequense = [
            "world",
            "collection_Step1",
        ]
        window_sequense_temp = [f"AttackIceBeast_Step{i}" for i in range(1,7)]
        window_sequense += window_sequense_temp
        for window_name in window_sequense:
            window = self.GetWindow(window_name)
            if not window.open():
                return cool_time_error
        time.sleep(0.5)
        if stamina_threshold.CurrentWindowIsMe():
            return 10 * 60
        else:
            return 60 * 60
       

    def Task_collection(self):

        if self.InReconnectWindow():
            return 5*60

        collection_type_list = ["meat", "wood", "coal", "iron"]
        self.GoToCity()
        cool_time = 5*60

        if not self.__OpenLeftWinow_World():
            return cool_time

        FreeArmyQueueNum = self.__CheckFreeArmyQueueNum()
        if FreeArmyQueueNum == 0:
            log("没有空闲行军队列，无法进行采集")
            return cool_time
        
        collection_plan_list = []
        for collection_type in collection_type_list:
            doing_window = self.GetWindow(f"{collection_type}_collection_doing")
            if not doing_window.CurrentWindowIsMe():
                collection_plan_list.append(collection_type)
        
        if len(collection_plan_list) > FreeArmyQueueNum:
            collection_plan_list = random.sample(collection_plan_list, FreeArmyQueueNum)
        
        if len(collection_plan_list) == 0:
            return []
        log(f"计划采集项目:{collection_plan_list}")
        cool_time = []
        GameWindows = self.GameWindows
        GameWindows["world"].open()
        
        if not "collection_Step7" in GameWindows:
            collection_window = {}
            for i in range(1,8):
                if i == 2:
                    pass
                else:
                    collection_window[f"collection_Step{i}"] = None
            for collection_type in collection_type_list:
                collection_window[f"{collection_type}_collection_Step2"] = None
                collection_window[f"{collection_type}_collection_doing"] = None
            RegisterWindow(collection_window, window_controller=self.windwow_controller, GameWindows=self.GameWindows)
        need_run_again = False
        for collection_type in collection_plan_list:
            # if self.GetWindow(f"{collection_type}_collection_doing").CurrentWindowIsMe():
            #     continue
            for i in range(1,8):
                if i == 2:
                    window_name = f"{collection_type}_collection_Step2"
                else:
                    window_name = f"collection_Step{i}"
                if i==4:
                    cool_time_task = GameWindows[window_name].GetCoolDownTime()
                    if not cool_time_task is None:
                        cool_time_task
                GameWindows[window_name].open()
                if not GameWindows[window_name].CurrentWindowIsMe():
                    log(f"{collection_type}采集窗口{window_name}未打开")
                    self.GoToCity()
                    GameWindows["world"].open()
                    need_run_again = True
                    break
            else:
                cool_time.append(cool_time_task)
        if need_run_again:
            cool_time.append(5*60)
        return cool_time

    def __left_window_op(self,sub_window_name):
        left_window = self.GetWindow("left_window")
        left_window_sub = self.GetWindow(sub_window_name)

        if left_window.CurrentWindowIsMe():
            x,y = left_window.judge_point
            left_window.windwow_controller.tap(x,y)
            time.sleep(0.5)
        if not left_window.open():
            return False
        if not left_window_sub.CurrentWindowIsMe():
            if not left_window_sub.open():
                log("左侧城市窗口打开失败")
                return False
            
        return True
    def __OpenLeftWinow_City(self):
            
        return self.__left_window_op("left_window_city")

    def __OpenLeftWinow_World(self):

        return self.__left_window_op("left_window_world")
    
    def __CheckFreeArmyQueueNum(self):
        window_free_quee_list = [ self.GetWindow(f"free_quee_{i}") for i in range(1,7) ]
        free_quee_num = 0
        for window_free_quee in window_free_quee_list:
            if window_free_quee.CurrentWindowIsMe():
                free_quee_num += 1
        self.free_quee_num = free_quee_num
        return free_quee_num

    def Task_FreeArmyQueue(self):
        self.GoToCity()
        if not self.__OpenLeftWinow_World():
            return 60 * 5
    def Task_canned(self):
        cool_time_error = 5*60

        if not self.GoToCity():
            return cool_time_error
        
        # 定义窗口序列
        window_sequence = [
            "left_window",
            "left_window_city",
            "Technology_reserach_center",
            "warehouse",
            "canned"
        ]
        cool_time = []
        for window_name in window_sequence:
            window = self.GetWindow(window_name)
            if not window.open():
                cool_time = cool_time_error
                self.GoToCity()
                break
        
        return cool_time
    
    def task_sub_step_excute(self,name,step_num,Specical_error_func=None):
        if Specical_error_func is None:
            Specical_error_func ={}
        for i in range(1,step_num+1):
            window = self.GetWindow(f"{name}_Step{i}")
            if not window.open():
                if i in Specical_error_func:
                    code = Specical_error_func[i](i)
                    if code == TaskResult.ERROR:
                        return False
                    elif code == TaskResult.SUCCESS:
                        return True
                    elif code == TaskResult.CONTINUE:
                        pass
                    else:
                        logger.warning(f"未定义任务错误执行code:{code}")
                        return False
                else:
                    return False
        
        return True

    def __Intelligence_sub(self,name,step_num):
        reward_window = self.GetWindow("Intelligence_reward")
        def reward_fun(_):
            if reward_window.CurrentWindowIsMe():
                x, y = reward_window.judge_point
                self.windwow_controller.tap(x,y)
                Info(f"成功获取{name}奖励")
                return TaskResult.SUCCESS
            else:
                return TaskResult.ERROR
        error_deal = {1:reward_fun}
        return self.task_sub_step_excute(name,step_num,error_deal)
    
    def Task_Intelligence(self):
        """
        情报任务：自动完成情报相关操作
        """
        cool_time_error = 5 * 60

        if self.InReconnectWindow():
            Info("当前正在重连中")
            return cool_time_error

        world = self.GetWindow("world")
        if not world.CurrentWindowIsMe():
            if not self.GoToCity():
                logger.warning("返回城市失败")
                return cool_time_error
            if not world.open():
                logger.warning("野外打开失败")
                return cool_time_error

        Intelligence_item = [
            ("Intelligence_beast",5),
            ("Intelligence_rescue",3),
            ("Intelligence_adventure",5),
        ]
        finish = True
        for item in Intelligence_item:
            Intelligence_window = self.GetWindow("Intelligence_Step1")
            if not Intelligence_window.open():
                logger.warning("情报窗口打开失败")
                self.GoToCity()
                world.open()
            else:
                name = item[0]
                step_num = item[1]
                if not self.__Intelligence_sub(name,step_num):
                    if not Intelligence_window.CurrentWindowIsMe():
                        logger.warning(f"{name}执行中出错")
                        self.GoToCity()
                        world.open()
                        finish = False
                else:
                    finish = False
                    time.sleep(0.5)
        if finish:
            Intelligence_window.ClikReturnButton()
            cool_down = 4 * 60 *60
        else:
            cool_down = 2 * 60
        return cool_down

    def Task_HeroRecruit(self):
        """
        英雄招募任务：自动完成英雄招募相关操作
        """
        cool_time_error = 5 * 60

        if self.InReconnectWindow():
            Info("当前正在重连中")
            return cool_time_error

        city = self.GetWindow("city")
        world = self.GetWindow("world")

        if not city.CurrentWindowIsMe():
            if not world.CurrentWindowIsMe():
                if not self.GoToCity():
                    return cool_time_error

        def step3_error(step):
            HeroRecruit_Step2 = self.GetWindow("HeroRecruit_Step2")
            HeroRecruit_Step3 = self.GetWindow("HeroRecruit_Step3")
            if HeroRecruit_Step2.CurrentWindowIsMe():
                self.HeroRecruit_faild_num += 1
                return TaskResult.CONTINUE
            for i in range(5):
                if HeroRecruit_Step2.CurrentWindowIsMe():
                    self.HeroRecruit_faild_num = 0 if i != 0 else self.HeroRecruit_faild_num + 1
                    return TaskResult.CONTINUE
                x,y = HeroRecruit_Step2.judge_point
                self.windwow_controller.tap(x,y)
                time.sleep(1)
            return TaskResult.ERROR
                
        error_deal = {3:step3_error}                                                                                                                                                                                                                                                               
            
        name = "HeroRecruit"
        step_num = 6
        exe_status = self.task_sub_step_excute(name,step_num,error_deal)
        if not exe_status:
            self.GoToCity()

        if self.HeroRecruit_faild_num > 5:
            now_time_hour = datetime.now().hour
            cool_down = (26-now_time_hour) * 60 * 60
        else:
            cool_down = 5*60

        return cool_down

    def InReconnectWindow(self):
        reconnect_window = self.GetWindow("reconcect")
        return reconnect_window.CurrentWindowIsMe()
    def Task_Reconnect(self):
        count_down = 60*10
        reconnect_window = self.GetWindow("reconcect")
        if reconnect_window.CurrentWindowIsMe():
            click_point = reconnect_window.GetDefultClickPoint()
            if click_point is not None:
                x, y = click_point["x"], click_point["y"]
                self.windwow_controller.tap(x, y)
                time.sleep(1)

                count_down = 60*30
        
        return count_down
    
    def GoToCXD(self):
        GameWindows = self.GameWindows
        city = GameWindows["city"]
        world = GameWindows["world"]
        left_window = GameWindows["left_window"]
        left_window_city = GameWindows.get("left_window_city", 
                                    self.RegisterWindow("left_window_city"))
        left_window_world = GameWindows.get("left_window_world", 
                                    self.RegisterWindow("left_window_world"))
        cxd_window = GameWindows.get("CXD", 
                                    self.RegisterWindow("CXD"))
        click_figure = GameWindows.get("click_figure",
                                    self.RegisterWindow("click_figure"))
        
        """返回城市"""
        if ((not city.CurrentWindowIsMe()) and 
            (not world.CurrentWindowIsMe())):
            self.GoToCity()
        if not left_window.CurrentWindowIsMe():
            left_window.open()
        if left_window_city.CurrentWindowIsMe():
            pass
        elif left_window_world.CurrentWindowIsMe():
            left_window_city.open()
        else:
            pass
        
        if not left_window_city.CurrentWindowIsMe():
            log("左侧城市窗口打开失败")
            return False
        
        re = cxd_window.open()
        if re:
            for i in range(5):
                time.sleep(0.4)
                if click_figure.open():
                    break
        return re


    def __Train_sub(self):
        GameWindows = self.GameWindows
        for i in range(1,4):
            training_window = self.GetWindow(f"train_Step{i}")
            if i == 1:
                open = training_window.open()
                if open:
                    time.sleep(1)
                    x,y = training_window.open_XY
                    training_window.windwow_controller.tap(x,y)
                    time.sleep(0.5)
                    training_window.windwow_controller.tap(x,y)
                    time.sleep(0.5)
                    training_window.windwow_controller.tap(x,y)
            else:
                open = training_window.open()
            # if not open:
            #     return False, 60*60*5
        CoolDownTime = training_window.GetCoolDownTime()
        training_window.ClikReturnButton()
        return True,CoolDownTime
    # 练兵任务
    def __Train(self,type):
        """练兵任务"""
        GameWindows = self.GameWindows
        self.GoToCity()

        left_window = GameWindows.get("left_window", self.RegisterWindow("left_window"))
        left_window_city = GameWindows.get("left_window_city", self.RegisterWindow("left_window_city"))
        left_window_world = GameWindows.get("left_window_world", self.RegisterWindow("left_window_world"))

        training_complete = f"{type}_training_complete"
        training_complete_window = self.GetWindow(training_complete)
        # # 矛兵训练完成窗口
        # spear_training_complete_window = self.GetWindow("spear_training_complete")
        # # 弓兵训练完成窗口
        # bow_training_complete_window = self.GetWindow("bow_training_complete")

        
        left_window.open()
        time.sleep(0.5)
        if not left_window_city.open():
            log("左侧窗口打开失败")
        if training_complete_window.CurrentWindowIsMe():
            x,y = training_complete_window.judge_point
            training_complete_window.windwow_controller.tap(x,y)
            ok , cool_down = self.__Train_sub()
        else:
            left_window_close = self.GetWindow("CloseLeftWindow")
            left_window_close.open()
            cool_down = 10*60
    
        return cool_down 
    
    def Task_train_shield(self):
        return self.__Train("shield")

    
    def Task_train_spear(self):
        return self.__Train("spear")

    
    def Task_train_bow(self):
        return self.__Train("bow")
    
    def __add_cool_dow_time_to_cool_down_list(self,cool_down_list,cool_down,threshod=60*20):
        skip = False
        for c_time in cool_down_list:
            if abs(cool_down - c_time) < threshod:
                skip = True
                break
        if not skip:
            cool_down_list.append(cool_down)
    def Task_train(self):
        cool_down_list = []
        cool_down = self.__Train("shield")
        self.__add_cool_dow_time_to_cool_down_list(cool_down_list,cool_down)
        cool_down = self.__Train("spear")
        self.__add_cool_dow_time_to_cool_down_list(cool_down_list,cool_down)
        cool_down = self.__Train("bow")
        self.__add_cool_dow_time_to_cool_down_list(cool_down_list,cool_down)
        
        return cool_down_list


    def GoToCity(self):
        """返回城市"""

        GameWindows = self.GameWindows
        city = GameWindows["city"]

        if city.CurrentWindowIsMe():
            log("已经在城市窗口")
            return True
        
        city.open()
        
        if city.CurrentWindowIsMe():
            log("返回城市成功")
            return True
        
        # 尝试点击返回按钮
        for i in range(5):
            city.ClikReturnButton()
            if city.CurrentWindowIsMe():
                log("返回城市成功")
                return True
            city.open()
            if city.CurrentWindowIsMe():
                log("返回城市成功")
                return True
        
        self.GameWindows["close_button"].open()
        if city.CurrentWindowIsMe():
            log("返回城市成功")
            return True
        
        colloction_window = self.GetWindow("collection_Step1")
        if not colloction_window is None:
            if colloction_window.CurrentWindowIsMe():
                city.windwow_controller.tap(250,450)
        
        city.open()
        if city.CurrentWindowIsMe():
            log("返回城市成功")
            return True
        
        x, y = city.open_config["defult_click_point"]["x"], city.open_config["defult_click_point"]["y"]
        city.windwow_controller.tap(x,y)
        time.sleep(1)
        if city.CurrentWindowIsMe():
            log("返回城市成功")
            return True
        city.open()

        if city.CurrentWindowIsMe():
            log("返回城市成功")
            return True
        else:
            log("返回城市失败")
            return False

    def check_image(self, template_path, region, threshold=0.8, notify=False, task_name=None,real_time_show = False):
        """检查指定区域是否匹配模板图片，使用自定义阈值"""
        try:
            # 获取屏幕截图
            screen = self.windwow_controller.screenshot()
            
            # 检查屏幕截图是否有效
            if screen is None or screen.size == 0:
                log("获取屏幕截图失败")
                return False
            
            # 检查区域坐标是否有效
            screen_height, screen_width = screen.shape[:2]
            if (region['left'] < 0 or region['top'] < 0 or 
                region['right'] > screen_width or region['bottom'] > screen_height or
                region['left'] >= region['right'] or region['top'] >= region['bottom']):
                log(f"区域坐标无效: {region}, 屏幕大小: {screen_width}x{screen_height}")
                return False
            
            # 裁剪感兴趣区域
            try:
                roi = screen[region['top']:region['bottom'], region['left']:region['right']]
                if roi.size == 0:
                    log("裁剪区域为空")
                    return False
            except Exception as e:
                log(f"裁剪区域出错: {e}")
                return False
            if real_time_show: 
                # 使用matplotlib显示ROI
                import matplotlib.pyplot as plt
                plt.imshow(roi)
                plt.title("Region of Interest (ROI)")
                plt.show()
            # 转换为BGR格式（OpenCV默认格式）
            try:
                # roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
                roi_bgr = roi  # 处理RGBA格式
            except Exception as e:
                log(f"颜色空间转换出错: {e}")
                return False
            
            # 保存裁剪区域的图片（用于调试）
            self.save_image(roi_bgr, 'cropped')
            
            # 读取模板图片
            template = cv2.imread(template_path)
            if template is None:
                log(f"无法读取模板图片: {template_path}")
                return False
            
            # 检查两个图像的形状和类型是否匹配
            if roi_bgr.shape != template.shape:
                log(f"图像形状不匹配: ROI {roi_bgr.shape}, 模板 {template.shape}")
                return False
            
            if roi_bgr.dtype != template.dtype:
                log(f"图像类型不匹配: ROI {roi_bgr.dtype}, 模板 {template.dtype}")
                template = template.astype(roi_bgr.dtype)
            
            # 进行模板匹配
            try:
                result = cv2.matchTemplate(roi_bgr, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                log(f"模板匹配度: {max_val}, 阈值: {threshold}")
                
                # 如果匹配成功且启用了通知
                if max_val > threshold and notify:
                    # 保存匹配成功的图片（如果启用了保存）
                    matched_image_path = None
                    if self.save_images:
                        matched_image_path = self.save_image(roi_bgr, 'matched')
                    
                    # 发送通知
                    task_info = f"\n任务名称: {task_name}" if task_name else ""
                    message = f"图片匹配成功！{task_info}\n匹配度: {max_val:.2f}\n阈值: {threshold}\n区域: {region}"
                    # send_notification(message, matched_image_path)
                
                return max_val > threshold
            except Exception as e:
                log(f"模板匹配出错: {e}")
                return False
        
        except Exception as e:
            log(f"图片匹配过程中出现未知错误: {e}")
            import traceback
            traceback.print_exc()
            return False

    def find_image_in_image(self,screen, template_path, threshold=0.8,notify=False, task_name=None):
        # 检查屏幕截图是否有效
        if screen is None or screen.size == 0:
            log("图片无效")
            return False, 0, 0
        
        # 转换为BGR格式（OpenCV默认格式）
        # screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        screen_bgr = screen  # 处理RGBA格式
        
        # 读取模板图片
        template = cv2.imread(template_path)
        if template is None:
            log(f"无法读取模板图片: {template_path}")
            return False , 0, 0
        
        # 保存调试图片
        self.save_image(screen_bgr, 'screen')
        # self.save_image(template, 'template')
        
        # 进行模板匹配
        result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
        
        # 获取最佳匹配位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        log(f"最佳匹配度: {max_val}, 位置: {max_loc}")

        center_x, center_y = 0, 0

        # 计算点击位置（模板中心 + 偏移量）
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2 
        center_y = max_loc[1] + h // 2

        find = max_val > threshold
        if find:
            # 如果启用了通知
            if notify:
                # 保存匹配成功的图片（如果启用了保存）
                matched_image_path = None
                if self.save_images:
                    matched_image_path = self.save_image(screen_bgr, 'matched')
                
                task_info = f"\n任务名称: {task_name}" if task_name else ""
                message = f"图片匹配成功！{task_info}\n匹配度: {max_val:.2f}\n阈值: {threshold}\n点击位置: ({center_x}, {center_y})"
                # send_notification(message, matched_image_path)
        else:
            log(f"未找到匹配图片，最佳匹配度: {max_val}")
                    
            
        return find, center_x, center_y

    def find_and_click_image(self, template_path, threshold=0.8, click_offset=(0, 0), notify=False, task_name=None):
        """在屏幕上查找模板图片并点击匹配位置"""
        try:
            # 获取屏幕截图
            screen = self.windwow_controller.screenshot()
            
            exsited, center_x, center_y = self.find_image_in_image(screen, template_path, threshold=threshold,notify=notify, task_name=task_name)
            
            # 如果匹配度超过阈值，点击匹配位置
            if exsited:
                # 计算点击位置（模板中心 + 偏移量）
                click_x = center_x + click_offset[0]
                click_y = center_y+ click_offset[1]

                # 点击位置
                self.windwow_controller.tap(click_x, click_y)
                log(f"点击位置: ({click_x}, {click_y})")
                return True
            else:
                return False
            
        except Exception as e:
            log(f"查找图片出错: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def save_image(self, image, prefix='cropped'):
        """保存图片到指定目录"""
        # 如果未启用图片保存，直接返回
        if not self.save_images:
            return None
        
        try:
            # 确保保存目录存在
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            
            # 生成文件名，包含时间戳
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{self.save_path}/{prefix}_{timestamp}.png'
            
            # 保存图片
            cv2.imwrite(filename, image)
            log(f"调试图片已保存: {filename}")
            return filename
        except Exception as e:
            log(f"保存调试图片失败: {e}")
            return None





from adb_controller import ADBController
import random


if __name__ == "__main__":
    adb_controller = ADBController()
    game_controller = GameController(adb_controller)
    # print(game_controller.Task_train_shield())
    # print(game_controller.Task_train_spear())
    # print(game_controller.Task_train_bow())
    game_controller.GoToCity()
    game_controller.Task_WarehouseRewards()
    # for i in range(20):
    #     re = game_controller.Task_Intelligence()
    #     if re == 4*60*60:
    #         break
        
    
    # GameWindows_test = {
    #     "city":None,
    #     "world":None,
    #     "left_window":None,
    #     "warehouse_rewards":None,
    # }
 
    # RegisterWindow(GameWindows_test)
    # GoToCity()
    # Task_WarehouseRewards()



    # RegisterWindow(GameWindows_test)

    # # 示例用法
    # game_controller_list = []
    # for _ in range(2):
    #     window_controller = WindowsController()
    #     game_controller = GameController(window_controller)
    #     game_controller_list.append(game_controller)
    
    # time_minute = 0
    # while True:
    #     time_minute +=5

    #     for game_controller in game_controller_list:
    #         # 测试函数
    #         game_controller.Reconnect()
    #         time.sleep(1)
    #         game_controller.ClosePopup()
    #         time.sleep(1)
    #         if time_minute % 5 == 0:
    #             pass
    #             # game_controller.Task_RefreshAllianceMobilization()
    #         if time_minute %120 == 0:
    #             game_controller.Task_AllianceTechnology()
    #     time.sleep(60*5)  

