import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import os
import threading
import time
import logging
import tkinter as tk
from PIL import Image, ImageTk
import queue
from paddleocr import PaddleOCR

class AutoWhackAMole:
    def __init__(self, game_title, config):
        self.game_title = game_title
        self.window = None
        self.resolution = None
        self.image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images/whack_a_mole'))
        self.time_limit = config['time_limit']
        self.threshold = config['threshold']
        self.sleep_interval = config.get('sleep_interval', 0.03)
        self.click_interval = config.get('click_interval', 0.03)
        self.enable_copy_window = config.get('enable_copy_window', False)
        self.enable_ocr_detection = config.get('enable_ocr_detection', False)
        self.start_time = None
        self.default_resolution = (656, 539)
        self.running = True
        self.update_queue = queue.Queue()

        # 日志设置
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(filename=os.path.join(log_dir, 'auto_whack_a_mole.log'), level=logging.INFO)

        if self.enable_copy_window:
            self.init_copy_window()

        # 初始化OCR对象，指定本地模型路径
        self.ocr = PaddleOCR(det_model_dir='./inference/ch_ppocr_server_v2.0_det_infer',
                             rec_model_dir='./inference/ch_ppocr_server_v2.0_rec_infer',
                             cls_model_dir='./inference/ch_ppocr_mobile_v2.0_cls_infer',
                             use_angle_cls=True, lang='ch')

        # 获取窗口分辨率
        self.get_window_resolution()

    def init_copy_window(self):
        self.copy_root = tk.Tk()
        self.copy_root.title("复制窗口")
        self.copy_label = tk.Label(self.copy_root)
        self.copy_label.pack()
        self.copy_root.after(100, self.process_queue)

    def process_queue(self):
        try:
            while not self.update_queue.empty():
                image = self.update_queue.get_nowait()
                img = Image.fromarray(image)
                img_tk = ImageTk.PhotoImage(img)
                self.copy_label.config(image=img_tk)
                self.copy_label.image = img_tk
        except queue.Empty:
            pass
        self.copy_root.after(100, self.process_queue)

    def update_copy_window(self, image):
        if self.enable_copy_window:
            self.update_queue.put(image)

    def get_window_resolution(self):
        windows = gw.getWindowsWithTitle(self.game_title)
        if windows:
            self.window = windows[0]
            self.resolution = (self.window.width, self.window.height)
            logging.info(f"找到窗口 {self.game_title}，分辨率: {self.resolution}")
            return self.resolution
        else:
            raise Exception(f"未找到标题为 {self.game_title} 的窗口。")

    def capture_screen(self):
        if self.window:
            screenshot = pyautogui.screenshot(region=(
                self.window.left,
                self.window.top,
                self.window.width,
                self.window.height
            ))
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            return screenshot
        else:
            raise Exception("未找到窗口，无法截屏。")

    def load_templates(self):
        templates = {}
        scaling_factor_x = self.resolution[0] / self.default_resolution[0]
        scaling_factor_y = self.resolution[1] / self.default_resolution[1]

        def load_and_resize(image_name):
            image = cv2.imread(os.path.join(self.image_dir, image_name), 0)
            resized_image = cv2.resize(image, (0, 0), fx=scaling_factor_x, fy=scaling_factor_y)
            return resized_image

        templates['snake'] = load_and_resize('snake.png')
        templates['female_mole'] = load_and_resize('female_mole.png')
        templates['iron_ore'] = load_and_resize('iron_ore.png')
        return templates

    def find_moles_and_snakes(self, screenshot, templates):
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        results = []
        for name, template in templates.items():
            res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.threshold)
            for pt in zip(*loc[::-1]):
                results.append((name, pt))
        return results

    def whack_mole(self, position):
        click_x = self.window.left + position[0]
        click_y = self.window.top + position[1]
        pyautogui.moveTo(click_x, click_y)
        pyautogui.mouseDown()
        time.sleep(self.click_interval)  # 使用配置文件中的 click_interval
        pyautogui.mouseUp()
        # 将鼠标移到窗口的右下角
        pyautogui.moveTo(self.window.left + self.window.width - 10, self.window.top + self.window.height - 10)

    def run_game_logic(self):
        def time_limit_exceeded():
            time.sleep(self.time_limit)
            print("时间已到。退出程序...")
            logging.info("时间已到。退出程序...")
            self.running = False

        def ocr_check():
            screenshot_counter = 0
            while self.running:
                screenshot = self.capture_screen()
                region = screenshot[int(self.resolution[1] * 2 / 3):, :int(self.resolution[0] / 4)]
                
                # 保存调试截图
                screenshot_counter += 1
                debug_image_path = os.path.join("debug_screenshots", f"ocr_debug_{screenshot_counter}.png")
                os.makedirs(os.path.dirname(debug_image_path), exist_ok=True)
                cv2.imwrite(debug_image_path, region)
                logging.info(f"保存调试截图: {debug_image_path}")

                result = self.ocr.ocr(region, cls=True)
                logging.info(f"OCR结果: {result}")
                
                # 检查OCR结果是否为None
                if result is None:
                    logging.warning("OCR结果为None")
                    continue

                for line in result:
                    if line is None:
                        continue
                    for word in line:
                        if word is None:
                            continue
                        if '回合终了' in word[1][0]:
                            print("检测到'回合终了'，脚本终止")
                            logging.info("检测到'回合终了'，脚本终止")
                            self.running = False
                            return
                time.sleep(1)  # 每秒检查一次

        self.start_time = time.time()
        logging.info(f"游戏开始时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time))}")

        timer_thread = threading.Thread(target=time_limit_exceeded)
        timer_thread.daemon = True
        timer_thread.start()

        if self.enable_ocr_detection:
            ocr_thread = threading.Thread(target=ocr_check)
            ocr_thread.daemon = True
            ocr_thread.start()

        try:
            resolution = self.get_window_resolution()
            logging.info(f"游戏分辨率: {resolution}")
            print(f"游戏分辨率: {resolution}")

            screen_width, screen_height = pyautogui.size()
            if self.enable_copy_window:
                if self.window.left + self.window.width + resolution[0] > screen_width:
                    print("警告：游戏窗口太大，复制窗口放不下！")
                    logging.warning("游戏窗口太大，复制窗口放不下！")
                    self.enable_copy_window = False  # 禁用复制窗口
                else:
                    self.copy_root.geometry(f"{resolution[0]}x{resolution[1]}+{self.window.left + self.window.width + 10}+{self.window.top}")

            templates = self.load_templates()

            while self.running:
                screenshot = self.capture_screen()
                results = self.find_moles_and_snakes(screenshot, templates)
                for name, position in results:
                    if name == 'iron_ore' or name == 'snake':
                        self.whack_mole(position)
                        # 框出特征物体
                        cv2.rectangle(screenshot, position, (position[0] + templates[name].shape[1], position[1] + templates[name].shape[0]), (0, 255, 0), 2)
                self.update_copy_window(screenshot)
                time.sleep(self.sleep_interval)  # 使用配置文件中的 sleep_interval

        except Exception as e:
            logging.error(f"错误: {e}")
            print(f"错误: {e}")

    def start(self):
        if self.enable_copy_window:
            threading.Thread(target=self.copy_root.mainloop).start()
        
        game_logic_thread = threading.Thread(target=self.run_game_logic)
        game_logic_thread.start()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(script_dir, '../config.json5'))
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    auto_whack_a_mole = AutoWhackAMole("武林群侠传", config['whack_a_mole'])
    auto_whack_a_mole.start()
