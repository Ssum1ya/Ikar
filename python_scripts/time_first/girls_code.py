from pioneer_sdk import Pioneer
from pioneer_sdk import Camera
import cv2
import time
import numpy as np
import os.path

names = ['Verkhneuralsk', 'Magnitogorsk', 'Yuzhnouralsk'] # Названия для городов для сохранения
Crd = [[0, 0], [0, 0], [0, 0],[0, 0]] # Координаты для пролёта городов

cam = Camera()
me = Pioneer()

status = "start"
Pos = 0
City = None
i = 0
running = False
lr1 = np.array([0, 100, 100])
ur1 = np.array([10, 255, 255])
lr2 = np.array([170, 100, 100])
ur2 = np.array([180, 255, 255])


def go_point(x,y):
    me.go_to_local_point_body_fixed(x=x, y=y, z=0, yaw=0)
    while not me.point_reached():
        pass

me.arm()
time.sleep(2)
me.takeoff()
time.sleep(2)
me.go_to_local_point(x=0, y=0, z=1.3, yaw=0)
cam.connect()

while True:
    key = cv2.waitKey(1)
    Pos = Crd[i]
    x = Pos[0]
    y = Pos[1]
    City = names[i]
    cam.disconnect()
    go_point(x,y)
    cam.connect()
    frame = cam.get_cv_frame()
    cv2.imwrite(f'{City}.png', frame)
    status = ''
    # img = cv2.imread(frame)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # mask1 = cv2.inRange(hsv, lr1, ur1)
    # mask2 = cv2.inRange(hsv, lr2, ur2)
    # red_mask = cv2.bitwise_or(mask1, mask2)
    # contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # frame1 = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    if os.path.exists(f'{City}.png'):
        print(f'frame saved as {City}.png')
    else:
        print(f'frame was not saved')
    time.sleep(5)
    i += 1
    if i == len(names):
        status = 'finish'
    #cv2.imshow("Output", frame)
    if key == 27 or status == 'finish':
        print("esc pressed")
        me.land()
        break
#me.go_to_local_point_body_fixed(2.05,-0.3,0,0)
while not me.point_reached():
    pass
if me.get_autopilot_state() != 'LANDED':
    me.land()
cv2.destroyAllWindows()
me.disarm()