import cv2
import time
import os
import HandTrackingModule as htm
import handVolumeControl as hvc
import handMouse as hm
import fingerOpen as fo
import numpy as np
from pynput.mouse import Button, Controller


##################################
wCam, hCam = 640, 480
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
maxLength,minLength = 300 , 0
mouse = Controller()

##################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = fo.FingerCounter()

    if fingers == [1,1,0,0,0]:
        hvc.volControl(0)

    if fingers == [1,1,1,0,0]:
        hm.mouse(wCam,hCam)
    
    if fingers == [0,0,0,0,0]:
        break


            
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Control Screen", img)
    cv2.waitKey(1)