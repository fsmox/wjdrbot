import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import simpledialog, messagebox
import threading
import datetime
from Cure import CureAssist  # 假设有一个CureAssist模块处理治疗辅助逻辑
from task_manager import *

class Task:
    def __init__(self, name, scheduler=None, config=None):
        self.name = name
        self.running = False
        self.scheduler = scheduler  # 传入调度器实例

    def start(self):
        self.running = True
        if self.scheduler:
            self.scheduler.resume()  # 恢复调度器

    def stop(self):
        self.running = False
        if self.scheduler:
            self.scheduler.pause()  # 暂停调度器

    def configure(self, parent):
        new_window = tk.Toplevel(parent)
        new_window.title(f"{self.name} 配置窗口")
        tk.Label(new_window, text=f"正在为 {self.name} 配置参数", font=("Arial", 12, "bold")).pack(pady=10)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("按钮与输出界面")
        self.geometry("900x500")

        # 设置主窗口为2行1列，底部按钮栏在第2行
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)



        # 主内容区（左侧+右侧）
        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")


        # self.config_frame = tk.Frame(self, borderwidth=2, relief="groove")
        # self.config_frame.place(relx=0.5, rely=0.5, anchor="center")
        # self.config_frame.place_forget()  # 初始隐藏
        # self.config_frame.place(relx=0.5, rely=0.5, anchor="center")
        scheduler = SetSchedulerAndTaskListWindow()
        scheduler.pause()
        # 假设有多个游戏窗口
        self.window_names = ["原始", "#1", "#2", "#3"]
        self.window_tasks = {
            "原始": [Task("一键挂机",scheduler), Task("任务B"), Task("任务C")],
            "#1": [Task("任务A"), Task("任务B"), Task("任务C")],
            "#2": [Task("任务A"), Task("任务B"), Task("任务C")],
            "#3": [Task("任务A"), Task("任务B"), Task("任务C")]
        }

        # 当前选择的窗口
        self.current_window = tk.StringVar(value=self.window_names[0])

        # 左侧主区域
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 右侧输出区域
        output_frame = tk.Frame(main_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输出文本框（占右侧上方2/3）
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Arial", 12), height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # 已添加任务及下次执行时间（右侧下方1/3）
        self.task_info_frame = tk.Frame(output_frame, height=1)
        self.task_info_frame.pack(fill=tk.X, side=tk.BOTTOM, anchor="s")
        
        # 添加滚动条
        task_info_scrollbar = tk.Scrollbar(self.task_info_frame, orient=tk.VERTICAL)
        self.task_info_tree = ttk.Treeview(self.task_info_frame, columns=("任务ID", "下次执行时间"), show="headings",yscrollcommand=task_info_scrollbar.set)
        self.task_info_tree.heading("任务ID", text="任务ID")
        self.task_info_tree.heading("下次执行时间", text="下次执行时间")
        task_info_scrollbar.config(command=self.task_info_tree.yview)
        self.task_info_tree.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor="w")
        task_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)





        # 顶部窗口选择按钮
        window_btn_frame = tk.Frame(left_frame)
        window_btn_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(window_btn_frame, text="游戏分身ID", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        for win_name in self.window_names:
            btn = tk.Radiobutton(window_btn_frame, text=win_name, variable=self.current_window, value=win_name, indicatoron=0, width=8, command=self.switch_window)
            btn.pack(side=tk.LEFT, padx=2)

        # 书签式任务按钮区域
        self.notebook = tk.Frame(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.task_buttons = {}
        self.task_config_buttons = {}
        self.task_label_widgets = {}

        self.create_task_page(self.current_window.get())



        self.update_task_info()

        # 全局按钮栏
        global_btn_frame = tk.Frame(self)
        global_btn_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.CrueAssist_button = tk.Button(global_btn_frame, text="治疗辅助开始", width=12, command=self.global_CrueAssist)
        self.CrueAssist_button.pack(side=tk.LEFT, padx=10)
        
        self.CrueAssist = CureAssist()
        self.CrueAssist.run = False  # 初始化治疗辅助状态
        tk.Button(global_btn_frame, text="预留位", width=12, command=self.global_stop).pack(side=tk.LEFT, padx=10)
        tk.Button(global_btn_frame, text="预留位", width=12, command=self.global_config).pack(side=tk.LEFT, padx=10)
        tk.Button(global_btn_frame, text="预留位", width=12, command=self.quit).pack(side=tk.RIGHT, padx=10)

    def create_task_page(self, window_name):
        # 清除旧的任务按钮
        for widget in self.notebook.winfo_children():
            widget.destroy()
        self.task_buttons.clear()
        self.task_config_buttons.clear()
        self.task_label_widgets.clear()

        tasks = self.window_tasks[window_name]
        for idx, task in enumerate(tasks):
            row_frame = tk.Frame(self.notebook)
            row_frame.pack(fill=tk.X, pady=5)

            # 任务名标签
            name_label = tk.Label(row_frame, text=task.name, width=8, anchor="w")
            name_label.pack(side=tk.LEFT)
            self.task_label_widgets[task] = name_label

            # 启动/停止按钮
            btn = tk.Button(row_frame, text="启动", width=8,
                            command=lambda t=task, b_idx=idx: self.toggle_task(t, b_idx))
            btn.pack(side=tk.LEFT, padx=5)
            self.task_buttons[task] = btn

            # 配置按钮
            config_btn = tk.Button(row_frame, text="自动执行配置", width=12,
                                   command=lambda t=task: t.configure(self))
            config_btn.pack(side=tk.LEFT, padx=5)
            self.task_config_buttons[task] = config_btn

    def switch_window(self):
        self.create_task_page(self.current_window.get())
        self.update_task_info()

    def show_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def toggle_task(self, task, btn_idx):
        btn = self.task_buttons[task]
        if not task.running:
            task.start()
            btn.config(text="停止")
        else:
            task.stop()
            btn.config(text="启动")
        self.update_task_info()

    def update_task_info(self):
        update_task_tree(self.task_info_tree)
        # self.task_info_list.delete(0, tk.END)
        # for win_name in self.window_names:
        #     for task in self.window_tasks[win_name]:
        #         if task.running and task.next_run_time:
        #             next_time = task.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
        #             self.task_info_list.insert(tk.END, f"{win_name} - {task.name} - 下次执行: {next_time}")
        #         elif task.running:
        #             self.task_info_list.insert(tk.END, f"{win_name} - {task.name} - 正在运行")
        self.after(1000, self.update_task_info)

    # 示例全局功能方法
    def global_CrueAssist(self):
        
        if self.CrueAssist.run:
            self.CrueAssist.run = False
            self.CrueAssist_button.config(text = "治疗辅助开始")
            self.show_output("治疗辅助已停止")
        else:
            self.CrueAssist.run = True
            self.CrueAssist_button.config(text = "治疗辅助停止")
            self.show_output("治疗辅助已开始")
            # 这里可以添加实际的治疗辅助逻辑
        self.update_task_info()

    def global_stop(self):
        self.show_output("全局停止：所有任务停止")
        for win_name in self.window_names:
            for idx, task in enumerate(self.window_tasks[win_name]):
                if task.running:
                    task.stop()
                    if task in self.task_buttons:
                        self.task_buttons[task].config(text="启动")
        self.update_task_info()

    def global_config(self):
        self.show_output("全局配置：请逐个配置任务")
        for win_name in self.window_names:
            for task in self.window_tasks[win_name]:
                task.configure(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()