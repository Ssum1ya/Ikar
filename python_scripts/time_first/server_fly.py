import pioneer_sdk
import cv2
import numpy as np
import time
import socket
import struct
import pickle
import math

from detect_red_colour import get_red_object

s_get = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 65432

s_get.connect(("127.0.0.1", port))
data = b""
payload_size = struct.calcsize("Q")

pioneerMini = pioneer_sdk.Pioneer(log_connection=False, logger=False)

current_command = 1

def go_to_point(x, y):
    time.sleep(2)
    pioneerMini.go_to_local_point_body_fixed(x, y, 0, 0)
    time.sleep(3)

pioneerMini.arm()
pioneerMini.takeoff()
time.sleep(2)
pioneerMini.go_to_local_point_body_fixed(0,0, 0.3, 0)

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
    

    if frame is not None:
        cv2.imshow("drone_client", frame)


# 1.5 yaw = 90


    if current_command == 1:
        go_to_point(0, 1)
        time.sleep(3)
        cv2.imwrite('Верхнеуральск.jpg', frame)
        current_command = 2
    if current_command == 2:
        go_to_point(-1.35, 0)
        go_to_point(0, 0.8)
        time.sleep(3)
        cv2.imwrite('Магнитогорск.jpg', frame)
        current_command = 3
    if current_command == 3:
        go_to_point(0, -1.4)
        go_to_point(0.6, 0)
        time.sleep(3)
        cv2.imwrite('Южноуральск.jpg', get_red_object(frame))
        pioneerMini.land()

    key = cv2.waitKey(1)

    if key == 27 or key == ord("q"):
        cv2.destroyAllWindows()
        break