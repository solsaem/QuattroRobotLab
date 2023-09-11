
from time import sleep
import robot
import Help_functions

arlo = robot.Robot()

leftS = 61
rightS = 63.75

print(arlo.go_diff(leftS, rightS, 1, 1))


while True:

    print(arlo.go_diff(leftS, rightS, 1, 1))


    left = arlo.read_left_ping_sensor()
    right = arlo.read_right_ping_sensor()
    front = arlo.read_front_ping_sensor()
    print("Front sensor = ", front)
    if front < 500:
        Help_functions.TurnXDegLeft(arlo, 90)
        Help_functions.GoXMeters(arlo, 1, 1)
        Help_functions.TurnXDegRight(arlo, 90)
        Help_functions.GoXMeters(arlo, 2, 1)
        Help_functions.TurnXDegRight(arlo, 90)
        Help_functions.GoXMeters(arlo, 1, 1)
        Help_functions.TurnXDegLeft(arlo, 90)
