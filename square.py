# from time import sleep
# import robot

# # init robot
# arlo = robot.Robot()

# leftS = 63
# rightS = 64

# for i in range(0,4):
#         print(arlo.go_diff(leftS, rightS, 1, 1))
#         sleep(1)
#         arlo.stop()

#         # sleep(1)

#         print(arlo.go_diff(leftS, rightS, 1, 0))
#         sleep(0.72)
#         arlo.stop()



#### Approved
from time import sleep
import robot

arlo = robot.Robot()


leftS = 61
rightS = 63.75

# Time to drive 1 meter
t = 2.3


t_full_rotation = 0.77
t_90deg = 0.725

while True:
        print(arlo.go_diff(leftS, rightS, 1, 1))
        sleep(2.45)
        arlo.stop()
        sleep(0.5)
        print(arlo.go_diff(leftS, rightS + 0.4, 0, 1)) # +.4 when turning left
        sleep(t_90deg)
        arlo.stop()
        sleep(0.5)