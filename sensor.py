

from time import sleep
import robot
import Help_functions

arlo = robot.Robot()

leftS = 61
rightS = 63.75

turn = 1

print(arlo.go_diff(leftS, rightS, 1, 1))


while True:
    # print(arlo.go_diff(leftS, rightS, 1, 1))
    left = arlo.read_left_ping_sensor() 
    right = arlo.read_right_ping_sensor()
    front = arlo.read_front_ping_sensor()

    print("Front sensor = ", front)
    print("Left sensor = ", left)
    print("Right sensor = ", right)
    while 600 < (arlo.read_left_ping_sensor() and arlo.read_right_ping_sensor() and arlo.read_front_ping_sensor()):
        print(arlo.go_diff(leftS, rightS, 1, 1))
    arlo.stop()
    left = arlo.read_left_ping_sensor() 
    right = arlo.read_right_ping_sensor()
    front = arlo.read_front_ping_sensor()
    
    if front < left and right: 
        if left < right:
            Help_functions.TurnXDegLeft(arlo, 90)
        else: 
            Help_functions.TurnXDegRight(arlo, 90)
        
    elif left < right and front:
        Help_functions.TurnXDegRight(arlo, 90)
    elif right < left and front: 
        Help_functions.TurnXDegLeft(arlo, 90)

 





    
    
    # front < 500 and turn != 2: 
    #     Help_functions.TurnXDegRight(arlo, 45)
    #     while arlo.read_left_ping_sensor() < 600:
    #         Help_functions.TurnXDegRight(arlo, 10)
    #         turn += 1
    # elif front < 500 and turn == 2: 
    #     Help_functions.TurnXDegRight(arlo, 45)
    #     while arlo.read_right_ping_sensor() < 600:
    #         Help_functions.TurnXDegLeft(arlo, 10)
    #         turn += 1
    

 

