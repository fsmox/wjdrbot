import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from skimage.measure import label, regionprops
from windows_controller import WindowsController
import yaml

# 截图 + 边缘检测 + 连通区域
controller = WindowsController()
screenshot = controller.screenshot()  # PIL.Image
img_rgb = np.array(screenshot)
gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2)
labeled = label(closed > 0)

# 图像尺寸
img_h, img_w = img_rgb.shape[:2]

# 初始化窗口
root = tk.Tk()
root.title("GUI Block Detector")

# 左侧图像Canvas
canvas = tk.Canvas(root, width=img_w, height=img_h)
canvas.grid(row=0, column=0, rowspan=10)

# 显示图像
tk_img = ImageTk.PhotoImage(Image.fromarray(img_rgb))
canvas_img = canvas.create_image(0, 0, anchor="nw", image=tk_img)

# 输入框
tk.Label(root, text="输入标注或备注:").grid(row=0, column=1, sticky="w")
entry = tk.Entry(root, width=30)
entry.grid(row=1, column=1, sticky="w")

# 图标块预览列表
preview_labels = []

# 框列表
bounding_boxes = []


from enum import Enum

class JudgeType(Enum):
    CHECK = "check"
    SEARCH = "find"
    SWIPE_SERACH = "swipe_find"
    SWIPE_CHECK = "swipe_check"
    OCR = "ocr"
    NONE = "None"

# 创建JudgeType多选项
judge_type_var = tk.StringVar(value=JudgeType.CHECK.value)
tk.Label(root, text="检测方法:").grid(row=2, column=2, sticky="w")
judge_type_menu = ttk.Combobox(
    root,
    textvariable=judge_type_var,
    values=[jt.value for jt in JudgeType],
    state="readonly",
    width=18
)
judge_type_menu.grid(row=3, column=2, sticky="w")


def recapture_image():
    global screenshot, img_rgb, gray, blurred, edges, closed, labeled, tk_img
    # 重新截图
    screenshot = controller.screenshot()
    img_rgb = np.array(screenshot)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=2)
    labeled = label(closed > 0)
    # 更新canvas图片
    tk_img = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    canvas.itemconfig(canvas_img, image=tk_img)
    # 清除已选框和预览
    clear_boxes_and_previews()

recapture_button = tk.Button(root, text="重新捕获图片", command=recapture_image)
recapture_button.grid(row=5, column=2, sticky="w")
# 保存按钮
def on_save_button_click():
    if not bounding_boxes:
        print("请先选择一个区域")
        return
    # 取最后一个框
    box_id = bounding_boxes[-1]
    x1, y1, x2, y2 = map(int, canvas.coords(box_id))
    save_Lable(img_rgb, (x1, y1, x2, y2))

save_button = tk.Button(root, text="保存标注", command=on_save_button_click)
save_button.grid(row=4, column=2, sticky="w")

# 添加点击选项框（单选框），选项为 open 和 window
click_mode_var = tk.StringVar(value="open")
tk.Label(root, text="点击类型:").grid(row=6, column=1, sticky="w")
open_radio = tk.Radiobutton(root, text="open", variable=click_mode_var, value="open")
open_radio.grid(row=7, column=1, sticky="w")
window_radio = tk.Radiobutton(root, text="window", variable=click_mode_var, value="window")
window_radio.grid(row=8, column=1, sticky="w")

def save_Lable(label_img, box, swipe_config =None):

    
    window_name = task_entry_task_name.get()
    step = step_entry.get()
    # 判断 open_radio 还是 window_radio 被选中
    click_type = click_mode_var.get()

    if not window_name:
        print("请先输入任务名")
        return
    name = f"{window_name}_{step}_{click_type}"
    picture_path = f"images/{name}.png"
    config_path = f"images/{name}_config.yaml"
    method = JudgeType(judge_type_var.get())
    # method = JudgeType.CHECK

    left, top, right, bottom = box



    # swipe = {
    #     "start": {
    #         "x": 160,
    #         "y": 540,
    #     },
    #     "end": {
    #         "x": 162,
    #         "y": 300,
    #     },
    #     "duration": 0.5,
    # }
    config ={
        "method":method.value,
        "window_name": window_name,
        "picture_path": picture_path,
        "region": {
            "left": left , # 左边界X坐标
            "top": top , # 上边界Y坐标
            "right": right ,# 右边界X坐标
            "bottom": bottom ,# 下边界Y坐标 
        },
        "threshold": 0.8,
        "defult_click_point": {
            "x": (left + right) // 2,
            "y": (top + bottom) // 2,
        },
        "swipe": swipe_config,
    }
    region=config['region']
    cropped_img = label_img[region['top']:region['bottom'], region['left']:region['right']]
    cv2.imwrite(picture_path, cropped_img)
    # Save the region dictionary to a YAML config file
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def clear_boxes_and_previews():
    for box in bounding_boxes:
        canvas.delete(box)
    bounding_boxes.clear()

    for label in preview_labels:
        label.destroy()
    preview_labels.clear()

def on_click(event):
    if mode_var.get() == "manual":
        return  # 手动模式下不响应自动检测
    x, y = int(event.x), int(event.y)
    if event.num == 3:  # 右键清除
        clear_boxes_and_previews()
        return
    label_id = labeled[y, x]
    if label_id == 0:
        print("点击区域没有目标")
        return
    for prop in regionprops(labeled):
        if prop.label == label_id:
            minr, minc, maxr, maxc = prop.bbox
            box = canvas.create_rectangle(minc, minr, maxc, maxr, outline="red", width=2)
            bounding_boxes.append(box)
            crop = img_rgb[minr:maxr, minc:maxc]
            pil_crop = Image.fromarray(crop).resize((100, 100))
            preview = ImageTk.PhotoImage(pil_crop)
            label = tk.Label(root, image=preview)
            label.image = preview
            label.grid(row=2 + len(preview_labels), column=1, sticky="w")
            preview_labels.append(label)
            text = entry.get()
            print(f"你输入的备注：{text}")
            method = JudgeType(judge_type_var.get())
            print(f"检测方法：{method.value}")
            break

# 任务名输入框
tk.Label(root, text="任务名:").grid(row=0, column=2, sticky="w")
task_entry_task_name = tk.Entry(root, width=20)
task_entry_task_name.grid(row=1, column=2, sticky="w")

# 当前Step输入框
tk.Label(root, text="当前Step:").grid(row=2, column=1, sticky="w")
step_entry = tk.Entry(root, width=20)
step_entry.insert(0, "Step1")
step_entry.grid(row=3, column=1, sticky="w")

# 增加模式选择
mode_var = tk.StringVar(value="auto")
tk.Label(root, text="标注模式:").grid(row=6, column=2, sticky="w")
mode_menu = ttk.Combobox(
    root,
    textvariable=mode_var,
    values=["auto", "manual"],
    state="readonly",
    width=18
)
mode_menu.grid(row=7, column=2, sticky="w")

# 手动画框相关变量
manual_box_start = [None, None]
manual_box_rect = [None]

def on_canvas_press(event):
    if mode_var.get() != "manual":
        return
    clear_boxes_and_previews()
    manual_box_start[0], manual_box_start[1] = event.x, event.y
    manual_box_rect[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="blue", width=2)

def on_canvas_drag(event):
    if mode_var.get() != "manual" or manual_box_rect[0] is None:
        return
    canvas.coords(manual_box_rect[0], manual_box_start[0], manual_box_start[1], event.x, event.y)

def on_canvas_release(event):
    if mode_var.get() != "manual" or manual_box_rect[0] is None:
        return
    x1, y1 = manual_box_start
    x2, y2 = event.x, event.y
    # 规范化坐标
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    canvas.coords(manual_box_rect[0], x1, y1, x2, y2)
    bounding_boxes.append(manual_box_rect[0])

    # 显示预览
    crop = img_rgb[y1:y2, x1:x2]
    pil_crop = Image.fromarray(crop).resize((100, 100))
    preview = ImageTk.PhotoImage(pil_crop)
    label = tk.Label(root, image=preview)
    label.image = preview
    label.grid(row=2 + len(preview_labels), column=1, sticky="w")
    preview_labels.append(label)

    # 输出备注
    text = entry.get()
    print(f"你输入的备注：{text}")
    method = JudgeType(judge_type_var.get())
    print(f"检测方法：{method.value}")


def bind_canvas_events(*args):
    # 先解绑所有相关事件
    canvas.unbind("<Button-1>")
    canvas.unbind("<Button-3>")
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if mode_var.get() == "manual":
        # 手动模式绑定画框相关
        canvas.bind("<ButtonPress-1>", on_canvas_press)
        canvas.bind("<B1-Motion>", on_canvas_drag)
        canvas.bind("<ButtonRelease-1>", on_canvas_release)
        canvas.bind("<Button-3>", on_click)  # 右键清除
    else:
        # 自动模式绑定点击检测
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Button-3>", on_click)  # 右键清除

# 绑定模式切换事件
mode_menu.bind("<<ComboboxSelected>>", bind_canvas_events)
# 初始化时也绑定一次
bind_canvas_events()

from GameController import GameController


def test_data():
    # 读取配置文件
    window_name = task_entry_task_name.get()
    step = step_entry.get()
    window_name = f"{window_name}_{step}"

    game_controller = GameController(windwow_controller=controller) 

    game_controller.RegisterWindow(window_name)
    test_window = game_controller.GameWindows[window_name]
    test_window.open()
    

test_button = tk.Button(root, text="数据测试", command=test_data)
test_button.grid(row=9, column=2, sticky="w")

root.mainloop()
