import cv2
import time
import os

import numpy as np

import handTrackingModule as htm

pTime = 0
#################################
xp, yp = 0, 0
#################################

detector = htm.handDetector(detectionCon=0.75)

folderPath = 'header'
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath} /{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[1]
deawColor = (0, 0, 255)
brushThickness = 15

#chanel ekak sada genema(kalupata thirayak)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)# uint8 magin thamai 255 hadala denne,coler code eka sadaha


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
while True:
    # 1. import img
    success, img = cap.read()
    img = cv2.flip(img, 1)#wama dakuna maru wena getaluwa visadeema
    #img[0:125, 0:1280] = header

    # 2. find lank marks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) !=0:


        #tip of index and midel fingle
        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # check with fingers up
        fingers = detector.fingersUp()
        #print(fingers)


        #if selection
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #ckick for the selection
            if y1<125:
                if 0< x1 <100:
                    deawColor = (255, 0, 255)
                elif 100< x1 <200:
                    deawColor = (255, 0, 0)
                elif 200< x1 < 300:
                    deawColor = (0, 255, 0)
                elif 300< x1 < 400:
                    deawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), deawColor, cv2.FILLED)
            print('sellection mood')

        #if Drowving mood
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, deawColor, 3, cv2.FILLED)
            print('Drowving mood')
            # mema if parat eka denme neththam patan gaddima 0,0 kandanka walin patan gani
            if xp == 0 and yp == 0:
                xp, yp = x1, y2

            cv2.line(img, (xp, yp), (x1,y1), deawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), deawColor, brushThickness)
            xp,yp = x1,y1


    #mee kotasen thamai cam eken api adina eke pata pennane
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    cv2.imshow('IMGES', img)
    cv2.imshow('IMGESCANVES', imgCanvas)
    cv2.waitKey(1)