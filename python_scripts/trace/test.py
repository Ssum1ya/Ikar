import pioneer_sdk
import time
from map import map
from utils import start, finish

drone = pioneer_sdk.Pioneer()
start(drone)
for array in map:
    drone.go_to_local_point_body_fixed(x = array[0], y = array[1], z = array[2], yaw = 0)
    time.sleep(3)
finish(drone)