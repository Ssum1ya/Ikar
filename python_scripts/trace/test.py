import pioneer_sdk
import time
from map import map
from utils import start, finish

drone = pioneer_sdk.Pioneer()
for array in map:
    if array == 'arm':
        start(drone)
    elif array == 'land':
        finish(drone)
    else:
        drone.go_to_local_point_body_fixed(x = array[0], y = array[1], z = array[2], yaw = 0)
    time.sleep(1.5)