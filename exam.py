import Help_Functions as hf
import robot
import cv2
import time
import numpy as np
import path_find_copy as pf
import drive_landmarks as dl
import threading
import math
from ex5 import selflocalize_copy as sf

# L1 = 1      # (0,0)
# L2 = 2      # (0,300)
# L3 = 3      # (400,0)
# L4 = 4      # (400,300)

L1 = 4      # (0,0)
L2 = 9      # (0,300)
L3 = 8      # (400,0)
L4 = 3      # (400,300)

l_coords = {
    L1: (0.0, 0.0),     # Coordinates for landmark 1
    L2: (0.0, 300.0),   # Coordinates for landmark 2
    L3: (400.0, 0.0),   # Coordinates for landmark 3
    L4: (400.0, 300.0), # Coordinates for landmark 4
}
LANDMARKS = [L1, L2, L3, L4, L1]
SEEN_LANDMARKS = []
OBSTACLES = []
VISITED_OBSTACLES = []
CHECKED_LANDMARKS = []

reached_landmark = False
found_landmark = False


arlo = robot.Robot()
picam2 = hf.Camera_Init()

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

camera_matrix = hf.CAMERA_MATRIX

x = threading.Thread(target=sf.self_localize)
x.start()

def drive_towards_object(angle, dist):
    global reached_landmark
    real_angle = angle[2]/np.pi*180   # Converts radians to degrees
    # Turn towards landmamrk
    if real_angle < 0:
        # print("\nTurning right : " + str(real_angle))
        hf.TurnXDegRight(arlo, real_angle)
    else:
        # print("\nTurning left : " + str(real_angle))
        hf.TurnXDegLeft(arlo, real_angle)
    # Go to first landmark
    if dist < 100:
        hf.GoXCM(arlo, dist, 1, 1)
        reached_landmark = True
    else:
        reached = hf.GoXCM(arlo, dist/2, 1, 1)
        time.sleep(.25)

def run_RRT():
    # We know the estimated pose at this point, so we will orient the robot to face upwards
    
    return


for landmark in LANDMARKS:
    reached_landmark = False
    found_landmark = False
    degrees = 0
    target = 'landmark'
    while len(SEEN_LANDMARKS) < 2:
        CHECKED_LANDMARKS = []
        ids = sf.objectIDs
        dists = sf.dists
        angles = sf.angles
        unique_ids = np.unique(ids)
        # OBSTACLES = dl.Add_Landmarks_From_Image(aruco_corners, camera_matrix)
        # Check if there are no ids
        if not unique_ids is None:
            # Check all ids in the picture
            for id in unique_ids:
                if id not in CHECKED_LANDMARKS:
                    CHECKED_LANDMARKS.append(id)
                    if id in LANDMARKS and id not in SEEN_LANDMARKS:
                        SEEN_LANDMARKS.append(id)
                    elif id not in LANDMARKS and id not in OBSTACLES:
                        OBSTACLES.append(id)
                    # Check if current id is the landmark we are driving towards
                    # This code will run if we can see the next landmark
                    if target == 'landmark':
                        if id == landmark and not reached_landmark: 
                            found_landmark = True
                            drive_towards_object(angles[ids.index(id)], dists[ids.index(id)])
                    else:
                        if id not in VISITED_OBSTACLES and id not in LANDMARKS:
                            drive_towards_object(angles[ids.index(id)], dists[ids.index(id)])
                            target = 'landmark'
                            degrees = 0
        if not reached_landmark and not found_landmark:
            #Spins 360 degrees and checks for landmarks 
            hf.TurnXDegLeft(arlo, 40)
            time.sleep(0.25)
            degrees += 40
            if degrees > 360:
                #If no landmark is found, drive to random obstacle
                target = 'obstacle'
        time.sleep(10)

        # Face upwards
        hf.TurnXDegLeft(arlo, sf.pose.getTheta())

        time.sleep(0.5)

    while True:
        ids = sf.objectIDs
        dists = sf.dists
        angles = sf.angles
        ids = np.unique(ids)
        pos_list = []
        for id in ids:
            # X = dist * cos(angle)
            # Y = dist * sin(angle)
            if id != landmark:
                pos_list.append([sf.pose.getX() + (dists[ids.index(id)] * np.cos(angles[ids.index(id)])), sf.pose.getY() + (dists[ids.index(id)] * np.sin(angles[ids.index(id)]))])
            
        temp_path = pf.find_path(origin=(sf.pose.getX(), sf.pose.getY()), 
                                landmarks=pos_list, 
                                goal=l_coords(landmark),                                   
                                grid_size_x_neg=-100, 
                                grid_size_x_pos=500, 
                                grid_size_y_neg=-100, 
                                grid_size_y_pos=400)
     
        path = pf.optimize_path_rrt(temp_path, lmarks=pos_list)
        if len(temp_path) == 2:
            break
        dl.Drive_Path(path[0], math.degrees(sf.pose.getTheta()))



        #if not reached_landmark:
        #    # Path planning and drive one step
        #    _, path = pf.find_path([0, 0], OBSTACLES, landmark, -50, 450, -50, 350)
        #    path.reverse()
        #    prev_angle = 0
        #    for point in path:
        #        if point[1] == landmark:
        #            break
        #        angle = hf.calculate_angle(point[0][0], point[0][1], point[1][0], point[1][1])
        #        hf.TurnXDegRight(arlo, angle - prev_angle)
        #        dist = hf.calculate_distance(point[0], point[1])
        #        hf.GoXMeters(arlo, dist*10, 1, 1)
        #        prev_angle = angle
