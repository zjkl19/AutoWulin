import cv2
 
path = r'21.png'
ori_image = cv2.imread(path)
cv2.imshow('ori_image',ori_image)
 
#灰度化
gray_image = cv2.cvtColor(ori_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray_image',gray_image)

ret, th1 = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
ret, th2 = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)
ret, th3 = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TRUNC)
ret, th4 = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TOZERO)
ret, th5 = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TOZERO_INV)
cv2.imshow('th1',cv2.resize(th1,(int(th1.shape[1]/2),int(th1.shape[0]/2))))
cv2.imshow('th2',cv2.resize(th2,(int(th1.shape[1]/2),int(th1.shape[0]/2))))
cv2.imshow('th3',cv2.resize(th3,(int(th1.shape[1]/2),int(th1.shape[0]/2))))
cv2.imshow('th4',cv2.resize(th4,(int(th1.shape[1]/2),int(th1.shape[0]/2))))
cv2.imshow('th5',cv2.resize(th5,(int(th1.shape[1]/2),int(th1.shape[0]/2))))

cv2.waitKey()