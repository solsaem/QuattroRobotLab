

import Help_functions as hf
import robot
from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np
import ex4.grid_occ as grid_occ
import matplotlib.pyplot as plt

arlo = robot.Robot()

pos = [0,0]

picam2 = hf.Camera_Init()

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

# OLD ONE: camera_matrix = np.array([[1293, 0, 320], [0, 1293, 240], [0, 0, 1]])
camera_matrix = hf.CAMERA_MATRIX
ids = None
picam2.capture_file("img.jpg")
img = cv2.imread("img.jpg")
cv2.imwrite("img2.jpg", img)
aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
print(ids)

rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)

#print(aruco_corners)

print("Vectors:")
print(tvecs)

#print("angle:")
#angle = np.arccos(tvecs[0][0] / np.linalg.norm(tvecs[0][0]) * np.array([0,0,1]))

points = []

for list in tvecs:
	for vector in list:
		points.append ([vector[0], np.sqrt(vector[2] ** 2 - vector[0] ** 2)])

map = grid_occ.GridOccupancyMap()
map.populate(points)
plt.clf()
map.draw_map()
plt.savefig("result.png")
plt.show()

