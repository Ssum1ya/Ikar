import time

def start(drone):
 drone.arm()
 time.sleep(2)
 drone.takeoff()
 time.sleep(2)

def finish(drone):
    drone.land()
    time.sleep(2)
    drone.disarm()