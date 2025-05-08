from GlobalConfig import *
from windows_controller import WindowsController
from logger import log
import cv2
from datetime import datetime
import os
import threading
import time
import yaml
import pytesseract

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
    "threshold": 0.8,
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
    "threshold": 0.8,
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
        "x": region_return_button["defult_location"]["x"],
        "y": region_return_button["defult_location"]["y"], 
    }, 
    "picture_path": f"images/{file_name}.png",
    "threshold": 0.8,
    "region": region_return_button,
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

class GameController:
    def __init__(self, windwow_controller:WindowsController):
        self.windwow_controller = windwow_controller
        self.game_state = "initial"
        self.player_score = 0
        self.level = 1
        self.save_images = save_images  # 是否保存图片
        self.save_path = "images/tmp"

    def Reconnect(self,task_name=None):
        return self.find_and_click_image(config_reconnect["picture_path"], config_reconnect["threshold"], notify=True, task_name=task_name)
        # 重新连接游戏逻辑

    def ClosePopup(self, task_name=None):
        return self.find_and_click_image(config_popup["picture_path"], config_popup["threshold"], notify=True, task_name=task_name)
    
    def ReturnToCity(self, task_name=None):
        """返回城市"""
        # 获取屏幕截图
        with lock:
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
        
        with lock:
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
            with lock:
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

        return None    
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
        IsTraining = self.check_image("images/zdy_860.png", region, 0.9, notify=True, task_name=task_name, real_time_show=False)
        if (score == 520 or score == 860) and IsTraining:
            log(f"联盟任务分数为{score}，符合条件")
            return True
        else:
            log(f"联盟任务分数为{score}，不符合条件")
            return False

    def __AllianceMobilizationIsCooldown(self,region, task_name=None):
        return self.check_image("images/Zdy_cool_down.png", region, 0.8, notify=True, task_name=task_name, real_time_show=False)


    def __IsAllianceWindow(self, task_name=None):
        exsited = self.check_image(config_alliance_window["picture_path"], config_alliance_window["region"], config_alliance_window["threshold"], notify=True, task_name=task_name, real_time_show=False)
        return exsited
    def __AllianceIconExsited(self, task_name=None):
        exsited = self.check_image(config_alliance_icon["picture_path"], config_alliance_icon["region"], config_alliance_icon["threshold"], notify=True, task_name=task_name, real_time_show=False)
        return exsited
    def OpenAllianceWindow(self, task_name=None):
        if not self.__AllianceIconExsited(task_name=task_name):
            self.ClikReturnButton(task_name=task_name)
        
        if not self.__AllianceIconExsited(task_name=task_name):
            log("联盟图标不存在，无法打开联盟窗口")
            return False
        
        self.windwow_controller.tap(config_alliance_icon["defult_location"]["x"], config_alliance_icon["defult_location"]["y"])
        time.sleep(1)
        seccess = False
        for i in range(Operation_interval):
            time.sleep(1)
            log(f"第{i+1}次检查联盟窗口")
            task_found = self.__IsAllianceWindow(task_name=task_name)
            if task_found:
                log("联盟窗口已打开")
                seccess = True
                break
        
        return seccess
    def OpenAllianceTechnologyWindow(self, task_name=None):
        """打开联盟科技窗口"""
        if not self.__IsAllianceWindow(task_name=task_name):
            log("当前窗口不是联盟窗口，无法打开联盟科技窗口")
            return False
        
        self.windwow_controller.tap(374,650)
        time.sleep(1)
        return True
    def CloseAllianceWindow(self, task_name=None):
        self.windwow_controller.tap(config_return_button["defult_location"]["x"],config_return_button["defult_location"]["y"])
        return True

    def CloseAllianceTechnologyWindow(self, task_name=None):
        self.windwow_controller.tap(config_return_button["defult_location"]["x"],config_return_button["defult_location"]["y"])
        return True
    
    def ClickAllianceTechnologyRecommendButton(self, task_name=None):
        """点击推荐按钮"""
        config_alliance_technology_recommend_icon = {
            "picture_path": "images/alliance_technology_recommend.png",
            "threshold": 0.8,
        }
        screen = self.windwow_controller.screenshot()
        # 检查屏幕截图是否有效
        if screen is None or screen.size == 0:
            log("获取屏幕截图失败")
            return False
        exsited,x,y = self.find_image_in_image(screen, config_alliance_technology_recommend_icon["picture_path"], config_alliance_technology_recommend_icon["threshold"], notify=True, task_name=task_name)
        if not exsited:
            log("大拇指选项不存在")
            return False
        with lock:
            self.windwow_controller.tap(x, y)
        time.sleep(1)
        self.windwow_controller.long_press(374,714,5000)
        self.windwow_controller.tap(config_return_button["defult_location"]["x"],config_return_button["defult_location"]["y"])

        return True


    def Task_AllianceTechnology(self):
        self.ReturnToCity()
        self.OpenAllianceWindow()
        self.OpenAllianceTechnologyWindow()
        self.ClickAllianceTechnologyRecommendButton()
        self.CloseAllianceTechnologyWindow()
        self.CloseAllianceWindow()

        return True

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

class ImageJudge:
    def __init__(self, config):
        self.image_path = config.get("picture_path",None)
        self.region = config.get("region",None)
        self.defult_location = config.get("defult_click_point",None)
        self.method = config.get("method",None)
        self.threshold = config.get("threshold",0.8)
        self.save_images = config.get("save_images",True)
        self.save_path = config.get("save_path","images/tmp")

    def Existed(self, screen):

        existed = False
        center_x = 0
        center_y = 0
        if self.method is None or self.method == "None":
            if self.defult_location is not None:
                existed = True
                center_x = self.defult_location["x"]
                center_y = self.defult_location["y"]
            else:
                existed = False

        if self.method == "check" or self.method == "swipe_check":
            existed = self.check_image(screen)
            center_x = (self.region['left'] + self.region['right']) // 2
            center_y = (self.region['top'] + self.region['bottom']) // 2
        elif self.method == "find" or self.method == "swipe_find":
            existed, center_x, center_y = self.find_image_in_image(screen)

        return existed, center_x, center_y
    

    def check_image(self, screen, real_time_show=False, notify=False, task_name=None):
        """检查指定区域是否匹配模板图片，使用自定义阈值"""

        region = self.region
        template_path = self.image_path
        threshold = self.threshold

        try:
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

    def find_image_in_image(self,screen, template_path=None, threshold=None,notify=False, task_name=None):
        template_path = template_path if template_path else self.image_path
        threshold = threshold if threshold else self.threshold
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


class GameWindow:
    def __init__(self,window_name,open_config,in_window_config,cool_down_config, windwow_controller: WindowsController):
        self.windwow_controller = windwow_controller
        self.window_name = window_name
        self.father_window = None
        self.child_windows = {}
        self.open_config = open_config
        self.in_window_config = in_window_config
        self.cool_down_config = cool_down_config

    def CurrentWindowIsMe(self):
        """判断当前窗口是否是我"""
        # 获取屏幕截图
        screen = self.windwow_controller.screenshot()
        # 检查屏幕截图是否有效
        if screen is None or screen.size == 0:
            log("获取屏幕截图失败")
            return False
        
        judge = ImageJudge(self.in_window_config)
        # 检查当前窗口是否是我
        existed,x,y = judge.Existed(screen)
        return existed

    def CurrentWindowIsFather(self):
        """判断当前窗口是否是父窗口"""
        if self.father_window is None:
            return False
        return self.father_window.CurrentWindowIsMe()

    def open(self):
        # # 打开游戏窗口的逻辑
        # if not self.CurrentWindowIsFather():
        #     log("当前窗口不是父窗口，无法打开游戏窗口")
        #     return False

        judge = ImageJudge(self.open_config)

        if judge.method == "swipe_check" or judge.method == "swipe_find":
            for i in range(3):
                log(f"第{i+1}次检查{self.window_name}窗口")
                existed,x,y = judge.Existed(self.windwow_controller.screenshot())
                if existed:
                    break
                start_x = self.open_config["swipe"]["start"]["x"]
                start_y = self.open_config["swipe"]["start"]["y"]
                end_x = self.open_config["swipe"]["end"]["x"]
                end_y = self.open_config["swipe"]["end"]["y"]
                duration = self.open_config["swipe"]["duration"]
                self.windwow_controller.swipe(start_x, start_y, end_x, end_y, duration)
                time.sleep(1)
                # 先滑动到窗口位置
            if not existed:
                existed,x,y = judge.Existed(self.windwow_controller.screenshot())
            
        else:
            existed,x,y = judge.Existed(self.windwow_controller.screenshot())
        
        if not existed:
            log(f"没检测到{self.window_name}窗口打开图标，无法打开{self.window_name}窗口")
            return False
        

        self.windwow_controller.tap(x,y)
        for i in range(Operation_interval):
            time.sleep(1)
            log(f"第{i+1}次检查游戏窗口")
            task_found = self.CurrentWindowIsMe()
            if task_found:
                log(f"{self.window_name}窗口已打开")
                break

        time.sleep(1)

    def return_to_father_window(self):
        pass

    
GameWindows = {}
def RegisterWindow(windows_config,window_controller=None):
    """注册窗口"""
    global GameWindows
    if window_controller is None:
        window_controller = WindowsController()
    for window_name,config in windows_config.items():
        in_window_config = f"images/{window_name}_window_config.yaml"
        open_config = f"images/{window_name}_open_config.yaml"
        cool_down_config = f"images/{window_name}_cool_down_config.yaml"
        if not config  is None:
            in_window_config = config.get("in_window_config",in_window_config)
            open_config = config.get("open_config",open_config)

        if os.path.exists(in_window_config) and os.path.exists(open_config):
            with open(in_window_config, 'r', encoding='utf-8') as f:
                in_window_config = yaml.safe_load(f)
            with open(open_config, 'r', encoding='utf-8') as f:
                open_config = yaml.safe_load(f)
            
            if os.path.exists(cool_down_config):
                with open(cool_down_config, 'r', encoding='utf-8') as f:
                    cool_down_config = yaml.safe_load(f)
            else:
                cool_down_config = None
            GameWindows[window_name] = GameWindow(window_name,open_config,in_window_config,cool_down_config,window_controller)
        else:
            log(f"窗口配置文件不存在: {in_window_config} 或 {open_config}")
            continue

    return GameWindows

if __name__ == "__main__":
    GameWindows_test = {
        "city":None,
        "world":None,
        "left_window":None,
        "warehouse_rewards":None,
    }
 
    RegisterWindow(GameWindows_test)

    if not GameWindows["city"].CurrentWindowIsMe():
        GameWindows["city"].open()
    GameWindows["world"].open()
    GameWindows["left_window"].open()
    GameWindows["warehouse_rewards"].open()


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

