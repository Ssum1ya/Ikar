import time

def start(drone):
    drone.arm()
    drone.takeoff()

def finish(drone):
    drone.land()
    time.sleep(2)
    #drone.disarm()