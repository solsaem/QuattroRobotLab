import Help_Functions as hf
import robot
from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import path_find as pf

# Initialize robot
arlo = robot.Robot()

pos = [0,0]
goal = [0,40]

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

# Initialize camera
picam2 = hf.Camera_Init()

picam2.capture_file("img.jpg")
img = cv2.imread("img.jpg")
aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
ids = np.unique(ids)

def Add_Landmarks_From_Image(aruco_corners, camera_matrix):

	rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)

	landmarks = []
	for list in tvecs:
		for vector in list:
			landmarks.append ([vector[0]/100, (np.sqrt(vector[2] ** 2 - vector[0] ** 2)/100 + 3)])

	return landmarks

def Drive_Path(path, angle):
	prev_angle = angle

	for point in path:
		if point[1] == goal:
			break

		angle = hf.calculate_angle(point[0][0], point[0][1], point[1][0], point[1][1])
		hf.TurnXDegRight(arlo, angle - prev_angle)
		dist = hf.calculate_distance(point[0], point[1])
		hf.GoXCM(arlo, dist*10, 1, 1)
		prev_angle = angle

# Find landmarks in view of the camera
landmarks = Add_Landmarks_From_Image(aruco_corners, hf.CAMERA_MATRIX)

# Find path based on landmarks
_, path = pf.find_path([0, 0], landmarks, goal, -10, 10, 0, 100)
path.reverse()

# Drive the path
Drive_Path(path, 0)

# Draw the graph it thinks it drove (for testing)
pf.draw_graph(path, landmarks, -100, 100, -100, 100)