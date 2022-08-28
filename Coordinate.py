import logging
class Coordinate:
   """武林群侠传坐标文件
      注意点：可以移动游戏窗口，但不能进行缩放等操作
   """
   BaseFix=(8,0)    #基点坐标修正
   WidthFix=2*8
   HeightFix=7
   MinimumButton = (1802,15)    #VSCode IDE最小化窗口位置   
   Base=(632, 270)    #实际运行电脑程序左上角x,y坐标，默认为测试电脑程序左上角x,y坐标，实际程序运行后，默认值会被替换
   Base0=(632, 270)    #测试电脑程序左上角x,y坐标,-8是修正
   Width=0    #窗口宽度
   Height=0    #窗口高度
   Role=(Base[0]-Base0[0]+954,Base[1]-Base0[1]+512)    #主角坐标
   Load=(Base[0]-Base0[0]+818,Base[1]-Base0[1]+766)    #读档
   Save=(Base[0]-Base0[0]+1105,Base[1]-Base0[1]+773)   #存档
   HerbLocation=(Base[0]-Base0[0]+974,Base[1]-Base0[1]+453)    #草药位置
   Record=(Base[0]-Base0[0]+977,Base[1]-Base0[1]+576)    #读档
   RecordYes=(Base[0]-Base0[0]+1036,Base[1]-Base0[1]+653)    #确认读档
   HerbItemSelect1st=(Base[0]-Base0[0]+733,Base[1]-Base0[1]+499)    #第1个草药选项的位置
   HerbItemSelect=[]
   

   def __init__(self,base,w,h):
      self.Base=base
      self.Width=w-self.WidthFix    #修正，实际尺寸偏大了
      self.Height=h-self.HeightFix    #修正，实际尺寸偏大了
      for i in range(0,8):
         self.HerbItemSelect.append((self.HerbItemSelect1st[0]+i*(769-733),self.HerbItemSelect1st[1]))
      logging.info(self.HerbItemSelect)