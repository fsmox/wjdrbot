from GameController import *
from threading import Thread

class CureAssist():

    def __init__(self, game_controller: GameController=None):
        if game_controller is None:
            adb_controller = ADBController(10)
            game_controller = GameController(adb_controller)
            self.cure = game_controller.GetWindow("cure")
            adb_controller = ADBController(0)
            game_controller = GameController(adb_controller)
            self.assist1 = game_controller.GetWindow("assist")
            adb_controller = ADBController(12)
            game_controller = GameController(adb_controller)
            self.assist2 = game_controller.GetWindow("assist")
            self.cure.windwow_controller.screenshot()
            self.assist2.windwow_controller.screenshot()
            self.assist1.windwow_controller.screenshot()
        self.run = False
        self.thread = Thread(target=self.CureAssist, daemon=True)
        self.thread.start()


    # def InitAssist(self):
    #     self.assist1.windwow_controller.active()
    #     self.assist1.open()
    #     self.assist1.open()
    #     self.assist2.windwow_controller.active()
    #     self.assist2.open()
    def CureAssist(self):
        frist = True
        cure = self.cure
        while True:
            if self.run:
                assist1 = self.assist1
                assist2 = self.assist2
                # cure.windwow_controller.active()
                if frist:
                    cure.open()
                    x,y = cure.open_XY
                    cure.windwow_controller.tap(x,y)
                cure.windwow_controller.tap(x,y)
                cure.windwow_controller.tap(x,y)
            else:
                time.sleep(1)

        # assist1.windwow_controller.active()
        # assist1.open()
        # assist2.windwow_controller.active()
        # assist2.open()
    
