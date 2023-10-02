

import Help_functions as hf
import robot
from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np
import ex4.grid_occ as grid_occ
import matplotlib.pyplot as plt
import path_find as pf

arlo = robot.Robot()

pos = [0,0]

picam2 = hf.Camera_Init()

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

camera_matrix = hf.CAMERA_MATRIX
ids = None
picam2.capture_file("img.jpg")
img = cv2.imread("img.jpg")
cv2.imwrite("img2.jpg", img)
aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
print(ids)

rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)

landmarks = []

for list in tvecs:
	for vector in list:
		landmarks.append ([vector[0], np.sqrt(vector[2] ** 2 - vector[0] ** 2)])

goal = [0,50]

path = pf.find_path(landmarks, goal, 100)
path.reverse()
path.append(goal)

for i, point in enumerate(path):
	angle = np.arccos((point - path[i-1]) / np.linalg.norm(point - path[i-1]) * np.array([0,1]))
	if (i == 0):
	    angle = np.arccos(point / np.linalg.norm(point) * np.array([0,1]))