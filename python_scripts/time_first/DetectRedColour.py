import cv2
import numpy as np

def get_red_object(im):
    image = im

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # преобразует в цвет в че то там

    lr1 = np.array([0, 100, 100])
    ur1 = np.array([10, 255, 255])
    lr2 = np.array([170, 100, 100])
    ur2 = np.array([180, 255, 255])

    # Маска для красного цвета
    mask1 = cv2.inRange(hsv_image, lr1, ur1)
    mask2 = cv2.inRange(hsv_image, lr2, ur2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Нахождение контуров
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Рисование окружностей
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(image, center, radius, (255, 255, 255), 2)

    return image
