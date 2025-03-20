import pioneer_sdk
import cv2
import time

camera = pioneer_sdk.Camera(timeout=2, video_buffer_size=250000, log_connection=False)

time.sleep(3)
camera.connect()
frame = camera.get_cv_frame()
cv2.imwrite('Photo.jpg', frame)
camera.disconnect()