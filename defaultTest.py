import pyautogui
from Wulin import Wulin
import time
import pyautogui
import logging

#游戏进入到主角在草丛下方时，启动脚本，需要保证游戏窗口在IDE窗口下一层，且游戏窗口没有被拉伸
delayTime=1

#https://blog.csdn.net/weixin_41010198/article/details/89356417
level = logging.DEBUG # DEBUG、INFO、WARNING、ERROR、CRITICAL
logging.basicConfig(level=level)


pyautogui.moveTo(1802,15)    #移动到IDE最小化位置
time.sleep(delayTime)
pyautogui.click()

p = pyautogui.locateOnScreen(r'.\Images\Quantity.png')
print(p)