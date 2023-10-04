# from picamera2 import Picamera2, Preview
# import cv2
import time
import numpy as np
import ex4.grid_occ as grid_occ
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import sys
# import robot
import Help_Functions as hf

LANDMARK_R = 2
OBSTACLES = 15
ROBOT_R =  2.25
STEPS = 10
ORIGIN = [0,0]

def find_path(landmarks, goal, grid_size_x, grid_size_y):
    points = [[ORIGIN, ORIGIN]]
    sortedPoints = [[ORIGIN, ORIGIN]]
    while True:
        # Get a random point
        rand_point = [np.random.randint(-grid_size_x, grid_size_x), np.random.randint(0, grid_size_y)]
        print("random point: " + str(rand_point))
        # Find the closest point
        dists = []
        for point in points:
            dist = hf.calculate_distance(point[0], rand_point)
            print("dist: " + str(dist))
            dists.append(dist)
        if len(points) > 0:
            zipped = zip(dists, points)
            sortedZip = sorted(zipped)
            print(sortedZip)
            _, sortedPoints  = zip(*sortedZip)

        print("sorted points: " + str(sortedPoints))
        points.append([rand_point, sortedPoints[0][0]])
        print("points: " + str(points))
        print("points[0]: " + str(points[0]))

        if(hf.calculate_distance(points[-1], goal) < 30):
            final_path = [points[-1]]
            while final_path[-1][1] != ORIGIN:
                final_path.append(points.index(final_path[-1][1]))
            final_path.append(ORIGIN)
            break
    return points
        # Check for collisions (in steps)
        # Add point with closest point: [[new point], [closest previous point]]
        # Check if new point is within vicinity of goal
        # Go from  goal to origin through closest previous point


lmarks = []
goal = [0, 50]

path = find_path(lmarks, goal, 100, 100)
print(path)

plt.plot([x for (x, y) in path], [y for (x, y) in path], '-b')
plt.scatter([x for (x, y) in lmarks], [y for (x, y) in lmarks], s=LANDMARK_R**2, c='red')
plt.scatter(goal[0], goal[1], s=10**2, c='green')
plt.scatter(0,0, s=2.25**2, c='black')
plt.grid(True)
plt.ylim(-10,100)
plt.xlim(-100,100)
plt.pause(0.01)  # Need for Mac
plt.show()