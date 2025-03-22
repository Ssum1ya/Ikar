import pioneer_sdk
import cv2
import numpy as np
import time
import socket
import struct
import pickle
import math

pioneerMini = pioneer_sdk.Pioneer(log_connection=False, logger=False)

# Инициализация и подключение к серваку
s_get = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 65432

s_get.connect(("127.0.0.1", port))
data = b""
payload_size = struct.calcsize("Q")

# Аруко параметры
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

pioneerMini.arm()
time.sleep(2)
pioneerMini.takeoff()
time.sleep(2)
pioneerMini.go_to_local_point_body_fixed(x=0, y=0, z=0.3, yaw=0)
time.sleep(3)

last_aruco = -1

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

    corners, ids = False, False
    xc, yc = -100, -100
    y1, y4, y2, y3 = 0, 0, 0, 0
    normalId = None
    if frame is not None:
        corners, ids, rejected = aruco_detector.detectMarkers(frame)
        if type(ids) != type(None):
            normalId = ids[0][0]
        else:
            normalId = None
        if corners:
            normal_corners = corners[0][0]
            x1, y1 = int(normal_corners[0][0]), int(normal_corners[0][1])
            x2, y2 = int(normal_corners[1][0]), int(normal_corners[1][1])
            x3, y3 = int(normal_corners[2][0]), int(normal_corners[2][1])
            x4, y4 = int(normal_corners[3][0]), int(normal_corners[3][1])
            xc, yc = (x1 + x2 + x3 + x4) // 4, (y1 + y2 + y3 + y4) // 4

        cv2.imshow("drone_client", frame)

    print(normalId)

    # 1.5 yaw = 90

    # if normalId != None:
    #     pioneerMini.go_to_local_point_body_fixed(x = map[normalId][0], y = map[normalId][1], z = map[normalId][2], yaw = 0)
    if xc > -100 and yc > -100:
        if normalId != None:
            if normalId == 0 and last_aruco != normalId:
                pioneerMini.go_to_local_point_body_fixed(x=-0.5, y=1.3, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 0
            if normalId == 3 and last_aruco == 0:
                pioneerMini.go_to_local_point_body_fixed(x=-0.7, y=1.5, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 3
            if normalId == 1 and last_aruco != normalId:
                #pioneerMini.go_to_local_point_body_fixed(x=1, y=0, z=0, yaw=0)
                pioneerMini.go_to_local_point_body_fixed(x=0.5, y=0.7, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 1
            if normalId == 5 and last_aruco != normalId:
                pioneerMini.go_to_local_point_body_fixed(x=0.7, y=-0.7, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 5
            if normalId == 2 and last_aruco != normalId:
                pioneerMini.go_to_local_point_body_fixed(x=-1.2, y=-3, z=0, yaw=0) # -0.5 -2.6
                time.sleep(5)
                last_aruco = 2
            if normalId == 4 and last_aruco != normalId:
                #pioneerMini.go_to_local_point_body_fixed(x=0.8, y=0, z=0, yaw=0)
                pioneerMini.go_to_local_point_body_fixed(x=0.5, y=-0.8, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 4
            if normalId == 6 and last_aruco != normalId:
                pioneerMini.go_to_local_point_body_fixed(x=0.5, y=0.8, z=0, yaw=0)
                time.sleep(5)
                last_aruco = 6

    key = cv2.waitKey(1)

    if key == 27 or key == ord("q"):
        cv2.destroyAllWindows()
        break