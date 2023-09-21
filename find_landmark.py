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
#picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

camera_matrix = np.array([[1293, 0, 320], [0, 1293, 240], [0, 0, 1]])

dictionary_type = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.Dictionary_get(dictionary_type)

ids = None
while True:
        if not ids is None:

                picam2.capture_file("img.jpg")
                img = cv2.imread("img.jpg")
                aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
                if ids is None:
                        hf.GoXMeters(arlo, 2, 1, 0.5)
                        break
                rvecs, tvecs, objPoints = cv2.aruco.estimatePoseSingleMarkers(aruco_corners, 145, camera_matrix, None)
                print(tvecs)
                angle = np.arccos(tvecs[0][0] / np.linalg.norm(tvecs[0][0]) * np.array([0,0,1]))
                real_angle = angle[2]/np.pi*180
                if tvecs[0][0][0] > 0:
                        hf.TurnXDegRight(arlo, real_angle)
                else:
                        hf.TurnXDegLeft(arlo, real_angle)
                found = hf.GoXMeters(arlo, tvecs[0][0][2]/2000, 1, 0.5)
                time.sleep(0.5)
                if found == 0:
                        break
        else:
                hf.TurnXDegLeft(arlo, 20)
                time.sleep(0.5)
                picam2.capture_file("img.jpg")
                img = cv2.imread("img.jpg")
                aruco_corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, dictionary)
                print(ids)
