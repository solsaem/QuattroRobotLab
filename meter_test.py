from time import sleep
import robot


arlo = robot.Robot()

print(arlo.go_diff(63, 64, 1, 1))
sleep(3)
arlo.stop()
