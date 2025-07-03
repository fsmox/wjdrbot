import time
from GameController import GameController

def Task_Alliance(game_controller: GameController):
    cool_time_error = 5*60
    for i in range(1,19):
        name = f"alliance_Step{i}"
        window = game_controller.GetWindow(name)
        if i==8:
            alliance_Step8_0 = game_controller.GetWindow("alliance_Step8_0")
            alliance_Step8_0.open()
        elif 13<=i<=17: # 13-17是加入集结
            if not game_controller.auto_join_rally:
                continue

        if window.open():
            if i== 2:
                time.sleep(0.5)
                window.windwow_controller.op_after_capture = True
            elif i == 4:
                x , y = window.open_XY
                game_controller.windwow_controller.long_press(x , y, 5*1000)
            elif i==8:
                Step9 =f"alliance_Step9"
                Step9 = game_controller.GetWindow(Step9)
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

if __name__ == "__main__":
    game_controller = GameController()
    Task_Alliance(game_controller)