# from picamera2 import Picamera2, Preview
# import cv2
import time
import numpy as np
import grid_occ as grid_occ
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import sys



# import robot
import Help_Functions as hf

landmark_radius = 3
obstacles = 15


def find_path(landmarks, goal, grid_size):
    robot_radius = 2.25
    steps = 20

    print("Landmarks: " + str(landmarks))

    robot_posX = 0
    robot_posY = 0
    robot_pos = [robot_posX, robot_posY]
    points = [[robot_pos,robot_pos]] # Index 0 in each inner list is a point. Index 1 is previous point.
    while True:
        rand_point = [np.random.uniform(-40,40), np.random.uniform(0,100)]

        # Gets distances from all points to rand_point
        dists = []
        for point in points:
            dists.append(np.linalg.norm(np.array(point[0]) - np.array(rand_point)))
        
        # Zips and sorts all distances
        zipped = zip(dists, points)
        sortedZip = sorted(zipped)
        _, sortedPoints = zip(*sortedZip)

        print(points)
        # Adds the random point to the list of points with the cloest point (with no collision) in index 1. 
        for point in sortedPoints:
            collision = False
            for i in range(0, steps + 1):
                for landmark in landmarks:
                    temp = [rand_point[0] + (4/5 * (point[0][0] - rand_point[0])), rand_point[1] + (4/5 * (point[0][1] - rand_point[1]))]
                    if (hf.check_distance(([temp[0] + (i/steps * (point[0][0] - temp[0])), temp[1] + (i/steps * (point[0][1] - temp[1]))]), landmark, robot_radius, landmark_radius)):
                        collision = True
            if collision == False:
                points.append([temp, point[0]])
        # Checks if any of the points are in a direct line to the goal.
        point = points[-1]
        collision = False
        #if hf.calc_dist(point[0], goal, 5, 5):
        for i in range(0, steps + 1):
            for landmark in landmarks:
                if (hf.calc_dist(([goal[0] + (i/steps * (point[0][0] - goal[0])), goal[1] + (i/steps * (point[0][1] - goal[1]))]), landmark, robot_radius, landmark_radius)):
                    collision = True
        if collision == False: 
            # Finds the final path.
            final_path = [point[0]]
            while final_path[- 1] != robot_pos: # Runs as longs as the the last elemesnt isn't robot pos.
                for point in points:
                    if point[0] == final_path[-1]: 
                        final_path.append(point[1])
            return final_path


        
#landmarks = ([[0, 15], [30, 30]])
#for i in range(0, obstacles):
#    val1 = np.random.randint(-60,60)
#    val2 = np.random.randint(-10,60)
#    if not hf.calc_dist([val1, val2], [0,0], landmark_radius, 5): 
#        landmarks.append([val1, val2])
#
#goal = [0, 50]
#
#plt.scatter([x for (x, y) in landmarks], [y for (x, y) in landmarks], s=landmark_radius**2, c='red')
#plt.scatter(goal[0], goal[1], s=10**2, c='green')
#plt.scatter(0,0, s=2.25**2, c='black')
#plt.ylim(-10,100)
#plt.xlim(-100,100)
#plt.show()
#
#path = find_path(landmarks, goal, grid_size=100)
#path.reverse()
#path.append(goal)
#
#
#
#plt.plot([x for (x, y) in path], [y for (x, y) in path], '-b')
#plt.scatter([x for (x, y) in landmarks], [y for (x, y) in landmarks], s=landmark_radius**2, c='red')
#plt.scatter(goal[0], goal[1], s=10**2, c='green')
#plt.scatter(0,0, s=2.25**2, c='black')
#plt.grid(True)
#plt.ylim(-10,100)
#plt.xlim(-100,100)
#plt.pause(0.01)  # Need for Mac
#plt.show()
