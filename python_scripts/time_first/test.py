from pioneer_sdk import Pioneer, Camera
import cv2
import time

from detect_red_colour import get_red_object

drone = Pioneer()
camera = Camera()

def go_to_point(x, y):
    time.sleep(2)
    drone.go_to_local_point_body_fixed(x, y, 0, 0)
    time.sleep(3)

drone.arm()
drone.takeoff()
time.sleep(2)
drone.go_to_local_point_body_fixed(0,0, 0.3, 0)

current_command = 1
while True:
    frame = camera.get_frame()

    cv2.imshow('camera', frame)
    
    if current_command == 1:
        go_to_point(0, 1)
        time.sleep(3)
        cv2.imwrite('Верхнеуральск.jpg', frame)
        current_command += 1
    elif current_command == 2:
        go_to_point(-1.35, 0)
        go_to_point(0, 0.8)
        time.sleep(3)
        cv2.imwrite('Магнитогорск.jpg', frame)
        current_command += 1
    elif current_command == 3:
        go_to_point(0, -1.4)
        go_to_point(0.6, 0)
        time.sleep(3)
        cv2.imwrite('Южноуральск.jpg', get_red_object(frame))
        drone.land()
