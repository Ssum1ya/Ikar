import cv2
import numpy as np

# Загрузка изображения
image = cv2.imread('qwe.png')

lr1 = np.array([0, 100, 100])
ur1 = np.array([10, 255, 255])
lr2 = np.array([170, 100, 100])
ur2 = np.array([180, 255, 255])

# Преобразование изображения из BGR в HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, lr1, ur1)
mask2 = cv2.inRange(hsv, lr2, ur2)
red_mask = cv2.bitwise_or(mask1, mask2)

contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

while True:
    cv2.imshow('Contours', image)
    ch = cv2.waitKey(5)

cv2.destroyAllWindows()
