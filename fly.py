import pioneer_sdk
import cv2
import numpy as np
import time
import socket
import struct
import pickle
import math

s_get = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 65432

s_get.connect(("127.0.0.1", port))
data = b""
payload_size = struct.calcsize("Q")

pioneerMini = pioneer_sdk.Pioneer(log_connection=False, logger=False)

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# Parameters for marker detection (in this case, default parameters)
aruco_params = cv2.aruco.DetectorParameters()
# Create instance of ArucoDetector.
# Required starting from version opencv 4.7.0
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

current_command = 0
accurate = 25
current_aruco = -1
new_aruco = -1
flag_achieved = False

def aruco_achieved(wxc, wyc, axc, ayc):
    if math.sqrt(pow((axc - wxc), 2) + pow((ayc - wyc), 2)) < accurate:
        return 1
    return 0

def leveling(aruco_x_c, aruco_y_c):
    if 260 > aruco_x_c:
        pioneerMini.set_manual_speed(vx = -0.5, vy = 0, vz = 0, yaw_rate = 0)
    if 240 < aruco_x_c:
        pioneerMini.set_manual_speed(vx = 0.5, vy = 0, vz = 0, yaw_rate = 0)
    if 140 < aruco_y_c:
        pioneerMini.set_manual_speed(vx = 0, vy = 0.5, vz = 0, yaw_rate = 0)
    if 160 > aruco_y_c:
        pioneerMini.set_manual_speed(vx = 0, vy = -0.5, vz = 0, yaw_rate = 0)

pioneerMini.arm()
time.sleep(2)
pioneerMini.takeoff()
time.sleep(1.5)
pioneerMini.go_to_local_point_body_fixed(x=0,y=0,z= 0.5,yaw=0)
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
    xa, ya = 0, 0
    lab, lac = 0, 0
    y1, y4, y2, y3 = 0, 0, 0, 0
    normalId = None
    flag1 = False
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
            xa, ya = (x1 + x2) // 2, (y1 + y2) // 2
            xc, yc = (x1 + x2 + x3 + x4) // 4, (y1 + y2 + y3 + y4) // 4
            lab = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)
            lac = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
        cv2.imshow("drone_client", frame)


# 1.5 yaw = 90

    if xc > -100 and yc > -100:
       if normalId != None:
           if normalId == 0 and last_aruco != normalId:
               pioneerMini.go_to_local_point_body_fixed(x=0, y=0, z=-0.6, yaw=0)
               time.sleep(2)
               pioneerMini.go_to_local_point_body_fixed(x = 0, y = 1.45, z = 0, yaw = 0)
               last_aruco = 0
               time.sleep(1)
           if normalId == 1 and last_aruco != normalId:
               time.sleep(1)
               pioneerMini.go_to_local_point_body_fixed(x = -1.15, y = 0, z = 0, yaw = 0)
               last_aruco = 1
           if normalId == 2 and last_aruco != normalId:
               time.sleep(1)
               pioneerMini.go_to_local_point_body_fixed(x=0, y = 0, z = 0.3, yaw=0)
               time.sleep(2)
               pioneerMini.go_to_local_point_body_fixed(x = 0, y = -1, z = 0, yaw = 0)
               last_aruco = 2
           if normalId == 3 and last_aruco != normalId:
               pioneerMini.go_to_local_point_body_fixed(x = 0, y = 0.1, z = 0, yaw = 0)
               time.sleep(2)
               pioneerMini.land()
               last_aruco = 3

    key = cv2.waitKey(1)

    if key == 27 or key == ord("q"):
        cv2.destroyAllWindows()
        break