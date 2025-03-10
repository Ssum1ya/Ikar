import pioneer_sdk
import time

from detect_red_colour import get_red_object

"""
Принцип такой что мы летим до города
затем останавливаемся на некоторое время
потом берём кадр с камеры у дрона и записываем в файл.
В случае с 3 городом мы берём кадр с камеры передаём его в функцию
она возвращает нам кадр с помеченными красными обьектами
"""

mini = pioneer_sdk.Pioneer()
camera = pioneer_sdk.Camera(timeout=2, video_buffer_size=250000, log_connection=False)

def go_to_point(x, y):
    time.sleep(2)
    mini.go_to_local_point_body_fixed(x, y, 0, 0)
    time.sleep(3)

mini.arm()
mini.takeoff()
time.sleep(2)

# 1 город
mini.go_to_local_point_body_fixed(0,0, 0.3, 0)
go_to_point(0, 1)
time.sleep(3)
image = camera.get_frame()
with open('Верхнеуральск.jpg', 'wb') as file:
    file.write(image)

# 2 город
go_to_point(-1.35, 0)
go_to_point(0, 0.8)
time.sleep(3)
image = camera.get_frame()
with open('Магнитогорск.jpg', 'wb') as file:
    file.write(bytes(image))

# 3 город
go_to_point(0, -1.4)
go_to_point(0.6, 0)
time.sleep(3)
image = camera.get_frame()
red_detect_image = get_red_object(image)
with open('Южноуральск.jpg', 'wb') as file:
    file.write(bytes(red_detect_image)) #если выдаст ошибку надо оставить просто file.write(red_detect_image)

# 2 строчки снизу это от 3 города до мчс
# go_to_point(0, 0.2)
# go_to_point(1, 0)

mini.land()