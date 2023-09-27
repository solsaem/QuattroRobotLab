from time import sleep
import robot
import Help_functions


arlo = robot.Robot()

data = [0,0,0,0,0]


for i in range(len(data)):
	data[i] = arlo.read_right_ping_sensor()
	sleep(0.1)

print(data) 
