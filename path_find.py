# from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import sys
import robot
import Help_Functions as hf

LANDMARK_R = 3.5
OBSTACLES = 15
ROBOT_R = 3.5
STEPS = 100
ORIGIN = [0,0]
MAX_DIST = 10
Y_LIM_NEG = -30
Y_LIM_POS = 100
X_LIM_NEG = -100
X_LIM_POS = 100


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


def sort_points(points, target):
    dists = []
    # go through all points and calculate each distance
    for point in points:
        dist = hf.calculate_distance(point[0], target)
        dists.append(dist)
    
    zipped = zip(dists, points) # zip the distance list with the points array 
    sortedZip = sorted(zipped) # sort the list from shortest to longest distance
    _, sortedPoints = zip(*sortedZip) # unzip the list, so we are left with the points in order of distance from shortest to longest
    return sortedPoints

def find_final_path(points, origin, goal):
    final_path = [[goal, points[-1][0]]]
    final_path.append(points[-1])
    # The while loop runs while the next point to add is not the origin
    while final_path[-1][1] != origin:
        print(final_path)
        # We then run through all points in the list
        for i in range(len(points)):
            # Then we find the point in the list, that is equal to the point linked to the with the previous point found, and add it to the final path
            if points[i][0] == final_path[-1][1]:
                final_path.append(points[i])
    return final_path

def check_collisions_in_steps(new_p, prev_p, lmarks):
    closest_valid_point = []
    collision = False
    for i in range(1,STEPS):
        p = [(prev_p[0][0]+((new_p[0]-prev_p[0][0])*(i/STEPS))), (prev_p[0][1]+((new_p[1]-prev_p[0][1])*(i/STEPS)))]
        for lmark in lmarks:
            if(hf.check_collision(p, lmark, LANDMARK_R, ROBOT_R)):
                collision = True
    if not collision:
        collision = False
    return collision

def smooth_path(path, lmarks, origin, goal):
    temp = path
    for i in range(len(temp)-1):
        for j in range(i+1, len(temp)):
            if not check_collisions_in_steps(temp[i][0], temp[j], lmarks):
                temp[i][1] = temp[j][0]
    return find_final_path(temp, origin, goal)

### Function for finding shortest path from origin to goal
def find_path(origin, landmarks, goal, grid_size_x_neg, grid_size_x_pos, grid_size_y_neg, grid_size_y_pos):
    # Initiate points with one point (origin)
    points = [[origin, origin]]
    sortedPoints = [[origin, origin]]

    while True:
        ### Get a random point [int, int]
        rand_point = [np.random.randint(grid_size_x_neg, grid_size_x_pos), np.random.randint(grid_size_y_neg, grid_size_y_pos)]

        sortedPoints = sort_points(points, rand_point)

        # Check for collisions (in steps)
        closest_valid_point = []
        for p in sortedPoints:
            if hf.calculate_distance(p[0], rand_point) > MAX_DIST:
                normal_p = normalize_point(p[0], rand_point, MAX_DIST)
            else:
                normal_p = rand_point
            if not check_collisions_in_steps(normal_p, p, landmarks):
                closest_valid_point = p
                break

        #points.append([[sortedPoints[0][0][0] + rand_point[0]/10, sortedPoints[0][0][1] + rand_point[1]/10], sortedPoints[0][0]]) # add the random point to the list of points with the closest point linked
        # Add point with closest point: [[new point], [closest previous point]]
        if not closest_valid_point == []:
            points.append([normalize_point(closest_valid_point[0], rand_point, MAX_DIST), closest_valid_point[0]])

        # If the random point generated is close enough to the goal, 
        # then we will start finding the shortest path going from the goal back to the origin
        # Go from  goal to origin through closest previous point
        if(hf.calculate_distance(points[-1][0], goal) < 10):
            final_path = find_final_path(points, origin, goal)
            #final_path_smooth = smooth_path(final_path, landmarks, origin, goal)
            return points, final_path#, final_path_smooth

def draw_graph(path, lmarks, ylim_neg, ylim_pos, xlim_neg, xlim_pos):
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
    plt.xlim(xlim_neg, xlim_pos)
    plt.ylim(ylim_neg, ylim_pos)

    # Show the plot
    plt.grid(True)
    plt.savefig("img3.png")
    plt.show()

def generate_random_landmark(origin, goal):
    point = [np.random.randint(X_LIM_NEG, X_LIM_POS), np.random.randint(Y_LIM_NEG, Y_LIM_POS)]
    if (hf.check_collision(point, goal, LANDMARK_R, LANDMARK_R) or hf.check_collision(point, origin, LANDMARK_R, ROBOT_R)):
        return generate_random_landmark(origin, goal)
    else:
        return point

def main():
    lmarks = []
    goal = [0, 50]
    for i in range(30):
        lmarks.append(generate_random_landmark(ORIGIN, goal))

    draw_graph([], lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

    path, final = find_path(ORIGIN, lmarks, goal, X_LIM_NEG, X_LIM_POS, Y_LIM_NEG, Y_LIM_POS)
    #path, final = find_path(ORIGIN, lmarks, goal, X_LIM_NEG, X_LIM_POS, Y_LIM_NEG, Y_LIM_POS)
    print(final)
    angles = []
    for point in final:
        angles.append(hf.calculate_angle(point[0][0], point[0][1], point[1][0], point[1][1]))
    print(angles)

    draw_graph(path, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

    draw_graph(final, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

    # draw_graph(final_smooth, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

