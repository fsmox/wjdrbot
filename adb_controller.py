import subprocess
import numpy as np
from PIL import Image
import io
import re
import cv2
from GlobalConfig import *
from logger import log
from datetime import datetime, timedelta

class ADBController:
    def __init__(self,user_id=None):
        self.user_id = user_id
        self.set_op()
        self.check_adb_connection()

    def set_op(self):
        self.last_op_time = datetime.now()
        self.op_after_capture = True
        self.op_judge_ok = False
    
    def active(self):
        cmd = ['adb', 'shell', 'am', 'start', '--user', str(self.user_id), '-n', 'com.gof.china/com.unity3d.player.DDUnityLaunchActivity']
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise Exception("窗口激活失败")
        self.set_op()
    def input_text(self, text, del_len=10):
        """
        输入文本到当前活动窗口
        :param text: 要输入的文本
        """

        for _ in range(del_len):
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '67'])  # 67是删除键

        # 使用adb命令模拟输入文本
        cmd = ['adb', 'shell', 'input', 'text', text]
        try:
            subprocess.run(cmd, check=True)
            self.set_op()
        except subprocess.CalledProcessError:
            raise Exception("文本输入失败，请检查设备连接状态")
    def check_adb_connection(self):
        try:
            subprocess.run(['adb', 'devices'], check=True)
            # 如果没有设备连接，尝试连接模拟器
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if( not 'emulator-5554' in result.stdout and
                not '127.0.0.1:7555' in result.stdout):
                cmd = ['adb', 'connect', '127.0.0.1:7555']
                subprocess.run(cmd, check=True)
            
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
        self.set_op()
    
    def screenshot(self,enable_cache = True, container=None):
        # 获取原始截图字节
        capture_time = datetime.now() 
        if ( not self.op_after_capture and 
            enable_cache and 
            ((capture_time - self.last_op_time > timedelta(seconds=5) or self.op_judge_ok))):
            if capture_time - self.last_capture_time < timedelta(seconds=30):
                if container is not None:
                    container[0] = self.capture_original
                log("使用上次截图")
                return self.last_img 
        
        log("ADB获取截图")
        # 在模拟器中保存截图
        # subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/screenshot.png'], check=True)
        # 从模拟器中拉取截图到本地
        # result = subprocess.run(['adb', 'pull', '/sdcard/screenshot.png', './screenshot.png'], check=True)
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
        # 将图片转换为BGR模式
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        self.capture_original = image_bgr
        if container is not None:
            container[0] = self.capture_original
        if original_size:
            img_resized = image_bgr
        else:
            img_resized = cv2.resize(image_bgr, (Capture_width, Capture_height))
        
        self.op_after_capture = False
        self.last_img = img_resized

        self.last_capture_time = capture_time
        return img_resized
        
    
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
        self.set_op()

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
        self.set_op()
