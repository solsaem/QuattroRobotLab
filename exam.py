import Help_Functions as hf
import robot
import cv2
import time
import numpy as np
import path_find as pf
import drive_landmarks as dl

# L1 = 1      # (0,0)
# L2 = 2      # (0,300)
# L3 = 3      # (400,0)
# L4 = 4      # (400,300)

L1 = 4      # (0,0)
L2 = 9      # (0,300)
L3 = 8      # (400,0)
L4 = 3      # (400,300)
LANDMARKS = [L1, L2, L3, L4, L1]
OBSTACLES = []
NEXT_LM = L1


arlo = robot.Robot()
picam2 = hf.Camera_Init()

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

camera_matrix = hf.CAMERA_MATRIX

for landmark in LANDMARKS:
    reached_landmark = False
    found_landmark = False
    while not reached_landmark:
        # Take picture and find landmarks in picture
        picam2.capture_file("img.jpg")
        img = cv2.imread("img.jpg")
        aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
        ids = np.unique(ids)
        # OBSTACLES = dl.Add_Landmarks_From_Image(aruco_corners, camera_matrix)
        # Check if there are no ids
        if not ids is None:
            # Check all ids in the picture
            for id in ids:
                # Check if current id is the landmark we are driving towards
                if id == landmark and not reached_landmark: # and id == NEXT_LM:
                    found_landmark = True
                    rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)
                    print(tvecs)
                    angle = np.arccos(tvecs[0][0] / np.linalg.norm(tvecs[0][0]) * np.array([0,0,1]))
                    real_angle = angle[2]/np.pi*180
                    # Turn towards landmamrk
                    if tvecs[0][0][0] > 0:
                        # print("\nTurning right : " + str(real_angle))
                        hf.TurnXDegRight(arlo, real_angle)
                    else:
                        # print("\nTurning left : " + str(real_angle))
                        hf.TurnXDegLeft(arlo, real_angle)
                    
                    # Go to first landmark
                    dist = tvecs[0][0][2]/10
                    if dist < 100:
                        hf.GoXCM(arlo, dist, 1, 1)
                        reached_landmark = True
                    else:
                        reached = hf.GoXCM(arlo, dist/2, 1, 1)
                        time.sleep(.25)
                elif not id in OBSTACLES:
                    # TODO Add landmark to obstacles
                    OBSTACLES.append(id)
        if not reached_landmark and not found_landmark:

            
            hf.TurnXDegLeft(arlo, 40)
            time.sleep(0.25)
        




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
