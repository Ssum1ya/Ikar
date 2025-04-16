from pioneer_sdk import Camera, Pioneer
from time import sleep
import cv2

from detect_4_points_gpt import get_points

camera = Camera()
drone = Pioneer()

def go_to_point(x, y, z):
    drone.go_to_local_point_body_fixed(x = x, y = y, z = z, yaw = 0)
    while not drone.point_reached(): pass 
    sleep(3)

drone.arm()
sleep(2)
drone.takeoff()
sleep(2)
go_to_point(x = 0, y = 0, z = 0.3)

camera_center = (250, 150)
points_array = [[0, 1, 0], [1, 0 ,0], 'cargo_up', [-1, 0 ,0], [0, -1, 0], 'cargo_down', 'land']
i = 0
camera.disconnect()
while True:
    frame = camera.get_cv_frame()
    if type(go_to_point[i]) == list:
        x, y, z = points_array[i][0], points_array[i][1], points_array[i][2]
        go_to_point(x = x, y = y, z = z)
        i += 1
    elif go_to_point[i] == 'cargo_up':
        try:
            image, left, right, top, bottom = get_points(frame)
            cv2.circle(frame, (250, 150), 10, (0, 255, 0), -1)
            cv2.imshow('server', image)
            print(left, right, top, bottom)
        except:
            print('Ошибка')
        else:
            print('Не Ошибка')
            if camera_center[0] < left[0]: drone.set_manual_speed_body_fixed(vx = 0.1, vy = 0, vz = 0, yaw_rate = 0)
            elif camera_center[0] > right[0]: drone.set_manual_speed_body_fixed(vx = -0.1, vy = 0, vz = 0, yaw_rate = 0)
            elif camera_center[1] < top[1]: drone.set_manual_speed_body_fixed(vx = 0, vy = -0.1, vz = 0, yaw_rate = 0)
            elif camera_center[1] > bottom[1]: drone.set_manual_speed_body_fixed(vx = 0, vy = 0.1, vz = 0, yaw_rate = 0)
            else:
                drone.land()
                sleep(3)
                drone.lua_script_control('Start')
                sleep(3)
                go_to_point(x = 0, y = 0, z = 0.3)
                i += 1
    elif go_to_point[i] == 'cargo_down':
        drone.lua_script_control('Start')
    elif go_to_point[i] == 'land':
        drone.land()
        break
    key = cv2.waitKey(1)