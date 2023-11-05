# from picamera2 import Picamera2, Preview
# import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import sys
# import robot
import Help_Functions as hf
import math

##### GLOBAL VARIABLES FOR EASE OF TESTING (AND EASY TWEAKS) #####
# ORIGIN AND GOAL
ORIGIN = [0,0]
GOAL = [0, 50]

# RADII
LANDMARK_R = 5
ROBOT_R =  5

# GRID LIMITS
Y_LIM_NEG = -30
Y_LIM_POS = 100
X_LIM_NEG = -100
X_LIM_POS = 100

# OTHER
STEPS = 100
MAX_DIST = 100
HARD_CODED_LANDMARKS = []
OBSTACLES = 15

def normalize_point(previous_point, current_point, max_distance):
    '''
    Normalizes the distance to the new point, so all points are a set distance away from a previous point

    previous_point: The point closest to current_point
    current_point: The randomly generated point to be added a set distance from previous_point
    max_distance: The distance that the point should be from previous_point

    return: The point between previous_point to current_point where the distance from previous_point is max_distance
    '''
    # Normalize the distance to the maximum distance
    normalized_distance = max_distance / (hf.calculate_distance(previous_point, current_point))

    # Adjust the current point based on the normalized distance
    normalized_point = [
        previous_point[0] + (current_point[0] - previous_point[0]) * normalized_distance,
        previous_point[1] + (current_point[1] - previous_point[1]) * normalized_distance
    ]

    return normalized_point

def sort_points(points, target):
    '''
    Help function to sort current points based on distance from the new point

    points: The list of points to be sorted
    target: The point to be sorted after

    return: The sorted list of points
    '''
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
    '''
    Runs through all the branches in the tree, to find the shortest path to the goal

    points: All points in the tree
    origin: The point of origin (The start)
    goal: The destination (Finish line)

    return: The shortest path through the given points
    '''
    final_path = [[goal, points[-1][0]]]
    final_path.append(points[-1])
    # The while loop runs while the next point to add is not the origin
    while final_path[-1][1] != origin:
        # We then run through all points in the list
        for i in range(len(points)):
            # Then we find the point in the list, that is equal to the point linked to the with the previous point found, and add it to the final path
            if points[i][0] == final_path[-1][1]:
                final_path.append(points[i])
    return final_path

def is_collision_between_points(point1, point2, obstacles):
    '''
    Checks collision between two points with a given radius

    point1: The first point in the line to check for collisions
    point2: The second point in the line to check for collisions
    obstacles: The list of obstacles to check for collisions with on the given line

    return: True on collision, False on no collision
    '''
    x1, y1 = point1
    x2, y2 = point2

    for obstacle in obstacles:
        obstacle_x, obstacle_y, = obstacle

        # Calculate the distance between the line segment (point1 to point2) and the obstacle center
        dist = abs(
            (x2 - x1) * (obstacle_y - y1) - (y2 - y1) * (obstacle_x - x1)
        ) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Check if the distance is less than the sum of radii (collision condition)
        if dist <= LANDMARK_R+ROBOT_R:
            return True

    return False

def optimize_path_rrt(path, lmarks):
    '''
    Optimizes the given path

    path: The given path to optimize
    lmarks: All landmarks to avoid

    return: Most optimized path through the points given
    '''
    optimized_path = []
    if not is_collision_between_points(path[0][0], path[-1][1], lmarks):
        return [[path[0][0], path[-1][1]]]
    optimized_path = [path[0]]  # Initialize the optimized path with the first point

    for i in range(1, len(path)):
        current_point = path[i][0]
        previous_point = optimized_path[-1][0]

        if not is_collision_between_points(previous_point, current_point, lmarks):
            # No collision, skip the current point
            continue

        optimized_path.append(path[i])
    
    for i in range(len(optimized_path)-1):
        optimized_path[i][1] = optimized_path[i+1][0]
    optimized_path[-1][1] = path[-1][1]
    return optimized_path

def find_path(origin, landmarks, goal, grid_size_x_neg, grid_size_x_pos, grid_size_y_neg, grid_size_y_pos):
    '''
    RRT Path Finding function

    origin: The start of the path
    landmarks: All landmarks to avoid in the grid
    goal: The finish of the path
    grid_size_x_neg: The negative limit of the x-axis
    grid_size_x_pos: The positive limit of the x-axis
    grid_size_y_neg: The negative limit of the y-axis
    grid_size_y_pos: The positive limit of the y-axis

    return: All points in the RRT tree, The shortest path through those points
    '''
    # Initiate points with one point (origin)
    points = [[origin, origin]]
    sortedPoints = [[origin, origin]]
    counter = 0
    while True:
        print(counter)
        ### Get a random point [int, int]
        rand_point = [np.random.randint(grid_size_x_neg, grid_size_x_pos), np.random.randint(grid_size_y_neg, grid_size_y_pos)]

        sortedPoints = sort_points(points, rand_point)

        # Check for collisions (in steps)
        closest_valid_point = []
        for p in sortedPoints:
            normal_p = normalize_point(p[0], rand_point, MAX_DIST)
            if not is_collision_between_points(normal_p, p[0], landmarks):
                closest_valid_point = p
                break

        #points.append([[sortedPoints[0][0][0] + rand_point[0]/10, sortedPoints[0][0][1] + rand_point[1]/10], sortedPoints[0][0]]) # add the random point to the list of points with the closest point linked
        # Add point with closest point: [[new point], [closest previous point]]
        if not closest_valid_point == []:
            points.append([normalize_point(closest_valid_point[0], rand_point, MAX_DIST), closest_valid_point[0]])
        else:
            continue

        # If the random point generated is close enough to the goal, 
        # then we will start finding the shortest path going from the goal back to the origin
        # Go from  goal to origin through closest previous point
        if(hf.calculate_distance(points[-1][0], goal) < MAX_DIST):
            final_path = find_final_path(points, origin, goal)
            fully_optimzed = False
            while not fully_optimzed:
                original_path = final_path[:]

                fully_optimzed = final_path == original_path
            return points, final_path
        counter += 1

def draw_graph(path, lmarks, ylim_neg, ylim_pos, xlim_neg, xlim_pos):
    '''
    Help function for drawing the map

    path: The path to draw on the graph
    lmarks: All landmarks to avoid in the grid
    xlim_neg: The negative limit of the x-axis
    xlim_pos: The positive limit of the x-axis
    ylim_neg: The negative limit of the y-axis
    ylim_pos: The positive limit of the y-axis

    return: Nothing
    '''
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
    plt.show()

def generate_random_landmark(origin, goal):
    '''
    Function for generating random landmarks (for testing)

    origin: The start of the path
    goal: The finish line

    return: A single randomly generated landmark
    '''
    point = [np.random.randint(X_LIM_NEG, X_LIM_POS), np.random.randint(Y_LIM_NEG, Y_LIM_POS)]
    if (hf.check_collision(point, goal, LANDMARK_R, LANDMARK_R) or hf.check_collision(point, origin, LANDMARK_R, ROBOT_R)):
        return generate_random_landmark(origin, goal)
    else:
        return point

def main():
    # Initialize landmarks and goal
    lmarks = []
    goal = GOAL

    # Add random landmarks (for testing)
    for i in range(OBSTACLES):
        lmarks.append(generate_random_landmark(ORIGIN, goal))

    # Draw the initial graph (only landmarks)
    draw_graph([], lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

    # Run path finding function
    path, final  = find_path(ORIGIN, lmarks, goal, X_LIM_NEG, X_LIM_POS, Y_LIM_NEG, Y_LIM_POS)

    # Calculate angles that the robot should turn for each point in the path
    angles = []
    for point in final:
        angles.append(hf.calculate_angle(point[0][0], point[0][1], point[1][0], point[1][1]))
    print(angles)
    
    # Draw the whole tree
    draw_graph(path, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

    # Draw the path found
    draw_graph(final, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)
    
    # Optimize the path found
    final_smooth = optimize_path_rrt(final, lmarks)

    # Draw the optimized path found
    draw_graph(final_smooth, lmarks, Y_LIM_NEG, Y_LIM_POS, X_LIM_NEG, X_LIM_POS)

# Run code
# main()
