from time import sleep
import time

#################################################################################
                    ### GLOBAL CONST VARIABLES ###                              #
SPEED_LT = 61                           # LEFT MOTOR                            #
SPEED_RT = 63.75                        # RIGHT MOTOR                           #
METER_TIME = 2.3                        # TIME TO DRIVE 1 METER                 #
QUARTER_ROTATION_TIME = 0.725           # TIME TO DO QUARTER ROTATION           #
QUARTER_MOVING_ROTATION_TIME = 1.45     # TIME TO DO QUARTER MOVING ROTATION    #
#################################################################################

### Takes the robot object and the degrees it should turn (to the left) ###
def TurnXDegLeft(rob, deg):
    print(rob.go_diff(SPEED_LT, SPEED_RT, 0, 1))
    sleep((deg*QUARTER_ROTATION_TIME)/90)

### Takes the robot object and the degrees it should turn (to the right) ###
def TurnXDegRight(rob, deg):
    print(rob.go_diff(SPEED_LT, SPEED_RT + 0.4, 1, 0))
    sleep((deg*QUARTER_ROTATION_TIME)/90)

### Takes the robot object, the distance, and direction (negative for backwards) ###
def GoXMeters(rob, dist, dir):
    start = time.perf_counter()
    while time.perf_counter - start < dist*METER_TIME:
        print(rob.go_diff(SPEED_LT, SPEED_RT, dir, dir))

### Stops the robot ###
def Stop(rob):
    print(rob.stop())
    sleep(0.1)

### Takes the robot object, degrees it should turn, and the direction (positve = right, negative = left) ###
def MovingTurn(rob, deg, dir): # dir = 1 (right turn); dir = -1 (left turn)
    print(rob.go_diff(SPEED_LT + (30 * dir), SPEED_RT - (30 * dir), 1, 1))
    sleep((deg*QUARTER_MOVING_ROTATION_TIME)/90)

