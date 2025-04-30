import pygetwindow as gw
import pyautogui
import time

class WindowManager:
    def __init__(self):
        self.selected_window = None

    def select_window(self):
        print("请将鼠标移动到目标窗口上，3秒后开始捕获...")
        time.sleep(3)
        x, y = pyautogui.position()
        windows = gw.getWindowsAt(x, y)
        if windows:
            self.selected_window = windows[0]
            print(f"已选择窗口: {self.selected_window.title}")
        else:
            print("未找到窗口，请重试。")

    def get_window_position(self):
        if self.selected_window:
            position = {
                "left": self.selected_window.left,
                "top": self.selected_window.top,
                "width": self.selected_window.width,
                "height": self.selected_window.height
            }
            print(f"窗口位置: {position}")
            return position
        else:
            print("未选择窗口。")
            return None

    def activate_window(self):
        if self.selected_window:
            # 检查窗口句柄是否有效
            if not self.selected_window._hWnd:
                print("窗口句柄无效，请重新选择窗口。")
                return
            
            if self.selected_window.isMinimized:
                print("窗口已最小化，正在恢复...")
                self.selected_window.restore()
            
            try:
                self.selected_window.activate()
                print(f"已激活窗口: {self.selected_window.title}")
            except Exception as e:
                print(f"激活窗口失败: {e}")
        else:
            print("未选择窗口。")

# 示例使用
if __name__ == "__main__":
    manager = WindowManager()
    manager.select_window()
    manager.get_window_position()
    time.sleep(5)  # 等待2秒
    manager.activate_window()
    manager.get_window_position()