import cv2
import time
import os
import HandTrackingModule as htm
import math
import numpy


##################################
wCam, hCam = 640, 480
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
maxLength,minLength = 300 , 0

##################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

def FingerCounter():
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            rows, cols = (5, 5)

            if len(lmList) != 0:
                fingers = []
                
                distances = [[0]*cols]*rows
                # Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                
                '''for x in range(0,4):
                    for y in range(0,4):
                        ax, ay = lmList[tipIds[x]][1], lmList[tipIds[x]][2]
                        bx, by = lmList[tipIds[y]][1], lmList[tipIds[y]][2]
                        length = math.hypot(bx-ax,by-ay)
                        distances[x][y] = length
                        return
                    return'''
                return fingers

