# -*- coding: utf-8 -*-
from Wulin import Wulin
import time
import pyautogui
import logging

delayTime=1

#https://blog.csdn.net/weixin_41010198/article/details/89356417
level = logging.DEBUG # DEBUG、INFO、WARNING、ERROR、CRITICAL
logging.basicConfig(level=level)

wulin=Wulin()
pyautogui.moveTo(wulin.Coordinate.Role[0], wulin.Coordinate.Role[1])    #移动到主角身上
time.sleep(delayTime)

for i in range(0,8):
    time.sleep(delayTime)
    pyautogui.moveTo(wulin.Coordinate.HerbItemSelect[i][0], wulin.Coordinate.HerbItemSelect[i][1])