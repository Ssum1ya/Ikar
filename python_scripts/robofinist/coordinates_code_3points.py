from pioneer_sdk import Pioneer
from time import sleep

pioneerMini = Pioneer()


def go_to_point(x, y):
    pioneerMini.go_to_local_point_body_fixed(x=x, y=y, z=0, yaw=0)
    while not pioneerMini.point_reached():
        pass


def right_angle():  # направо
    angle = 0

    while angle < 180:
        angle += 18
        yo = 0.3141590
        pioneerMini.go_to_local_point_body_fixed(0, 0.15, 0, yo)
        sleep(2)


def left_angle():  # это поворот налево
    angle = 0

    while angle < 180:
        sleep(1.5)
        angle += 18
        yo = -0.3141590
        pioneerMini.go_to_local_point_body_fixed(0, 0.15, 0, yo)
        sleep(2)


# взлёт
pioneerMini.arm()
sleep(2)
pioneerMini.takeoff()
sleep(2)
pioneerMini.go_to_local_point_body_fixed(x=0, y=0, z=0.3, yaw=0)
sleep(5)

# пролёт восьмёрки
while True:
    go_to_point(-1.03, 1.9) # -1.03 -2.07

    go_to_point(0.5, 0.52)
    go_to_point(0.5, -0.52)

    go_to_point(-1.03, -2.07)

    go_to_point(0.5, -0.52)
    go_to_point(0.5, -0.52)