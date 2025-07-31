from logger import log, Info
from Task import GameTask
import random

class Task_Collection(GameTask):
    def __init__(self, game_controller):
        super().__init__("CollectionTask", game_controller)
        self.collection_window = self.game_controller.GetWindow("collection")
        self.config["collection_count"] = 0  # 初始化收集次数

    def exe(self):
        collection_type_list = ["meat", "wood", "coal", "iron"]
        # world_window = self.game_controller.GetWindow("world")
        # city = self.game_controller.GetWindow("city")

        self.game_controller.GoToCity()

        cool_time = 5*60

        if not self.game_controller.OpenLeftWindow_World():
            return cool_time

        FreeArmyQueueNum = self.game_controller.GetFreeArmyQueueNum()
        if FreeArmyQueueNum == 0:
            log("没有空闲行军队列，无法进行采集")
            return cool_time
        
        collection_plan_list = []
        for collection_type in collection_type_list:
            doing_window = self.game_controller.GetWindow(f"{collection_type}_collection_doing")
            if not doing_window.CurrentWindowIsMe():
                collection_plan_list.append(collection_type)
        
        if len(collection_plan_list) > FreeArmyQueueNum:
            collection_plan_list = random.sample(collection_plan_list, FreeArmyQueueNum)
        
        if len(collection_plan_list) == 0:
            return []
        log(f"计划采集项目:{collection_plan_list}")
        cool_time = []
        world_window = self.game_controller.GetWindow("world")
        world_window.open()

        need_run_again = False
        for collection_type in collection_plan_list:

            for i in range(1,8):
                if i == 2:
                    window_name = f"{collection_type}_collection_Step2"
                else:
                    window_name = f"collection_Step{i}"
                window = self.game_controller.GetWindow(window_name)
                if i==4:
                    cool_time_task = window.GetCoolDownTime()
                
                if not window.open():
                    log(f"{collection_type}采集窗口{window_name}未打开")
                    self.game_controller.GoToCity()
                    world_window.open()
                    need_run_again = True
                    break
            else:
                cool_time.append(cool_time_task)
        if need_run_again:
            cool_time.append(5*60)
        return cool_time

if __name__ == "__main__":
    from GameController import GameController
    game_controller = GameController()
    task = Task_Collection(game_controller)
    task.exe()
    print("任务执行完毕")