import cv2
import pytesseract
from PIL import Image
import logging

level = logging.DEBUG # DEBUG、INFO、WARNING、ERROR、CRITICAL
logging.basicConfig(level=level)

path = r'3.png'
ori_image = cv2.imread(path)
cv2.imshow('ori_image',ori_image)
 
logging.info(pytesseract.image_to_string(ori_image,lang="chi_sim"))    #"eng",'chi_sim'

gray_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray_image',gray_image)
logging.info(pytesseract.image_to_string(gray_image,lang="chi_sim"))


#数字〇，lang="eng+chi_sim",--psm 5
#数字一、二，lang="eng+chi_sim",--psm 13
ret,thresh1 = cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)
cv2.imshow('binary_image',thresh1)

#for i in range(0,10):
logging.info(pytesseract.image_to_string(thresh1,lang="eng+chi_sim",config='--psm 5'))

#cv2.imwrite('31_binary.png', thresh1) 

#cv2.waitKey()