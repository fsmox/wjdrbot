from GameController import *

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


    # def InitAssist(self):
    #     self.assist1.windwow_controller.active()
    #     self.assist1.open()
    #     self.assist1.open()
    #     self.assist2.windwow_controller.active()
    #     self.assist2.open()
    def CureAssist(self):
        cure = self.cure
        assist1 = self.assist1
        assist2 = self.assist2
        cure.windwow_controller.active()
        cure.open()
        cure.open()
        assist1.windwow_controller.active()
        assist1.open()
        assist2.windwow_controller.active()
        assist2.open()
