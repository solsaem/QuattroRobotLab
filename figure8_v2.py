import robot
import Help_Functions

arlo = robot.Robot()

### Function for going in a figure 8. Takes the robot object and how many loops the robot should do ###
def Figure8(rob, loops):
    for i in range(loops):
        Help_Functions.MovingTurn(rob, 270, 1)
        Help_Functions.GoXMeters(rob, 0.83, 1)
        Help_Functions.MovingTurn(rob, 270, -1)
        Help_Functions.GoXMeters(rob, 0.83, 1)

Figure8(arlo, 1) # Do 1 figure 8