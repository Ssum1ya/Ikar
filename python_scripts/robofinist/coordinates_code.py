from pioneer_sdk import Pioneer
from time import sleep

pioneerMini = Pioneer()

def go_to_point(x, y):
    pioneerMini.go_to_local_point_body_fixed(x=x, y=y, z=0, yaw=0)
    while not pioneerMini.point_reached():
        pass

#взлёт
pioneerMini.arm()
sleep(2)
pioneerMini.takeoff()
sleep(2)
pioneerMini.go_to_local_point_body_fixed(x=0, y=0, z=0.3, yaw=0)
sleep(3)

#пролёт восьмёрки
while True:
    go_to_point(-1.2, 2.8)
    go_to_point(0.5, 0.7)
    go_to_point(0.7, -0.7)
    go_to_point(-1.2, -3)
    go_to_point(0.5, -0.8)
    go_to_point(0.5, 0.8)