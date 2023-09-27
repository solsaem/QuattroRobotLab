
from time import sleep
import robot

arlo = robot.Robot()


leftS = 61
rightS = 63.75

# Time to drive 1 meter
t = 2.3


#print(arlo.go_diff(leftS, rightS, 1, 1))
#sleep(t * 3)
#arlo.stop()

t_full_rotation = 0.77
t_90deg = 0.725

speeddiff = 0.5

while True:

	print(arlo.go_diff(leftS + 30, rightS - 30, 1, 1))
	sleep(4.35)

	print(arlo.go_diff(leftS, rightS, 1, 1))
	sleep(1.9)

	print(arlo.go_diff(leftS - 30, rightS + 30, 1, 1))
	sleep(4.325)

	print(arlo.go_diff(leftS, rightS, 1, 1))
	sleep(1.9)



