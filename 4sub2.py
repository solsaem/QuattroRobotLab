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


def find_path(landmarks, goal, grid_size):
    search_radius = 10
    robot_radius = 2.25
    point_count = 8
    steps = 10
    landmark_radius = 2

    robot_posX = 0
    robot_posY = 0

    # Creating randoom points 
    while True:
        points = []
        for _ in range(0,point_count):
            points.append( [np.random.uniform(-search_radius + robot_posX, search_radius + robot_posY), np.random.uniform(-search_radius + robot_posX, search_radius + robot_posY)])
        break
    print(points)

    colliding_points = []
    non_colliding_points = [] 
    for point in points:
        collision = False
        for i in range (0, steps):
            for landmark in landmarks:
                if (hf.calc_dist(([robot_posX + (i/steps * point[0]), robot_posY + point[1] * i/steps]), landmark, robot_radius, landmark_radius)):
                    collision = True
        if not collision:
            non_colliding_points.append(point)
        else: 
            colliding_points.append(point)
            print("\nCOLLISION !!!!\n")

    print("\nCollisions:")
    print(colliding_points)
    print("#################\n")

    
    # Calculating euclidean distances
    dists = []
    for point in non_colliding_points:
        dists.append(np.linalg.norm(np.array(point) - np.array(goal)))
        

    zipped = zip(dists, points)
    sortedZip = sorted(zipped)
    _, sortedPoints = zip(*sortedZip)
    return sortedPoints[:2]
    

    
print(find_path( ([[0, 5], [30, 30]]), [0, 50], grid_size=100))


# dist = np.linalg.norm(point1 - goal)





