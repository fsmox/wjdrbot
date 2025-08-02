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
        cool_down_list = []
        for i in range(3):
            window = self.game_controller.GetWindow(f"PedTask_Step{i+1}")
            if not window.open():
                Info("打开兽栏失败")
                cool_down_list.append(5 * 60)  # 如果打开兽栏失败，返回冷却时间5分钟
                return cool_down_list
            if i == 0:
                cool_down_list_t = self.use_skill()
                cool_down_list.extend(cool_down_list_t)

        if self.config.get("TodayRunTimes", 0) == 0:
            today_alliance_treasure = False
        else:
            today_alliance_treasure = self.config.get("today_alliance_treasure", False)
        
        if not today_alliance_treasure:
            if self.alliance_treasure():
                today_alliance_treasure = True
            self.config["today_alliance_treasure"] = today_alliance_treasure

        self.treasure_complete()
        treasure_doing = self.game_controller.GetWindow("treasure_doing")
        if treasure_doing.CurrentWindowIsMe():
            log("当前有派遣寻宝正在进行，等待完成")
            cool_down_list.append(30 * 60)  # 如果有派遣寻宝正在进行，返回冷却时间30分钟
        else:
            cool_down = self.treasure()
            cool_down_list.append(cool_down)

        for i in range(4):
            window.ClikReturnButton()
            time.sleep(0.5)


        return cool_down_list

    def use_skill(self):
        def use_skill(skill_name):
            result = False
            #点击技能图标
            skill_window = self.game_controller.GetWindow(f"ped_skill_{skill_name}")
            use_skill_window = self.game_controller.GetWindow(f"ped_use_skill")
            reward_window = self.game_controller.GetWindow(f"ped_reward")
            if skill_window.open():
                time.sleep(0.5)
                if use_skill_window.open():
                    time.sleep(0.5)
                    reward_window.open()
                    time.sleep(0.5)
                    result = True
            return result
        cool_down_list = []
        self.bull_on = use_skill("bull")
        self.wolf_on = use_skill("wolf")
        skill_1_used = use_skill("1")
        skill_2_used = use_skill("2")

        if skill_1_used or self.bull_on or self.wolf_on:
            cool_down_list.append(23 * 60 * 60)
        if skill_2_used:
            cool_down_list.append(39 * 60 * 60)

        return cool_down_list

        
    
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
    
    #领取联盟宝藏
    def alliance_treasure(self):
        """领取联盟宝藏"""
        treasure_alliance = self.game_controller.GetWindow("treasure_alliance")
        treasure_alliance_get_all = self.game_controller.GetWindow("treasure_alliance_get_all")
        if not treasure_alliance.open():
            Info("打开联盟宝藏窗口失败")
            return False
        re = True
        if not treasure_alliance_get_all.open():
            Info("打开领取联盟宝藏窗口失败")
            re =  False
        self.treasure_close.open()

        return re

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
            self.treasure_close.open()
            self.treasure_close.open()
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
    
    def After(self):
        if self.bull_on:
            pass
        #待作业
        
        return super().After()


if __name__ == "__main__":
    from GameController import GameController
    game_controller = GameController()
    task = Task_Ped(game_controller)
    task()
    # task.treasure_close.open()
    print("任务执行完毕")