import time
from dronekit import connect, VehicleMode
import threading
from detect_picam import object_detector
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect if args.connect else "127.0.0.1:14550"

print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=False)
#conn = mavutil.mavlink_connection(connection_string)

vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

print("Taking Off")
vehicle.simple_takeoff(20)
while vehicle.location.global_relative_frame.alt < 19:
    print(f"Current Altitude {vehicle.location.global_relative_frame.alt}")
    time.sleep(0.25)

event = threading.Event()
def show_bbox(det_obj):
  while True:
    print(det_obj.get_bbox())
    
det_obj = object_detector(weights = 'best.pt', label = "target")
bbox_thread = threading.Thread(target=show_bbox, args=(det_obj,))
bbox_thread.start()
det_obj.run(source=0)
    
'''def set_rc(vehicle, event):
    print("RC 3 SET")
    while not event.is_set():
        vehicle.channels.overrides['3'] = 1500
    
    print("RC 3 RESET")
    vehicle.channels.overrides['3'] = None
    
    
def decrease_radius(vehicle, min_radius):
    while (rad:=vehicle.parameters["CIRCLE_RADIUS"]) > min_radius:
        print(f"Changing Radius from {rad} to {rad-500}")
        vehicle.parameters["CIRCLE_RADIUS"] -= 200
        time.sleep(5)


MIN_RADIUS=1000
set_rc_thread = threading.Thread(target=set_rc, args=(vehicle, event,))
decrease_radius_thread = threading.Thread(target=decrease_radius, args=(vehicle, MIN_RADIUS,))

def circle():
    vehicle.parameters["CIRCLE_RADIUS"] = 5000
    set_rc_thread.start()
    print(f"circling")
    vehicle.mode = VehicleMode("CIRCLE")
    decrease_radius_thread.start()
    
circle()
while True:
    if vehicle.parameters["CIRCLE_RADIUS"]*0.95 < MIN_RADIUS:
        event.set()
        set_rc_thread.join()
        vehicle.mode = VehicleMode("RTL")
        break
'''        

# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")

# print("Close vehicle object")
# vehicle.close()

# if sitl:
#     sitl.stop()

