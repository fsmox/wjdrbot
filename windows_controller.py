from GlobalConfig import *
import subprocess
import numpy as np
from PIL import Image
import io
import re
import time
import cv2
import threading
import pyautogui
import matplotlib.pyplot as plt
from WindowsGameWindow import WindowManager

lock = threading.Lock()

class WindowsController:
    def __init__(self,wind_manager=None):
        if wind_manager is None:
            wind_manager = WindowManager()
            wind_manager.select_window()
        self.game_wind = wind_manager
        self.selected_window = wind_manager.selected_window
        if self.game_wind.selected_window.title == "无尽冬日":  # 处理无尽冬日的截图 微信小程序
            self.top_offset = 43
            self.bottom_offset = 7
            self.left_offset = 8
            self.right_offset = 8
        else:
            self.top_offset = 0
            self.bottom_offset = 0
            self.left_offset = 0
            self.right_offset = 0


    def XY_to_real(self, x, y):
        x_ratio = x / Capture_width
        y_ratio = y / Capture_height
        # 将相对坐标转换为绝对坐标
        real_x = int(self.selected_window.left+ self.left_offset + x_ratio * (self.selected_window.width - self.left_offset - self.right_offset))
        real_y = int(self.selected_window.top + self.top_offset + y_ratio * (self.selected_window.height - self.top_offset - self.bottom_offset))
        return real_x, real_y
    
    def check_adb_connection(self):
        pass
        # try:
        #     subprocess.run(['adb', 'devices'], check=True)
        # except subprocess.CalledProcessError:
        #     raise Exception("ADB 连接失败，请检查设备连接状态")
    
    def tap(self, x, y):
        real_x, real_y = self.XY_to_real(x, y)
        # 使用pyautogui模拟点击
        with lock:
            pyautogui.moveTo(real_x, real_y, duration=0.1)
            pyautogui.click()
    
    def screenshot(self):
        # 获取屏幕截图
        left = self.selected_window.left
        top = self.selected_window.top
        width = self.selected_window.width
        height = self.selected_window.height
        image = pyautogui.screenshot(region=(left, top, width, height))
        image_np = np.array(image)
        if self.game_wind.selected_window.title == "无尽冬日":  # 处理无尽冬日的截图 微信小程序
            image_np = image_np[self.top_offset:-self.bottom_offset, self.left_offset:-self.right_offset]
        img_resized = cv2.resize(image_np, (Capture_width, Capture_height))

        return img_resized
    

    # def get_current_app(self):
    #     # """获取当前前台应用的包名"""
    #     # cmd = ['adb', 'shell', 'dumpsys', 'window', '|', 'grep', '-E', 'mCurrentFocus']
    #     # result = subprocess.run(cmd, capture_output=True, text=True)
        
    #     # # 使用正则表达式提取包名
    #     # match = re.search(r'mCurrentFocus=.*{.*\s+([\w\.]+)\/.*}', result.stdout)
    #     # if match:
    #     #     return match.group(1)
    #     return None
    
    # def is_app_foreground(self, package_name):
    #     """检查指定应用是否在前台"""
    #     current_app = self.get_current_app()
    #     return current_app == package_name
    
    # def launch_app(self, package_name):
    #     """启动指定应用"""
    #     subprocess.run(['adb', 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1']) 
    
    # def force_stop_app(self, package_name):
    #     """强制停止应用"""
    #     subprocess.run(['adb', 'shell', 'am', 'force-stop', package_name])
    #     print(f"已强制停止应用: {package_name}")

    def swipe(self, start_x, start_y, end_x, end_y, duration=500):
        """
        使用 pyautogui 模拟滑动操作
        :param start_x: 起始点X坐标
        :param start_y: 起始点Y坐标
        :param end_x: 结束点X坐标
        :param end_y: 结束点Y坐标
        :param duration: 滑动持续时间（毫秒）
        """
        # 将持续时间从毫秒转换为秒
        duration_seconds = duration / 1000.0

        # 移动到起始点
        start_x, start_y = self.XY_to_real(start_x, start_y)
        end_x, end_y = self.XY_to_real(end_x, end_y)
        pyautogui.moveTo(start_x, start_y, duration=0.1)

        # 按下鼠标左键
        pyautogui.mouseDown()
        time.sleep(0.5)

        # 拖动到终点
        pyautogui.moveTo(end_x, end_y, duration=duration_seconds)

        # 松开鼠标左键
        pyautogui.mouseUp()

    def long_press(self, x, y, duration=1000):
        """
        执行长按操作
        :param x: X坐标
        :param y: Y坐标
        :param duration: 长按持续时间（毫秒）
        """
        # 将持续时间从毫秒转换为秒
        duration_seconds = duration / 1000.0

        x, y = self.XY_to_real(x, y)
        # 使用 pyautogui 模拟长按操作
        pyautogui.moveTo(x, y, duration=0.1)  # 移动到指定坐标
        pyautogui.mouseDown()  # 按下鼠标左键
        time.sleep(duration_seconds)  # 持续按住指定时间
        pyautogui.mouseUp()  # 松开鼠标左键

if __name__ == "__main__":
    controller = WindowsController()
    # controller.tap(100, 200)  # 示例点击坐标
    # controller.swipe(253, 100, 500, 100,200)  # 示例滑动坐标
    # controller.long_press(150, 250)  # 示例长按坐标
    screenshot = controller.screenshot()  # 截图
    plt.imshow(screenshot)
    plt.show()