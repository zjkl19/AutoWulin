import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json5
import os
import sys
import shutil
import logging
import threading
import time
# 添加src目录到sys.path中
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from auto_whack_a_mole import AutoWhackAMole

class AutoWulinApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoWulin 自动武林")
        self.geometry("800x600")

        # 加载配置文件
        with open('./config.json5', 'r', encoding='utf-8') as f:
            self.config = json5.load(f)

        self.config_path = './config.json5'
        self.config_backup_path = f'./config_backup_{int(time.time())}.json5'

        # 创建多标签界面
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # 创建标签页
        self.create_whack_a_mole_tab()
        self.create_fishing_tab()
        self.create_herb_collecting_tab()
        self.create_gambling_tab()
        self.create_config_tab()

    def create_whack_a_mole_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="自动打地鼠")

        # 阈值设置
        ttk.Label(tab, text="阈值:").grid(row=0, column=0, padx=10, pady=10)
        self.whack_a_mole_threshold = tk.DoubleVar(value=self.config['whack_a_mole']['threshold'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_threshold).grid(row=0, column=1, padx=10, pady=10)

        # 时间限制设置
        ttk.Label(tab, text="时间限制 (秒):").grid(row=1, column=0, padx=10, pady=10)
        self.whack_a_mole_time_limit = tk.IntVar(value=self.config['whack_a_mole']['time_limit'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_time_limit).grid(row=1, column=1, padx=10, pady=10)

        # 间隔时间设置
        ttk.Label(tab, text="间隔时间 (秒):").grid(row=2, column=0, padx=10, pady=10)
        self.whack_a_mole_sleep_interval = tk.DoubleVar(value=self.config['whack_a_mole']['sleep_interval'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_sleep_interval).grid(row=2, column=1, padx=10, pady=10)

        # 单击间隔设置
        ttk.Label(tab, text="单击间隔 (秒):").grid(row=3, column=0, padx=10, pady=10)
        self.whack_a_mole_click_interval = tk.DoubleVar(value=self.config['whack_a_mole']['click_interval'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_click_interval).grid(row=3, column=1, padx=10, pady=10)

        # 是否启用复制窗口
        ttk.Label(tab, text="启用复制窗口:").grid(row=4, column=0, padx=10, pady=10)
        self.enable_copy_window = tk.BooleanVar(value=self.config['whack_a_mole'].get('enable_copy_window', False))
        ttk.Checkbutton(tab, variable=self.enable_copy_window).grid(row=4, column=1, padx=10, pady=10)

        # OCR 判断游戏是否终止
        ttk.Label(tab, text="OCR 判断游戏是否终止:").grid(row=5, column=0, padx=10, pady=10)
        self.enable_ocr_detection = tk.BooleanVar(value=self.config['whack_a_mole'].get('enable_ocr_detection', False))
        ttk.Checkbutton(tab, variable=self.enable_ocr_detection).grid(row=5, column=1, padx=10, pady=10)

       # 物品过滤选项
        item_names = {
            'iron_ore': '铁矿',
            'copper_ore': '铜矿',
            'red_crystal': '红晶矿',
            'black_crystal': '黑晶矿',
            'blue_crystal': '蓝晶矿',
            'white_crystal': '白晶矿',
            'treasure': '宝藏'
        }
        self.item_filters = {
            item: tk.BooleanVar(value=self.config['whack_a_mole'].get(item, False))
            for item in item_names
        }

        row, col = 0, 2
        for index, (item, name) in enumerate(item_names.items()):
            ttk.Checkbutton(tab, text=f"过滤 {name}", variable=self.item_filters[item]).grid(row=row, column=col, padx=10, pady=10, sticky=tk.W)
            if index == 3:
                col = 3
                row = 0
            else:
                row += 1
                
        # 开始按钮
        ttk.Button(tab, text="开始自动打地鼠", command=self.start_whack_a_mole_thread).grid(row=6, column=0, columnspan=4, padx=10, pady=10)


    def save_config(self):
        self.config['whack_a_mole']['threshold'] = self.whack_a_mole_threshold.get()
        self.config['whack_a_mole']['time_limit'] = self.whack_a_mole_time_limit.get()
        self.config['whack_a_mole']['sleep_interval'] = self.whack_a_mole_sleep_interval.get()
        self.config['whack_a_mole']['click_interval'] = self.whack_a_mole_click_interval.get()
        self.config['whack_a_mole']['enable_copy_window'] = self.enable_copy_window.get()
        self.config['whack_a_mole']['enable_ocr_detection'] = self.enable_ocr_detection.get()
        for item, var in self.item_filters.items():
            self.config['whack_a_mole'][item] = var.get()
        with open('./config.json5', 'w', encoding='utf-8') as f:
            json5.dump(self.config, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("保存配置", "配置已保存")

    def backup_config(self):
        import shutil
        shutil.copy('./config.json5', f'./config_backup_{int(time.time())}.json5')
        messagebox.showinfo("备份配置", "配置已备份")

    def start_whack_a_mole(self):
        config = {
            'threshold': self.whack_a_mole_threshold.get(),
            'time_limit': self.whack_a_mole_time_limit.get(),
            'sleep_interval': self.whack_a_mole_sleep_interval.get(),
            'click_interval': self.whack_a_mole_click_interval.get(),
            'enable_copy_window': self.enable_copy_window.get(),
            'enable_ocr_detection': self.enable_ocr_detection.get()
        }
        for item, var in self.item_filters.items():
            config[item] = var.get()
        auto_whack_a_mole = AutoWhackAMole("武林群侠传", config)
        auto_whack_a_mole.start()

    def start_whack_a_mole_thread(self):
        threading.Thread(target=self.start_whack_a_mole).start()

    def create_fishing_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="自动钓鱼")

        ttk.Label(tab, text="时间限制（秒）:").grid(row=0, column=0, padx=10, pady=10)
        self.fishing_time_limit = tk.IntVar(value=self.config['fishing']['time_limit'])
        ttk.Entry(tab, textvariable=self.fishing_time_limit).grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(tab, text="开始", command=self.start_fishing).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def create_herb_collecting_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="自动采药")

        ttk.Label(tab, text="时间限制（秒）:").grid(row=0, column=0, padx=10, pady=10)
        self.herb_collecting_time_limit = tk.IntVar(value=self.config['herb_collecting']['time_limit'])
        ttk.Entry(tab, textvariable=self.herb_collecting_time_limit).grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(tab, text="开始", command=self.start_herb_collecting).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def create_gambling_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="自动赌博")

        ttk.Label(tab, text="时间限制（秒）:").grid(row=0, column=0, padx=10, pady=10)
        self.gambling_time_limit = tk.IntVar(value=self.config['gambling']['time_limit'])
        ttk.Entry(tab, textvariable=self.gambling_time_limit).grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(tab, text="开始", command=self.start_gambling).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def create_config_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="配置管理")

        ttk.Label(tab, text="修改配置文件").grid(row=0, column=0, padx=10, pady=10)
        self.new_config_content = tk.Text(tab, wrap=tk.WORD, height=20, width=80)
        self.new_config_content.insert(tk.END, json5.dumps(self.config, indent=4, ensure_ascii=False))
        self.new_config_content.grid(row=1, column=0, padx=10, pady=10)

        # 添加保存和备份按钮到同一行
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, padx=10, pady=10)
        
        ttk.Button(button_frame, text="保存修改", command=self.save_config).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="备份配置文件", command=self.backup_config).grid(row=0, column=1, padx=5)

    def save_config(self):
        new_config = self.new_config_content.get("1.0", tk.END)
        try:
            new_config_json = json5.loads(new_config)
            # 写入新配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json5.dump(new_config_json, f, indent=4, ensure_ascii=False)
            self.config = new_config_json
            messagebox.showinfo("保存成功", "配置文件已保存。")
            logging.info("配置文件已保存。")
        except json5.JSONDecodeError as e:
            messagebox.showerror("保存失败", f"配置文件格式错误: {e}")
            logging.error(f"配置文件格式错误: {e}")

    def backup_config(self):
        try:
            shutil.copyfile(self.config_path, self.config_backup_path)
            messagebox.showinfo("备份成功", "配置文件已备份。")
            logging.info("配置文件已备份。")
        except Exception as e:
            messagebox.showerror("备份失败", f"备份时出现错误: {e}")
            logging.error(f"备份时出现错误: {e}")

    def start_whack_a_mole(self):
        config = {
            'threshold': self.whack_a_mole_threshold.get(),
            'time_limit': self.whack_a_mole_time_limit.get(),
            'sleep_interval': self.whack_a_mole_sleep_interval.get(),
            'click_interval': self.whack_a_mole_click_interval.get(),
            'enable_copy_window': self.enable_copy_window.get(),
            'enable_ocr_detection': self.enable_ocr_detection.get()
        }
        auto_whack_a_mole = AutoWhackAMole("武林群侠传", config)
        auto_whack_a_mole.start()

    def start_whack_a_mole_thread(self):
        threading.Thread(target=self.start_whack_a_mole).start()

    def start_fishing(self):
        time_limit = self.fishing_time_limit.get()
        # 这里添加自动钓鱼的逻辑
        messagebox.showinfo("启动", f"自动钓鱼已启动\n时间限制: {time_limit} 秒")

    def start_herb_collecting(self):
        time_limit = self.herb_collecting_time_limit.get()
        # 这里添加自动采药的逻辑
        messagebox.showinfo("启动", f"自动采药已启动\n时间限制: {time_limit} 秒")

    def start_gambling(self):
        time_limit = self.gambling_time_limit.get()
        # 这里添加自动赌博的逻辑
        messagebox.showinfo("启动", f"自动赌博已启动\n时间限制: {time_limit} 秒")

if __name__ == "__main__":
    app = AutoWulinApp()
    app.mainloop()
