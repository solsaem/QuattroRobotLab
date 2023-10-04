from time import sleep
import robot


arlo = robot.Robot()

print(arlo.go_diff(61/2, 63.75/2, 0, 1))
sleep(1.25)
arlo.stop()

