import pioneer_sdk
import time

drone = pioneer_sdk.Pioneer()
drone.land()
drone.disarm()