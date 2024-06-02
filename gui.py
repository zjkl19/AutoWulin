import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import sys
import shutil
import logging

# 添加src目录到sys.path中
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from auto_whack_a_mole import AutoWhackAMole

class AutoWulinApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoWulin 自动武林")
        self.geometry("600x400")

        # 日志设置
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(filename=os.path.join(log_dir, 'gui.log'), level=logging.INFO)

        # 加载配置文件
        config_path = os.path.abspath('./config.json')
        self.config_backup_path = os.path.abspath('./config_backup.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.config_path = config_path

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

        ttk.Label(tab, text="阈值:").grid(row=0, column=0, padx=10, pady=10)
        self.whack_a_mole_threshold = tk.DoubleVar(value=self.config['whack_a_mole']['threshold'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_threshold).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(tab, text="时间限制（秒）:").grid(row=1, column=0, padx=10, pady=10)
        self.whack_a_mole_time_limit = tk.IntVar(value=self.config['whack_a_mole']['time_limit'])
        ttk.Entry(tab, textvariable=self.whack_a_mole_time_limit).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(tab, text="休眠间隔（秒）:").grid(row=2, column=0, padx=10, pady=10)
        self.whack_a_mole_sleep_interval = tk.DoubleVar(value=self.config['whack_a_mole'].get('sleep_interval', 0.03))
        ttk.Entry(tab, textvariable=self.whack_a_mole_sleep_interval).grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(tab, text="点击间隔（秒）:").grid(row=3, column=0, padx=10, pady=10)
        self.whack_a_mole_click_interval = tk.DoubleVar(value=self.config['whack_a_mole'].get('click_interval', 0.03))
        ttk.Entry(tab, textvariable=self.whack_a_mole_click_interval).grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(tab, text="开始", command=self.start_whack_a_mole).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

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
        self.new_config_content.insert(tk.END, json.dumps(self.config, indent=4, ensure_ascii=False))
        self.new_config_content.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(tab, text="保存修改", command=self.save_config).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(tab, text="备份日志文件", command=self.backup_config).grid(row=3, column=0, padx=10, pady=10)

    def save_config(self):
        new_config = self.new_config_content.get("1.0", tk.END)
        try:
            new_config_json = json.loads(new_config)
            # 备份现有配置文件
            shutil.copyfile(self.config_path, self.config_backup_path)
            # 写入新配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config_json, f, indent=4, ensure_ascii=False)
            self.config = new_config_json
            messagebox.showinfo("保存成功", "配置文件已保存并备份。")
            logging.info("配置文件已保存并备份。")
        except json.JSONDecodeError as e:
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
            'click_interval': self.whack_a_mole_click_interval.get()
        }
        # 这里添加自动打地鼠的逻辑
        auto_whack_a_mole = AutoWhackAMole("武林群侠传", config)
        auto_whack_a_mole.run()

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
