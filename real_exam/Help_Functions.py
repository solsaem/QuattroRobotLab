from time import sleep
import time
try:
    from picamera2 import Picamera2, Preview
except:
    ""
import cv2
import numpy as np
import math
#################################################################################
                    ### GLOBAL CONST VARIABLES ###                              #
SPEED_LT = 61                           # LEFT MOTOR                            #
SPEED_RT = 63.75                        # RIGHT MOTOR                           #
METER_TIME = 2.3                        # TIME TO DRIVE 1 METER                 #
QUARTER_ROTATION_TIME = 0.725           # TIME TO DO QUARTER ROTATION           #
QUARTER_MOVING_ROTATION_TIME = 1.45     # TIME TO DO QUARTER MOVING ROTATION    #
CAMERA_MATRIX = np.array([[2047, 0, 1296], [0, 2047, 972], [0, 0, 1]])          #
IS_DRIVING = False                                                              #
IS_TURNING_LEFT = False                                                         #
IS_TURNING_RIGHT = False                                                        #
#################################################################################

### Takes the robot object and the degrees it should turn (to the right) ###
def TurnXDegLeft(rob, deg):
    global IS_TURNING_LEFT
    if deg < 0:
        TurnXDegRight(rob, abs(deg))
        return
    if deg > 180:
        TurnXDegRight(rob, deg-180)
        return
    IS_TURNING_LEFT = True
    print(rob.go_diff(SPEED_LT/2, SPEED_RT/2, 0, 1))
    sleep(deg*0.0211+0.0646)
    Stop(rob)

### Takes the robot object and the degrees it should turn (to the left) ###
def TurnXDegRight(rob, deg):
    global IS_TURNING_RIGHT
    if deg < 0:
        TurnXDegLeft(rob, abs(deg))
        return
    if deg > 180:
        TurnXDegLeft(rob, deg-180)
        return
    IS_TURNING_RIGHT = True
    print(rob.go_diff(SPEED_LT/2, SPEED_RT/2, 1, 0))
    sleep(deg*0.0211+0.0646)
    Stop(rob)

### Takes the robot object, the distance, and direction (0 for backwards) ###
def GoXCM(rob, dist, dir, speed):
    global IS_DRIVING
    start = time.perf_counter()
    while time.perf_counter() - start < dist*0.0264 - 0.0608:
        left = rob.read_left_ping_sensor()
        right = rob.read_right_ping_sensor()
        front = rob.read_front_ping_sensor()
        if right < 300:
            print("right too close")
            GoAround(rob, "right")
            return False
        if left < 300:
            print("left too close")
            GoAround(rob, "left")
            return False
        if front < 150:
            print("front too close")
            GoAround(rob, "right")
            return False
        IS_DRIVING = True
        print(rob.go_diff(SPEED_LT * speed, SPEED_RT * speed, dir, dir))
    Stop(rob)
    return True
### Stops the robot ###
def Stop(rob):
    global IS_TURNING_LEFT
    global IS_TURNING_RIGHT
    global IS_DRIVING
    print(rob.stop())
    IS_TURNING_RIGHT = False
    IS_TURNING_LEFT = False
    IS_DRIVING = False
    sleep(0.1)

### Takes the robot object, degrees it should turn, and the direction (positve = right, negative = left) ###
def MovingTurn(rob, deg, dir): # dir = 1 (right turn); dir = -1 (left turn)
    print(rob.go_diff(SPEED_LT + (30 * dir), SPEED_RT - (30 * dir), 1, 1))
    sleep((deg*QUARTER_MOVING_ROTATION_TIME)/90)

### Takes the robot position, robot radius, an object position, and object radius. Returns true if they don't collide)
def Collision(robot_point, robot_radius, object_point, object_radius):
    return np.sqrt((robot_point[0] - object_point[0]) ** 2 + (robot_point[1] - object_point[1]) ** 2) < (robot_radius + object_radius)

### Start the camera with high resolution and return the picam ### 
def Camera_Init():
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration({"size": (2592, 1944)})
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(2)
    return picam2


# Return True on collision
def check_collision(p1, p2, r1, r2):
    return np.linalg.norm(np.array(p1) - np.array(p2)) <= r1 + r2

# Calculates distance between two points
def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_angle(x, y, x_prev, y_prev):
    delta_x = x - x_prev
    delta_y = y - y_prev

    angle = math.atan2(delta_x, delta_y)

    angle_degrees = math.degrees(angle)

    return angle_degrees

# Avoid obsstacles when side sensors de
def GoAround(rob, sensor):
    if sensor == 'left':
        TurnXDegRight(rob, 90)
        GoXCM(rob, 50, 1, 1)
        TurnXDegLeft(rob, 140)
    else:
        TurnXDegLeft(rob, 90)
        GoXCM(rob, 50, 1, 1)
        TurnXDegRight(rob, 140)
    Stop(rob)
