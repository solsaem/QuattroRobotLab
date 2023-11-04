import math

L1 = 1
L2 = 2
L3 = 3
L4 = 4

L_DICT = {
    L1: (0,0),
    L2: (0, 300),
    L3: (400, 0),
    L4: (400, 300)
}

LANDMARKS = [L1, L2, L3, L4, L1]

localized = False

current_pos = (0,0)

def Localize():
    # Run self localization algorithm to estimate the robot's position
    return

def RRT(pos, goal):
    # Run RRT algorithm to find a path to the current goal
    path = []
    return path

def drive_path_while_checking_obstacles(path):
    # Given the path, we want to start driving, while checking for new obstacles in the path
    # If new obstacle appears, then return from the function to run RRT again
    return

def main():
    while len(LANDMARKS) > 0:
        target = LANDMARKS[0]
        if not localized:
            localized = Localize()
        else:
            while math.dist(current_pos, L_DICT(target)) > 40:
                path = RRT(current_pos, L_DICT(target))
                drive_path_while_checking_obstacles(path)
            LANDMARKS.pop(0) # Remove the landmark we drove to from landmarks

    # Once all landmarks have been reached, do a victory dance

main()