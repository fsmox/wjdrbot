import subprocess
import numpy as np
from PIL import Image
import io
import re
import cv2
from GlobalConfig import *
from logger import log

class ADBController:
    def __init__(self,user_id=None):
        self.user_id = user_id
        self.check_adb_connection()
    
    def active(self):
        cmd = ['adb', 'shell', 'am', 'start', '--user', str(self.user_id), '-n', 'com.gof.china/com.unity3d.player.DDUnityLaunchActivity']
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise Exception("窗口激活失败")
    def check_adb_connection(self):
        try:
            cmd = ['adb', 'connect', '127.0.0.1:7555']
            subprocess.run(cmd, check=True)
            subprocess.run(['adb', 'devices'], check=True)
        except subprocess.CalledProcessError:
            raise Exception("ADB 连接失败，请检查设备连接状态")
    
    def XY_to_real(self, x, y):
        x_ratio = x / Capture_width
        y_ratio = y / Capture_height
        # 将相对坐标转换为绝对坐标
        real_x = int(x_ratio * (self.width))
        real_y = int(y_ratio * (self.height))
        return real_x, real_y
    def tap(self, x, y):
        # 将相对坐标转换为绝对坐标
        x, y = self.XY_to_real(x, y)

        log(f"点击位置: ({x}, {y})")
        # 使用adb命令模拟点击
        subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])
    
    def screenshot(self):
        # 获取原始截图字节
        result = subprocess.run(['adb', 'shell', 'screencap', '-p'], capture_output=True)
        img_bytes = result.stdout

        # 兼容Windows下的换行符问题
        img_bytes = img_bytes.replace(b'\r\n', b'\n')

        # 检查adb输出是否为PNG文件头
        if not img_bytes.startswith(b'\x89PNG'):
            log("ADB截图失败，输出内容不是PNG图片。请检查ADB连接和设备。")
            return None

        # 转为图片
        image = Image.open(io.BytesIO(img_bytes))
        self.width,  self.height= image.size

        image_np = np.array(image)
        img_resized = cv2.resize(image_np, (Capture_width, Capture_height))
        # 将图片转换为BGR模式
        image_bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGBA2RGB)
        
        return np.array(image_bgr)
        
    
    def get_current_app(self):
        """获取当前前台应用的包名"""
        cmd = ['adb', 'shell', 'dumpsys', 'window', '|', 'grep', '-E', 'mCurrentFocus']
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        # 使用正则表达式提取包名
        match = re.search(r'mCurrentFocus=.*{.*\s+([\w\.]+)\/.*}', result.stdout)
        if match:
            return match.group(1)
        return None
    
    def is_app_foreground(self, package_name):
        """检查指定应用是否在前台"""
        current_app = self.get_current_app()
        return current_app == package_name
    
    def launch_app(self, package_name):
        """启动指定应用"""
        subprocess.run(['adb', 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1']) 
    
    def force_stop_app(self, package_name):
        """强制停止应用"""
        subprocess.run(['adb', 'shell', 'am', 'force-stop', package_name])
        log(f"已强制停止应用: {package_name}")

    def swipe(self, start_x, start_y, end_x, end_y, duration=500):
        """
        执行滑动操作
        :param start_x: 起始点X坐标
        :param start_y: 起始点Y坐标
        :param end_x: 结束点X坐标
        :param end_y: 结束点Y坐标
        :param duration: 滑动持续时间（毫秒）
        """
        start_x, start_y = self.XY_to_real(start_x, start_y)
        end_x, end_y = self.XY_to_real(end_x, end_y)
        duration = int(duration)
        log(f"滑动从 ({start_x}, {start_y}) 到 ({end_x}, {end_y}) 持续时间: {duration}毫秒")
        subprocess.run([
            'adb', 'shell', 'input', 'swipe',
            str(start_x), str(start_y),
            str(end_x), str(end_y),
            str(duration)
        ])

    def long_press(self, x, y, duration=1000):
        """
        执行长按操作
        :param x: X坐标
        :param y: Y坐标
        :param duration: 长按持续时间（毫秒）
        """
        x, y = self.XY_to_real(x, y)
        subprocess.run([
            'adb', 'shell', 'input', 'swipe',
            str(x), str(y), str(x), str(y),
            str(duration)
        ])
