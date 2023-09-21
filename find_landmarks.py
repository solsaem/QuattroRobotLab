import Help_functions as hf
import robot
from picamera2 import Picamera2, Preview
import cv2
import time
import numpy as np

arlo = robot.Robot()

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
time.sleep(2)

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

camera_matrix = np.array([[1293, 0, 320], [0, 1293, 240], [0, 0, 1]])

ids = None
picam2.capture_file("img.jpg")
img = cv2.imread("img.jpg")
aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
print(ids)

rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)

print(aruco_corners)


print(tvecs)