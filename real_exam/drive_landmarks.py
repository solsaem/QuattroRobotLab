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

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

def Drive_Path(path, angle):
	print(f"NOW DRIVING RRT with path: {path}")
	prev_angle = -angle

	for point in path:
		print(point)
		#if point[1] == goal:
		#	break

		angle = hf.calculate_angle(point[0][0], point[0][1], point[1][0], point[1][1])
		hf.TurnXDegRight(arlo, angle - prev_angle)
		dist = hf.calculate_distance(point[0], point[1])
		hf.GoXCM(arlo, dist*10, 1, 1)
		prev_angle = angle
