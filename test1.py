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

speeddiff = 1



# request to read Front sonar ping sensor
print("Front sensor = ", arlo.read_front_ping_sensor())
sleep(0.041)
# request to read Back sonar ping sensor
print("Back sensor = ", arlo.read_back_ping_sensor())
sleep(0.041)
# request to read Right sonar ping sensor
print("Right sensor = ", arlo.read_right_ping_sensor())
sleep(0.041)
# request to read Left sonar ping sensor
print("Left sensor = ", arlo.read_left_ping_sensor())
sleep(0.041)





#while True:
#	print(arlo.go_diff(leftS, rightS, 1, 1))
#	sleep(2.45)
#	arlo.stop()
#	sleep(0.5)
#	print(arlo.go_diff(leftS, rightS + 0.4, 0, 1)) # +.4 when turning left
#	sleep(t_90deg)
#	arlo.stop()
#	sleep(0.5)

