import cv2
import time
import HandTrackingModule as htm
import numpy as np 
import math
from pynput.mouse import Button, Controller
import fingerOpen as fo

wCam, hCam = 640, 480
mouse = Controller()
detector = htm.handDetector(detectionCon=0.7)
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

def mouse(wCam, hCam):
    x1Check = 0 
    y1Check = 0
    x2Check = 0
    y2Check = 0

    lagRec = 3
    mouse = Controller()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw = False)
        fingers = fo.FingerCounter()

        if len(lmList) !=0:
            #print(lmList[4], lmList[8])

            x1, y1 = lmList[12][1], lmList[12][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            

            if abs(x1Check - x1) > lagRec:
                x1Check = x1        
            if abs(y1Check - y1) > lagRec:
                y1Check = y1   
            if abs(x2Check - x2) > lagRec:
                x2Check = x2        
            if abs(y2Check - y2) > lagRec:
                y2Check = y2
            
            cx, cy = (x1Check+x2Check)//2, (y1Check+y2Check)//2

            cv2.circle(img,(x1,y1), 15, (255, 0, 255), cv2.FILLED)
            if (fingers[2] == 1 ):
                cv2.circle(img,(x2,y2), 15, (255, 0, 255), cv2.FILLED)

            mx = np.interp(cx,[0.2*wCam, 0.8*wCam], [2560,0])
            my = np.interp(cy,[0.2*hCam, 0.8*hCam], [0,1600])
            mouse.position = (mx, my)

            click = math.hypot(abs(x2 - x1), abs(y2 - y1))
            
            #print(click)
            

            if fingers == [0,1,1,0,0] and click <= 30:
                mouse.press(Button.left)

            if fingers == [0,1,1,0,0] and click >= 30:
                mouse.release(Button.left)

            if fingers == [1,1,1,0,0] and click <= 30:
                mouse.press(Button.right)

            if fingers == [1,1,1,0,0] and click >= 30:
                mouse.release(Button.right)
            
            
        #print(mouse.position)
        if fingers == [1,1,1,0,1]:
            break
        cv2.imshow("Control Screen", img)
        cv2.waitKey(1)
    return

mouse(wCam,hCam)