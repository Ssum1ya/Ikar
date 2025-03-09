import pioneer_sdk
import time

drone = pioneer_sdk.Pioneer()
drone.land()
time.sleep(1)
drone.disarm()