# -*- coding: utf-8 -*-
import pyautogui
import logging
import pytesseract
import cv2

class HerbGathering:
    """草药采集
       存储采药采集过程中的状态
    """
    ItemSelect=[0,0,0,0,0,0,0,0]    #0表示没选中，1表示选中
    ItemSelectPosition=[0,0,0,0,0,0,0,0]
    Harvest=[0,0,0,0,0,0,0,0]
    HarvestPosition=[0,0,0,0,0,0,0,0]
    def __init__(self):
        self.Harvest=[0,0,0,0,0,0,0,0]    #已收获草药数目（从概率小的到概率大的）
    
    def GetItemSelectStatus(self) :      
        position = pyautogui.locateOnScreen(r'.\Images\Quantity.png', confidence=0.9)
        logging.info("HerbGathering-HerbGathering：")
        logging.info('位置：')
        logging.info(position)    #一般情况下在(733,499,299,5)附近
        self.ItemSelectPosition[0]=(position.left,position.top,33,25)
        self.ItemSelectPosition[1]=(position.left+(773-733),position.top,33,25)
        self.ItemSelectPosition[2]=(position.left+(810-733),position.top,33,25)
        self.ItemSelectPosition[3]=(position.left+(847-733),position.top,33,25)
        self.ItemSelectPosition[4]=(position.left+(884-733),position.top,33,25)
        self.ItemSelectPosition[5]=(position.left+(921-733),position.top,33,25)
        self.ItemSelectPosition[6]=(position.left+(958-733),position.top,33,25)
        self.ItemSelectPosition[7]=(position.left+(995-733),position.top,33,25)

        path = r'.\ScreenShots\HerbGatheringItemSelectScreenshot.png'
        for i in range(0,8):
            im = pyautogui.screenshot(region=self.ItemSelectPosition[i])#im = pyautogui.screenshot(region=(733,499,33,25))
            im.save(path)
            ori_image = cv2.imread(path)
            #cv2.imshow('ori_image',ori_image)

            gray_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)

            #数字〇，lang="eng+chi_sim",--psm 5
            #数字一、二，lang="eng+chi_sim",--psm 13
            ret,thresh1 = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
            logging.info(pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 5'))    #测试
            if pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 5')=='0\n':
                self.ItemSelect[i]=0
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='一\n':
                self.ItemSelect[i]=1
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='二\n':
                self.ItemSelect[i]=2
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='三\n':
                self.ItemSelect[i]=3
            else:
                self.ItemSelect[i]=9
    def GetHarvestStatus(self):
        position = pyautogui.locateOnScreen(r'.\Images\Quantity.png', confidence=0.9)    #“选择数量”左上角坐标（用抓抓软件查看）
        logging.info("HerbGathering-GetHarvestStatus：")
        baseLeft=1111-2;baseTop=455    #最左上角数据的左上角坐标
        width=13+2*2;height=8+2*2    #截图的宽度和高度
        self.HarvestPosition[0]=(position.left+(baseLeft-733+20*3),position.top+(baseTop-499),width,height)
        self.HarvestPosition[1]=(position.left+(baseLeft-733+20*2),position.top+(baseTop-499),width,height)
        self.HarvestPosition[2]=(position.left+(baseLeft-733+20*1),position.top+(baseTop-499),width,height)
        self.HarvestPosition[3]=(position.left+(baseLeft-733+20*0),position.top+(baseTop-499),width,height)
        self.HarvestPosition[4]=(position.left+(baseLeft-733+20*3),position.top+(baseTop-499+582-455),width,height)
        self.HarvestPosition[5]=(position.left+(baseLeft-733+20*2),position.top+(baseTop-499+582-455),width,height)
        self.HarvestPosition[6]=(position.left+(baseLeft-733+20*1),position.top+(baseTop-499+582-455),width,height)
        self.HarvestPosition[7]=(position.left+(baseLeft-733+20*0),position.top+(baseTop-499+582-455),width,height)
   
        for i in range(0,8):
            path = r'.\ScreenShots\HerbGatheringHarvestScreenshot'+str(i)+'.png'
            im = pyautogui.screenshot(region=self.HarvestPosition[i])
            im.save(path)
            ori_image = cv2.imread(path)
            #cv2.imshow('ori_image',ori_image)
            gray_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)

            #数字〇，lang="eng+chi_sim",--psm 5
            #数字一、二，lang="eng+chi_sim",--psm 13
            ret,thresh1 = cv2.threshold(gray_image,90,255,cv2.THRESH_BINARY)
            bin_image_path = r'.\ScreenShots\HerbGatheringHarvestScreenshotBinImage'+str(i)+'.png'
            cv2.imwrite(bin_image_path, thresh1)

            logging.info(pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 5'))    #测试
            if pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 5')=='0\n':
                self.Harvest[i]=0
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='一\n':
                self.Harvest[i]=1
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='二\n':
                self.Harvest[i]=2
            elif pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 13')=='三\n':
                self.Harvest[i]=3
            else:
                self.Harvest[i]=9
            