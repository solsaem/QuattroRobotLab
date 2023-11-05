
import Help_Functions as hf
import robot
import cv2
import time
import numpy as np
import path_find as pf
import drive_landmarks as dl
import threading
import math
import selflocalize as sf


arlo = robot.Robot()

x = threading.Thread(target=sf.self_localize)
x.start()

time.sleep(2)

turns = 1
degrees = 0
#hf.GoXCM(arlo, 200, 1, 1)

while degrees < 30:
	hf.TurnXDegRight(arlo, 30)
	print(f"turned {turns} times")
	degrees += 30
	time.sleep(2)
	turns += 1
