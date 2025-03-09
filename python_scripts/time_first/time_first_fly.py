import pioneer_sdk
import time

from detect_red_colour import get_red_object

mini = pioneer_sdk.Pioneer()
camera = pioneer_sdk.Camera(timeout=2, video_buffer_size=250000, log_connection=False)

def go_to_point(x, y):
    time.sleep(2)
    mini.go_to_local_point_body_fixed(x, y, 0, 0)
    time.sleep(3)

mini.arm()
mini.takeoff()
time.sleep(2)

mini.go_to_local_point_body_fixed(0,0, 0.3, 0)
go_to_point(0, 1)
time.sleep(3)
image = camera.get_frame()
with open('../Верхнеуральск.jpg', 'wb') as file:
    file.write(image)

go_to_point(-1.35, 0)
go_to_point(0, 0.8)
time.sleep(3)
image = camera.get_frame()
with open('Магнитогорск.jpg', 'wb') as file:
    file.write(bytes(image))

go_to_point(0, -1.4)
go_to_point(0.6, 0)
time.sleep(3)
image = camera.get_frame()
red_detect_image = get_red_object(image)
with open('Южноуральск.jpg', 'wb') as file:
    file.write(bytes(red_detect_image))

# go_to_point(0, 0.2)
# go_to_point(1, 0)

mini.land()