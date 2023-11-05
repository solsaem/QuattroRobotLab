import Help_Functions as hf
import robot
import cv2
import time
import numpy as np
import path_find as pf
import camera

# L1 = 1      # (0,0)
# L2 = 2      # (0,300)
# L3 = 3      # (400,0)
# L4 = 4      # (400,300)

L1 = 1      # (0,0)
L2 = 2      # (0,300)
L3 = 3      # (400,0)
L4 = 4      # (400,300)
LANDMARKS = [L1, L2, L3, L4, L1]
VISITED_OBSTACLES = []
start = time.perf_counter()

arlo = robot.Robot()

picam2 = hf.Camera_Init()

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

camera_matrix = hf.CAMERA_MATRIX
reached_landmark = False
found_landmark = False

degrees = 0

def drive_random(landmark):
    global degrees, reached_landmark, found_landmark
    while not reached_landmark:
        print("In function while loop")
        picam2.capture_file("img.jpg")
        img = cv2.imread("img.jpg")
        aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
        print(f"Robot sees: {ids}")
#ids = np.unique(ids)
            # Check if there are no ids
        if not ids is None:
                # Check all ids in the picture
            if landmark in ids:
                degrees = 0
                return
            for id in ids:
                    # Check if current id is the landmark we are driving towards
                if id > 4 and not reached_landmark and id not in VISITED_OBSTACLES: # and id == NEXT_LM:
                    rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)
                    print(tvecs)
                    angle = np.arccos(tvecs[list(ids).index(id)][0] / np.linalg.norm(tvecs[list(ids).index(id)][0]) * np.array([0,0,1]))
                    real_angle = angle[2]/np.pi*180
                        # Turn towards landmamrk
                    if tvecs[list(ids).index(id)][0][0] > 0:
                            # print("\nTurning right : " + str(real_angle))
                        hf.TurnXDegRight(arlo, real_angle)
                    else:
                            # print("\nTurning left : " + str(real_angle))
                        hf.TurnXDegLeft(arlo, real_angle)

                        # Go to first landmark
                    dist = tvecs[list(ids).index(id)][0][2]/10
                    if dist < 100:
                        print("Going sideways")
                        #hf.GoXCM(arlo, dist - 20, 1, 1)
                        VISITED_OBSTACLES.append(id)
                        degrees = 0
                        hf.TurnXDegLeft(arlo, 90)
                        hf.GoXCM(arlo, 100, 1, 1)
                        return
                    else:
                        reached = hf.GoXCM(arlo, dist/2, 1, 1)
                            #time.sleep(.15)
                    degrees = 0
                    return
        if not reached_landmark:
            if degrees < 360:
                degrees += 30
                hf.TurnXDegLeft(arlo, 30)
                time.sleep(0.25)
            else:
                degrees = 0
                return





for landmark in LANDMARKS:
    VISITED_OBSTACLES = []
    reached_landmark = False
    found_landmark = False
    while not reached_landmark:
        print(f"----------------Looking for {landmark}-------------")
        # Take picture and find landmarks in picture
        picam2.capture_file("img.jpg")
        img = cv2.imread("img.jpg")
        aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
        print(f"Robot sees: {ids}")
        #ids = np.unique(ids)
        # Check if there are no ids
        if not ids is None:
            # Check all ids in the picture
            for id in ids:
                # Check if current id is the landmark we are driving towards
                if id == landmark and not reached_landmark: # and id == NEXT_LM:
                    found_landmark = True
                    rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)
                    print(tvecs)
                    angle = np.arccos(tvecs[list(ids).index(id)][0] / np.linalg.norm(tvecs[list(ids).index(id)][0]) * np.array([0,0,1]))
                    real_angle = angle[2]/np.pi*180
                    # Turn towards landmamrk
                    if tvecs[list(ids).index(id)][0][0] > 0:
                        # print("\nTurning right : " + str(real_angle))
                        hf.TurnXDegRight(arlo, real_angle)
                    else:
                        # print("\nTurning left : " + str(real_angle))
                        hf.TurnXDegLeft(arlo, real_angle)
                    
                    # Go to first landmark
                    dist = tvecs[list(ids).index(id)][0][2]/10
                    if dist < 100:
                        completed = hf.GoXCM(arlo, dist - 20, 1, 1)
                        hf.GoXCM(arlo, dist - 20, 0, 1)
                        if completed:
                            reached_landmark = True
                        found_landmark = completed
                    else:
                        found_landmark = hf.GoXCM(arlo, dist/2, 1, 1)
                        #time.sleep(.15)
                    break
        if not reached_landmark and not found_landmark:
            if degrees < 360:
                degrees += 30
                hf.TurnXDegLeft(arlo, 30)
                time.sleep(0.25)
            else:
                degrees = 0
                drive_random(landmark)

end = time.perf_counter() - start
print("\nFinished in : " + str(end))
print("GOAL")



#DANCE TIME

while True:
    arlo.go_diff(100, 100, 0, 1)
    time.sleep(1)
    hf.Stop(arlo)
    time.sleep(0.1)
    arlo.go_diff(100, 100, 1, 0)
    time.sleep(1)
    hf.Stop(arlo)
    time.sleep(0.1)

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

