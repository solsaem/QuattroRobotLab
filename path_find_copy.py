# from picamera2 import Picamera2, Preview
# import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import sys
# import robot
import Help_Functions as hf

LANDMARK_R = 10
OBSTACLES = 15
ROBOT_R =  2.25
STEPS = 10
ORIGIN = [0,0]
MAX_DIST = 10


# Function to normalize a point based on a maximum distance
def normalize_point(previous_point, current_point, max_distance):
    # Normalize the distance to the maximum distance
    normalized_distance = max_distance / (hf.calculate_distance(previous_point, current_point))

    # Adjust the current point based on the normalized distance
    normalized_point = [
        previous_point[0] + (current_point[0] - previous_point[0]) * normalized_distance,
        previous_point[1] + (current_point[1] - previous_point[1]) * normalized_distance
    ]

    return normalized_point


### Function for finding shortest path from origin to goal
def find_path(origin, landmarks, goal, grid_size_x, grid_size_y):
    # Initiate points with one point (origin)
    points = [[origin, origin]]
    sortedPoints = [[origin, origin]]

    while True:
        ### Get a random point [int, int]
        rand_point = [np.random.randint(-grid_size_x, grid_size_x), np.random.randint(0, grid_size_y)]
        print("random point: " + str(rand_point))

        ### Find the closest point
        dists = []

        # go through all points and calculate each distance
        for point in points:
            dist = hf.calculate_distance(point[0], rand_point)
            print("dist: " + str(dist))
            dists.append(dist)

        # zip the distance list with the points array 
        zipped = zip(dists, points)
        # sort the list from shortest to longest distance
        sortedZip = sorted(zipped)
        print(sortedZip)
        # unzip the list, so we are left with the points in order of distance from shortest to longest
        _, sortedPoints  = zip(*sortedZip)

        closest_valid_point = []
        collision = False
        for p in sortedPoints:
            normal_p = normalize_point(p[0], rand_point, MAX_DIST)
            collision = False
            for i in range(STEPS):
                for lmark in lmarks:
                    if(hf.check_collision(normal_p, lmark, LANDMARK_R, ROBOT_R)):
                        collision = True
            if not collision:
                closest_valid_point = p
                break

        print("sorted points: " + str(sortedPoints))
        #points.append([[sortedPoints[0][0][0] + rand_point[0]/10, sortedPoints[0][0][1] + rand_point[1]/10], sortedPoints[0][0]]) # add the random point to the list of points with the closest point linked
        points.append([normalize_point(closest_valid_point[0], rand_point, MAX_DIST), closest_valid_point[0]])
        print("points: " + str(points))
        print("points[0]: " + str(points[0]))

        # If the random point generated is close enough to the goal, 
        # then we will start finding the shortest path going from the goal back to the origin
        if(hf.calculate_distance(points[-1][0], goal) < 10):
            final_path = [[goal, points[-1][0]]]
            final_path.append(points[-1])
            # The while loop runs while the next point to add is not the origin
            while final_path[-1][1] != origin:
                print(final_path)
                # We then run through all points in the list
                for i in range(len(points)):
                    print("points: " + str(points[i][0]))
                    print("finalpath[-1]: " + str(final_path[-1]))
                    # Then we find the point in the list, that is equal to the point linked to the with the previous point found, and add it to the final path
                    if points[i][0] == final_path[-1][1]:
                        final_path.append(points[i])
                    
            # We then return the final path
            return points, final_path

        # Check for collisions (in steps)
        # Add point with closest point: [[new point], [closest previous point]]
        # Go from  goal to origin through closest previous point


lmarks = [[0, 30], [50, 50], [-50, 50]]
goal = [0, 50]

path, final = find_path(ORIGIN, lmarks, goal, 100, 100)
print(path)

plt.figure()

# Loop through the data and plot each connection
for line in path:
    x_values = [line[0][0], line[1][0]]
    y_values = [line[0][1], line[1][1]]
    plt.plot(x_values, y_values, marker='o', linestyle='-', markersize=8)
plt.scatter([x for (x, y) in lmarks], [y for (x, y) in lmarks], s=LANDMARK_R**2, c='red')
# Set axis labels (you can customize these as needed)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.xlim(-100, 100)
plt.ylim(0, 100)

# Show the plot
plt.grid(True)
plt.show()

plt.figure()

# Loop through the data and plot each connection
for line in final:
    x_values = [line[0][0], line[1][0]]
    y_values = [line[0][1], line[1][1]]
    plt.plot(x_values, y_values, marker='o', linestyle='-', markersize=8)
plt.scatter([x for (x, y) in lmarks], [y for (x, y) in lmarks], s=LANDMARK_R**2, c='red')
# Set axis labels (you can customize these as needed)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.xlim(-100, 100)
plt.ylim(0, 100)

# Show the plot
plt.grid(True)
plt.show()