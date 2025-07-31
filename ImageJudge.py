
from GlobalConfig import *
from windows_controller import WindowsController
from logger import log,Info,logger
import cv2
from datetime import datetime, timedelta
import os
import yaml
import pytesseract

class ImageJudge:
    def __init__(self, config,name=None):
        self.config = config
        self.image_path = config.get("picture_path",None)
        self.region = config.get("region",None)
        self.defult_location = config.get("defult_click_point",None)
        self.method = config.get("method",None)
        self.threshold = config.get("threshold",0.8)
        self.save_images = config.get("save_images",True)
        if name is None:
            self.save_path = config.get("save_path",r"C:\SoftDev\wjdrbot_temp_Data\temp")
            self.label_path = config.get("label_path",None)
        else:
            root_path = r"C:\SoftDev\wjdrbot_temp_Data"
            self.save_path = config.get("save_path",f"{root_path}/AI_Data/images/{name}")
            self.label_path = config.get("label_path",f"{root_path}/AI_Data/labels/{name}")

    def Existed(self, screenshot):
        new_picture_container = [None]
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
            region = self.region
        else:
            screen = screenshot(container=new_picture_container)
            # 检查屏幕截图是否有效
            if screen is None or screen.size == 0:
                log("获取屏幕截图失败")
                return False, center_x, center_y
            if self.method == "check" or self.method == "swipe_check":
                if Create_new_config:

                    region = self.region
                    top = max(region['top'] - 10,0)
                    bottom = min(region['bottom']+10,Capture_height)
                    left = max(region['left']-10,0)
                    right = min(region['right']+10,Capture_width)
                    cropped_img = screen[top:bottom, left:right]
                    existed, center_x, center_y = self.find_image_in_image(cropped_img)
                else:
                    existed = self.check_image(screen)

                center_x = (self.region['left'] + self.region['right']) // 2
                center_y = (self.region['top'] + self.region['bottom']) // 2
            elif self.method == "find" or self.method == "swipe_find":
                existed, center_x, center_y = self.find_image_in_image(screen)
                width = (self.region['right'] - self.region['left']) // 2
                height = (self.region['bottom'] - self.region['top']) // 2
                region = {
                    'left':center_x - width,
                    'right':center_x + width,
                    'bottom':center_y + height,
                    'top':center_y - height,
                }
        if Create_new_config and existed:
            self.ChangeFormat(region,self.config,new_picture_container[0])

        return existed, center_x, center_y
    
    def get_countdown_time(self,screen,original_screen=None,region=None):
        """识别屏幕上的倒计时时间，支持多种格式"""
        try:
            if region is None:
                region = self.region
            # 裁剪倒计时区域
            roi = screen[region['top']:region['bottom'], region['left']:region['right']]
            
            # 转换为灰度图
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            # 二值化处理，使用自适应阈值以提高文字识别率
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # 使用OCR识别文字，配置为识别数字和冒号
            text = pytesseract.image_to_string(
                binary,
                config='--psm 7 -c tessedit_char_whitelist=0123456789:'
            ).strip()
            
            log(f"识别到的原始倒计时文本: {text}")
            
            # 保存识别区域的图片（用于调试）
            self.save_image(binary, 'countdown')
            
            # 清理文本，只保留数字和冒号
            cleaned_text = ''.join(char for char in text if char.isdigit() or char == ':')
            log(f"清理后的文本: {cleaned_text}")
            
            # 处理不同格式的时间字符串
            if ':' in cleaned_text:
                # 处理包含冒号的格式 (HH:MM:SS 或 MM:SS)
                parts = cleaned_text.split(':')
                if len(parts) == 3:
                    # HH:MM:SS 格式
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])
                elif len(parts) == 2:
                    # MM:SS 格式
                    hours = 0
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                else:
                    log(f"无效的时间格式: {cleaned_text}")
                    return None
            else:
                # 处理无冒号的纯数字格式
                if len(cleaned_text) == 6:
                    # HHMMSS 格式
                    hours = int(cleaned_text[:2])
                    minutes = int(cleaned_text[2:4])
                    seconds = int(cleaned_text[4:])
                elif len(cleaned_text) == 4:
                    # MMSS 格式
                    hours = 0
                    minutes = int(cleaned_text[:2])
                    seconds = int(cleaned_text[2:])
                else:
                    log(f"无法解析的时间格式: {cleaned_text}")
                    return None
            
            # 验证时间值的合理性
            if hours >= 0 and minutes >= 0 and minutes < 60 and seconds >= 0 and seconds < 60:
                total_seconds = hours * 3600 + minutes * 60 + seconds
                log(f"解析倒计时: {hours}时{minutes}分{seconds}秒，共{total_seconds}秒")
                if Create_new_config:
                    self.ChangeFormat(region,self.config,original_screen)
                return total_seconds
            else:
                log(f"时间值超出范围: {hours}:{minutes}:{seconds}")
                return None
            
        except Exception as e:
            log(f"倒计时识别失败: {e}")
            import traceback
            traceback.print_exc()
            return None

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
                

                center_x = (region['left'] + region['right']) / 2 / screen_width
                center_y = (region['top'] + region['bottom']) / 2 / screen_height
                lable_h = (region['bottom'] - region['top']) / screen_height
                lable_w = (region['right'] - region['left']) / screen_width
                lable_str = f"{center_x:.2f} {center_y:.2f} {lable_w:.2f} {lable_h:.2f}"

                prefix = "matched" if max_val > threshold else "unmatched"
                prefix = f"{prefix}_{max_val:.2f}"

                if self.save_images:
                    matched_image_path = self.save_image(screen, prefix=prefix, image_lable=lable_str)
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
        # self.save_image(screen_bgr, 'screen')
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

        screen_height, screen_width = screen.shape[:2]
        lable_center_x = center_x / screen_width
        lable_center_y = center_y / screen_height
        lable_h = h / screen_height
        lable_w = w / screen_width

        lable_str = f"{lable_center_x:.2f} {lable_center_y:.2f} {lable_w:.2f} {lable_h:.2f}"

        find = max_val > threshold
        if find:
            
            if self.save_images:
                matched_image_path = self.save_image(screen_bgr, f'matched_{max_val:.2f}', image_lable=lable_str)
            # 如果启用了通知
            if notify:                
                task_info = f"\n任务名称: {task_name}" if task_name else ""
                message = f"图片匹配成功！{task_info}\n匹配度: {max_val:.2f}\n阈值: {threshold}\n点击位置: ({center_x}, {center_y})"
                # send_notification(message, matched_image_path)
        else:
            log(f"未找到匹配图片，最佳匹配度: {max_val}")
                    
            
        return find, center_x, center_y

    def ChangeFormat(self,region,config,New_picture):
        new_config = config
        x_converter = lambda x:int(New_width / Capture_width * x)
        y_converter = lambda y:int(New_height / Capture_height * y)
        left = x_converter(region.get("left",-1))
        top = y_converter(region.get("top",-1))
        right = x_converter(region.get("right",-1))
        bottom = y_converter(region.get("bottom",-1))
        swipe_config = config.get("swipe",None)
    
        if not swipe_config is None:
            start_x = swipe_config["start"]["x"]
            start_x = x_converter(start_x)
            start_y = swipe_config["start"]["y"]
            start_y = y_converter(start_y)
            end_x = swipe_config["end"]["x"]
            end_x = x_converter(end_x)
            end_y = swipe_config["end"]["y"]
            end_y = y_converter(end_y)


            new_swipe_config = {
                "start": {"x": start_x, "y": start_y},
                "end": {"x": end_x, "y": end_y},
                "duration": swipe_config["duration"],  # 转换为毫秒
            }
        else:
            new_swipe_config = None
        new_config ={
                "method":config["method"],
                "window_name": config["window_name"],
                "picture_path": config["picture_path"],
                "region": {
                    "left": left , # 左边界X坐标
                    "top": top , # 上边界Y坐标
                    "right": right ,# 右边界X坐标
                    "bottom": bottom ,# 下边界Y坐标 
                },
                "threshold": config["threshold"],
                "defult_click_point": {
                    "x": (left + right) // 2,
                    "y": (top + bottom) // 2,
                },
                "swipe": new_swipe_config,
            }

        
        if new_config["method"] != "None":
            region=new_config['region']
            path = config["picture_path"]
            picture_path = os.path.join(os.path.dirname(path), "newconfig", os.path.basename(path))
            cropped_img = New_picture[region['top']:region['bottom'], region['left']:region['right']]
            cv2.imwrite(picture_path, cropped_img)
        path = self.config["config_file"]
        config_path = os.path.join(os.path.dirname(path), "newconfig", os.path.basename(path))
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        # Save the region dictionary to a YAML config file
        with open(config_path, 'w') as file:
            yaml.dump(new_config, file, default_flow_style=False)
            

    def save_image(self, image, prefix='cropped', image_lable=None,save_path=None): 
        """保存图片到指定目录"""
        # 如果未启用图片保存，直接返回
        if not self.save_images:
            return None
        
        if save_path is None:
            save_path = self.save_path

        try:
            # 确保保存目录存在
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            # 生成文件名，包含时间戳
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{save_path}/{prefix}_{timestamp}.png'
            
            # 保存图片
            cv2.imwrite(filename, image)
            log(f"调试图片已保存: {filename}")

            if image_lable is not None:
                # 保存标签文件
                if not os.path.exists(self.label_path):
                    os.makedirs(self.label_path)

                label_filename = f'{self.label_path}/{prefix}_{timestamp}.txt'
                with open(label_filename, 'w') as f:
                    f.write(image_lable)
                log(f"标签文件已保存: {label_filename}")

            
            return filename
        except Exception as e:
            log(f"保存调试图片失败: {e}")
            return None
