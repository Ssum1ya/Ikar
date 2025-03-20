from pioneer_sdk import Pioneer
from pioneer_sdk import Camera
import cv2
import time
import numpy as np
import os.path

from DetectRedColour import get_red_object

names = ['Verkhneuralsk','Magnitogorsk','Yuzhnouralsk','Base']
Crd = [[0, 1.9], [-1, -0.4], [-0.1, -1.1],[1, -0.5]]
MCHS = [[1, -0.3], [-0.4, -1.1], [-1.05, 0.4]]

cam = Camera()
me = Pioneer()

status = "start"
City = None
i = 0

def go_point(x,y):
    me.go_to_local_point_body_fixed(x=x, y=y, z=0, yaw=0)
    while not me.point_reached():
        pass

me.arm()
time.sleep(2)
me.takeoff()
time.sleep(2)
me.go_to_local_point_body_fixed(x=0, y=0, z=0.3, yaw=0)
time.sleep(3)
cam.connect()

while True:
    key = cv2.waitKey(1)
    x = Crd[i][0]
    y = Crd[i][1]
    City = names[i]
    cam.disconnect()
    go_point(x, y)
    cam.connect()
    frame = cam.get_cv_frame()
    cv2.imwrite(f'{City}.png', get_red_object(frame))
    status = ''
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
while not me.point_reached():
    pass
if me.get_autopilot_state() != 'LANDED':
    me.land()
cv2.destroyAllWindows()
me.disarm()