import pioneer_sdk
import cv2
import numpy as np
import time
import socket
import struct
import pickle
import math
from arcs import first_arc, second_arc

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

# Переменные для машинного зрения
hsvVals = [0, 19, 21, 36, 255,255]
sensors = 3
threshold = 0.2
width, height = 480, 360
senstivity = 3
weights = [1000, 1500 ,2000]
fSpeed = 1
curve = 0

#Функции для машинного зрения
def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getContours(imgThres, img):
    cx = 0
    contours, hieracrhy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    return cx

def getSensorOutput(imgThres, sensors, img):
    imgs = np.hsplit(imgThres, sensors)
    totalPixels = (img.shape[1] // sensors) * img.shape[0]
    senOut = []
    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
    return senOut

pioneerMini.arm()
pioneerMini.takeoff()
time.sleep(2)
pioneerMini.go_to_local_point_body_fixed(x=0,y=0,z= 0.3,yaw=0)
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

    # Выделение линии
    img2 = cv2.resize(frame, (width, height))
    img2 = cv2.flip(img2, 0)
    imgThres = thresholding(img2)
    cx = getContours(imgThres, img2)  ## For Translation
    senOut = getSensorOutput(imgThres, sensors, frame)  ## Rotation
    
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
        cv2.imshow("Output", img2)
        cv2.imshow("Path", imgThres)

    print(normalId)

# 1.5 yaw = 90

    if xc > -100 and yc > -100:
       if normalId != None:
           if normalId == 10 and last_aruco != normalId:
               pioneerMini.go_to_local_point_body_fixed(x = -0.6, y = 0.6, z = 0, yaw = 0)
               time.sleep(3)
               last_aruco = 10
           if normalId == 5 and last_aruco != normalId:
               first_arc(drone=pioneerMini)
               last_aruco = 5
           if normalId == 6 and last_aruco != normalId:
               pioneerMini.go_to_local_point_body_fixed(x=0, y = 0, z = 0.3, yaw=0)
               time.sleep(3)
               pioneerMini.go_to_local_point_body_fixed(x=0.6, y = 0.6, z = 0, yaw=0)
               time.sleep(3)
               last_aruco = 6
           if normalId == 9 and last_aruco != normalId:
               second_arc(pioneerMini)
               last_aruco = 9
               pioneerMini.land()

    key = cv2.waitKey(1)

    if key == 27 or key == ord("q"):
        cv2.destroyAllWindows()
        break