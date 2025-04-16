from pioneer_sdk import Camera, Pioneer
import cv2
import numpy as np
from time import sleep
import socket
import struct
import pickle

from detect_4_points_gpt import get_points

pioneerMini = Pioneer(log_connection=False, logger=False)

def go_to_point(x, y, z):
    pioneerMini.go_to_local_point_body_fixed(x = x, y = y, z = z, yaw = 0)
    while not pioneerMini.point_reached(): pass 
    sleep(3)

# Инициализация и подключение к серваку
s_get = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 65432

s_get.connect(("127.0.0.1", port))
data = b""
payload_size = struct.calcsize("Q")


pioneerMini.arm()
sleep(2)
pioneerMini.takeoff()
sleep(2)
go_to_point(x = 0, y = 0, z = 0.3)


camera_center = (250, 150)
points_array = [[0, 1, 0], [1, 0 ,0], 'cargo_up', [-1, 0 ,0], [0, -1, 0], 'cargo_down', 'land']
i = 0
while True:
    while len(data) < payload_size:
        packet = s_get.recv(4 * 1024)
        if not packet: break
        data += packet
    packet_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packet_msg_size)[0]

    while len(data) < msg_size:
        data += s_get.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    if type(go_to_point[i]) == list:
        x, y, z = points_array[i][0], points_array[i][1], points_array[i][2]
        go_to_point(x = x, y = y, z = z)
        i += 1
    elif go_to_point[i] == 'cargo_down':
        pioneerMini.lua_script_control('Start')
    elif go_to_point[i] == 'land':
        pioneerMini.land()
        break
    elif go_to_point[i] == 'cargo_up':
        if frame is not None:
            try:
                image, left, right, top, bottom = get_points(frame)
                cv2.circle(frame, (250, 150), 10, (0, 255, 0), -1)
                cv2.imshow('server', image)
                print(left, right, top, bottom)
            except:
                print('Ошибка')
                continue
            else:
                print('Не Ошибка')
                if camera_center[0] < left[0]: pioneerMini.set_manual_speed_body_fixed(vx = 0.1, vy = 0, vz = 0, yaw_rate = 0)
                elif camera_center[0] > right[0]: pioneerMini.set_manual_speed_body_fixed(vx = -0.1, vy = 0, vz = 0, yaw_rate = 0)
                elif camera_center[1] < top[1]: pioneerMini.set_manual_speed_body_fixed(vx = 0, vy = -0.1, vz = 0, yaw_rate = 0)
                elif camera_center[1] > bottom[1]: pioneerMini.set_manual_speed_body_fixed(vx = 0, vy = 0.1, vz = 0, yaw_rate = 0)
                else:
                    pioneerMini.land()
                    sleep(3)
                    pioneerMini.lua_script_control('Start')
                    sleep(3)
                    go_to_point(x = 0, y = 0, z = 0.3)
                    i += 1

    key = cv2.waitKey(1)

    if key == 27 or key == ord("q"):
        cv2.destroyAllWindows()
        break