# -*- coding: utf-8 -*-
from Wulin import Wulin
import pytesseract
import cv2
import time
import pyautogui
import logging

#游戏进入到主角在草丛下方时，启动脚本，需要保证游戏窗口在IDE窗口下一层，且游戏窗口没有被拉伸
delayTime=1

#https://blog.csdn.net/weixin_41010198/article/details/89356417
level = logging.DEBUG # DEBUG、INFO、WARNING、ERROR、CRITICAL
logging.basicConfig(level=level)

wulin=Wulin()
pyautogui.moveTo(wulin.Coordinate.MinimumButton[0], wulin.Coordinate.MinimumButton[1])    #移动到IDE最小化位置
time.sleep(delayTime)
pyautogui.click()

pyautogui.moveTo(wulin.Coordinate.HerbLocation[0], wulin.Coordinate.HerbLocation[1])    #移动到草药位置
time.sleep(delayTime)
pyautogui.click()

time.sleep(delayTime)

#读取游戏信息

#截取游戏窗口
im = pyautogui.screenshot(region=(wulin.Coordinate.Base[0]+wulin.Coordinate.BaseFix[0], wulin.Coordinate.Base[1]+wulin.Coordinate.BaseFix[1], wulin.Coordinate.Width ,wulin.Coordinate.Height))

# 保存图片
#im.save(r'.\ScreenShots\my_screenshot.png')

#time.sleep(delayTime*2)

wulin.HerbGathering.GetItemSelectStatus()
wulin.HerbGathering.GetHarvestStatus()
logging.info('草药收获数字0出现次数:')
logging.info(wulin.HerbGathering.Harvest.count(0))

print('finish')
#for i in range(0,8):
#time.sleep(delayTime)
#pyautogui.moveTo(wulin.Coordinate.HerbItemSelect[i][0], wulin.Coordinate.HerbItemSelect[i][1])