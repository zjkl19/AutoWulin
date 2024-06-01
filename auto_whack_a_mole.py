import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import os
import threading
import time

class AutoWhackAMole:
    def __init__(self, game_title, time_limit):
        self.game_title = game_title
        self.window = None
        self.resolution = None
        self.image_dir = "images"
        self.time_limit = time_limit
        self.start_time = None
        self.default_resolution = (656, 539)  # 默认分辨率

    def get_window_resolution(self):
        windows = gw.getWindowsWithTitle(self.game_title)
        if windows:
            self.window = windows[0]
            self.resolution = (self.window.width, self.window.height)
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
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                results.append((name, pt))
        return results

    def whack_mole(self, position):
        click_x = self.window.left + position[0]
        click_y = self.window.top + position[1]
        pyautogui.moveTo(click_x, click_y)
        pyautogui.mouseDown()
        time.sleep(0.03) 
        pyautogui.mouseUp()

    def run(self):
        def time_limit_exceeded():
            time.sleep(self.time_limit)
            print("时间已到。退出程序...")
            os._exit(0)

        self.start_time = time.time()
        timer_thread = threading.Thread(target=time_limit_exceeded)
        timer_thread.daemon = True
        timer_thread.start()

        try:
            resolution = self.get_window_resolution()
            print(f"游戏分辨率: {resolution}")
            templates = self.load_templates()
            while True:
                screenshot = self.capture_screen()
                results = self.find_moles_and_snakes(screenshot, templates)
                for name, position in results:
                    if name == 'iron_ore':
                        self.whack_mole(position)
                    if name == 'snake':
                        self.whack_mole(position)
                time.sleep(0.03)  # 增加时间间隔
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    time_limit = int(input("请输入时间限制（秒）: "))
    auto_whack_a_mole = AutoWhackAMole("武林群侠传", time_limit)
    auto_whack_a_mole.run()
