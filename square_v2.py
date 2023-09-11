import robot
import Help_Functions

arlo = robot.Robot()

### Function for going in a square. Takes robot object and how many loops the robot should do ###
def Square(rob, loops):
    for i in range(loops):
        Help_Functions.GoXMeters(rob, 1, 1)
        Help_Functions.Stop()
        Help_Functions.TurnXDegLeft(rob, 90)
        Help_Functions.Stop()

Square(arlo, 1) # Do 1 Square