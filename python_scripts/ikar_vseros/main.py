import time

from pioneer_sdk import Camera, Pioneer
from time import sleep
import cv2

from time_first.DetectRedColour import get_red_object
from get_4_points import get_points

camera_center = (250, 150)

camera = Camera()
camera.disconnect()
while True:
    frame = camera.get_cv_frame()
    try:
        image, left, right, top, bottom = get_points(frame)
        cv2.circle(frame, (250, 150), 10, (0, 255, 0), -1)
        cv2.imshow('server', image)
        print(left, right, top, bottom)
    except:
        print('Ошибка')
    else:
        print('Не Ошибка')
        if camera_center[0] < left[0]: print("точка левее")
        if camera_center[0] > right[0]: print("точка правее")
        if camera_center[1] < top[1]: print("выше")
        if camera_center[1] > bottom[1]: print("ниже")
    #if camera_center[0] < left[0]: print("zxc")
    # except:
    #     print("Ошибка")
    # else:
    #     cv2.imshow('server', get_points(frame))
    key = cv2.waitKey(1)