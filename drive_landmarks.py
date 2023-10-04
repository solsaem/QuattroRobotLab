<<<<<<< Updated upstream


import Help_functions as hf
=======
import Help_Functions as hf
>>>>>>> Stashed changes
import robot
from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np
import grid_occ as grid_occ
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
		landmarks.append ([vector[0]/100, (np.sqrt(vector[2] ** 2 - vector[0] ** 2)/100 + 3)])

goal = [0,50]

path = pf.find_path(landmarks, goal, 100)
path.reverse()
path.append(goal)
print("path" + str(path))
prev_angle = 0
for i, _ in enumerate(path, start=1):
	if  len(path) == i:
		print("GOAL")
		break
	print("path[i]" + str(path[i]))
	print("path[i-1]" + str(path[i-1]))
	angle = 90 - (np.arccos((np.array(path[i])-np.array(path[i-1]))/np.linalg.norm((np.array(path[i])-np.array(path[i-1]))))/np.pi*180)[0]
	print("angle: " + str(angle))
	print("prev angle: " + str(prev_angle))
	print("Total angle: " + str(angle - prev_angle))
	hf.TurnXDegRight(arlo, angle - prev_angle)
	dist = np.linalg.norm(np.array(path[i-1]) - np.array(path[i]))
	print("dist" + str(dist))
	hf.GoXMeters(arlo, dist/10, 1, 1)
	prev_angle += angle





plt.plot([x for (x, y) in path], [y for (x, y) in path], '-b')
plt.scatter([x for (x, y) in landmarks], [y for (x, y) in landmarks], s=9**2, c='red')
plt.scatter(goal[0], goal[1], s=10**2, c='green')
plt.scatter(0,0, s=5**2, c='black')
plt.grid(True)
plt.ylim(0,100)
plt.xlim(-40,40)
plt.pause(0.01)  # Need for Mac
plt.savefig("path.png")
plt.show()

