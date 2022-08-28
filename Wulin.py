from Coordinate import Coordinate
from HerbGathering import HerbGathering
import win32gui
import logging

class Wulin:
    """武林群侠传
       
    """
    WindowName = "武林群侠传"
    def __init__(self):
        hwnd= win32gui.FindWindow(None, self.WindowName)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        base=(x,y)    #窗口基点坐标
        self.Coordinate=Coordinate(base,w,h)
        logging.info("Window %s:" % win32gui.GetWindowText(hwnd))
        logging.info("\tLocation: (%d, %d)" % (x, y))
        logging.info("\t    Size: (%d, %d)" % (w, h))

        self.HerbGathering=HerbGathering()
