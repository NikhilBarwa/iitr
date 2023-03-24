import time
from dronekit import connect, VehicleMode
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
vehicle.simple_takeoff(5)
while vehicle.location.global_relative_frame.alt < 19:
    print(f"Current Altitude {vehicle.location.global_relative_frame.alt}")
    time.sleep(0.25)

print("Reached desired altitude")
print("RTL")

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

print("Close vehicle object")
vehicle.close()

if sitl:
    sitl.stop()

