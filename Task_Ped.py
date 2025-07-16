import time
from logger import log, Info
from Task import GameTask

class Task_Ped(GameTask):
    def __init__(self, game_controller):
        super().__init__("PedTask", game_controller)
        # 获取金色箱子窗口
        self.gold_box_window = self.game_controller.GetWindow("gold_box")
        # 获取紫色箱子窗口
        self.purple_box_window = self.game_controller.GetWindow("purple_box")
        # 获取蓝色箱子窗口
        self.blue_box_window = self.game_controller.GetWindow("blue_box")

        # 派遣寻宝窗口
        self.treasure_dispatch_window = self.game_controller.GetWindow("treasure_dispatch")
        self.treasure_start = self.game_controller.GetWindow("treasure_start")
        self.treasure_close = self.game_controller.GetWindow("treasure_close")
        self.now_treasure_num = 0  # 当前寻宝次数
        self.config["now_treasure_num"] = self.now_treasure_num

    def exe(self):
        world = self.game_controller.GetWindow("world")
        city = self.game_controller.GetWindow("city")
        if world.CurrentWindowIsMe() or city.CurrentWindowIsMe():
            pass
        else:
            self.game_controller.GoToCity()
        
        for i in range(3):
            window = self.game_controller.GetWindow(f"PedTask_Step{i+1}")
            if not window.open():
                Info("打开兽栏失败")
                return 5 * 60  # 如果打开兽栏失败，返回冷却时间5分钟

        self.treasure_complete()
        treasure_doing = self.game_controller.GetWindow("treasure_doing")
        if treasure_doing.CurrentWindowIsMe():
            log("当前有派遣寻宝正在进行，等待完成")
            cool_down = 10 * 60
        else:
            cool_down = self.treasure()
        window.ClikReturnButton()

        return cool_down

    
    def treasure_complete(self):
        """完成派遣寻宝"""
        if self.config["now_treasure_num"] > 0:
            self.config["now_treasure_num"] = self.config["now_treasure_num"] - 1
            box_location = self.config.get("BoxLocation", None)
            if box_location is None:
                log("没有记录箱子位置，无法完成派遣寻宝")
                return False
            
            self.game_controller.windwow_controller.tap(*box_location)
            time.sleep(1)
        
        else:
            complete_window = self.game_controller.GetWindow("treasure_complete")
            for i in range(3):
                if complete_window.open():
                    break
            else:
                Info("打开完成派遣寻宝窗口失败")
                return False
            
            
        window = self.game_controller.GetWindow(f"treasure_get")
        if not window.open():
            Info("打开领取奖励窗口失败")
        
        window = self.game_controller.GetWindow(f"treasure_get_1")

        if not window.open():
            Info("打开领取奖励窗口失败")
        
        window = self.game_controller.GetWindow(f"treasure_get_2")

        if not window.open():
            Info("打开领取奖励窗口失败")

        return True


    def treasure(self):
        if self.gold_box_window.open():
            cool_down = 5*60*60
            box_location = self.gold_box_window.open_XY
        elif self.purple_box_window.open():
            cool_down = 4*60*60
            box_location = self.purple_box_window.open_XY
        elif self.blue_box_window.open():
            cool_down = 3*60*60
            box_location = self.blue_box_window.open_XY
        else:
            log("没有检测到金色、紫色或蓝色箱子窗口，无法进行派遣寻宝")
            return 5 * 60
        
        if not self.treasure_dispatch_window.open():
            Info("打开派遣寻宝窗口失败")
            return 5 * 60

        if not self.treasure_start.open():
            Info("打开开始寻宝窗口失败")
            return 5 * 60

        if not self.treasure_close.open():
            Info("打开关闭寻宝窗口失败")

        self.config["BoxLocation"] = box_location
        self.config["now_treasure_num"] = self.config["now_treasure_num"] + 1
        
        return cool_down




