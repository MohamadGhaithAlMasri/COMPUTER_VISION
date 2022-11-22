import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject
import numpy as np
import mediapipe as mp
import time
import sendingDataToEsp as sender
import math

""""this code uses an updated versions of cvzone and other libraries 
 and this version gives us the ability to deal with multiple Hands 
 and recognizes the left and right hand even if you flipped them! """

"""so you should always use the same version murtaza use in his videos"""
"""cvzone 1.5 and above will use the two hand technique 
and now it contains the Hand Tracking Module with an updated and simplified set of functions"""

# arduino = SerialObject()
sender.base = "http://192.168.1.2/"

width_cam, height_cam = 1900, 1080

cap = cv2.VideoCapture(0)
cap.set(3, width_cam)
cap.set(4, height_cam)

detector = HandDetector(detectionCon=0.8, maxHands=2)  # object of HandDetector class
previous_time = 0
current_time = 0
pwm = 0
pwmBar = 400
pwmPer = 0
area = 0
direction = " "
path = " "

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img)  # now it's getting multiple hands
    # len(hands) shows us the number of hands are in
    """
    now no need for: lmList, bbox = detector.findPosition(img, draw=True)
    now  hands list will have different hands
    and each hand will have a dictionary inside in which it contains:
    lmList, bbox, center, type of hand (left or right)
    and each hand has it's own dictionary the defines it.
    """

    if hands:
        # Hand1(1st hand in the img)
        hand1 = hands[0]  # the first hand in the list
        lmList1 = hand1["lmList"]  # list of 21 landmarks points that is stored in lmList element
        """and it determines the pixels of width and height 
        of the taken image at a specific landmark and use it later as you wish"""
        # print(len(lmList1), lmList1)
        # print(bbox1) contains (x, y, width, height)
        bbox1 = hand1["bbox"]  # bounding box info= x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand= cx ,cy
        handType1 = hand1["type"]  # hand type= left or right
        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:  # if we have two hand at a time
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # list of 21 landmarks point
            bbox2 = hand2["bbox"]  # bounding box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx ,cy( the center of the bbox of the hand )
            handType2 = hand2["type"]  # hand type left or right

            fingers2 = detector.fingersUp(hand2)  # to find the number of fingers up of a specific hand
            if handType1 == "Left":
                if fingers1[0] == 1 and fingers1[1:] == [0, 0, 0, 0]:
                    path = sender.transfer("right")
                    direction = "Right"
                    print("right")
                elif fingers1[1] == 1 and fingers1[0] == 0 and fingers1[2:] == [0, 0, 0]:
                    path = sender.transfer("forward")
                    direction = "Forward"
                    print("forward")
                elif fingers1[0:4] == [0, 0, 0, 0] and fingers1[4] == 1:
                    path = sender.transfer("left")
                    direction = "Left"
                    print("left")
                elif fingers1[1:4] == [0, 0, 0] and fingers1[0] == 1 and fingers1[4] == 1:
                    path = sender.transfer("backward")
                    direction = "Backward"
                    print("backward")
                elif fingers1[0:] == [0, 0, 0, 0, 0]:
                    path = sender.transfer("stop")
                    direction = "Stop"
                    print("stop")
                # else:
                    # path = sender.transfer("/stop")
                    # direction = "Stop"
                    # print("stop")
            elif handType1 == "Right":
                if fingers1[0] == 1 and fingers1[1:] == [0, 0, 0, 0]:
                    path = sender.transfer("left")
                    direction = "Left"
                    print("left")
                elif fingers1[1] == 1 and fingers1[0] == 0 and fingers1[2:] == [0, 0, 0]:
                    path = sender.transfer("forward")
                    direction = "Forward"
                    print("forward")
                elif fingers1[0:4] == [0, 0, 0, 0] and fingers1[4] == 1:
                    path = sender.transfer("right")
                    direction = "Right"
                    print("right")
                elif fingers1[1:4] == [0, 0, 0] and fingers1[0] == 1 and fingers1[4] == 1:
                    path = sender.transfer("backward")
                    direction = "Backward"
                    print("backward")
                elif fingers1[0:] == [0, 0, 0, 0, 0]:
                    path = sender.transfer("stop")
                    direction = "Stop"
                    print("stop")
                # else:
                    # path = sender.transfer("/stop")
                    # direction = "Stop"
                    # print("stop")

            # pycharm length, info, img = detector.findDistance(lmList2[8], lmList2[4], img)
            length, info, img = detector.findDistance(lmList2[8][0:2], lmList2[4][0:2], img)
            # no draw: length, info = detector.findDistance(lmList1[8][0:2], lmList1[4][0:2])

            duty_cycle = int(np.interp(length, [50, 250], [0, 255]))
            res = list(map(int, str(duty_cycle)))

            pwmBar = int(np.interp(length, [50, 250], [400, 150]))

            pwmPer = int(np.interp(length, [50, 250], [0, 100]))
            smoothness = 2
            pwmPer = smoothness * round(pwmPer / smoothness)

            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, pwmBar), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{pwmPer} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 0, 0), 3)
            cv2.putText(img, f'PWM: {duty_cycle}', (40, 500), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255), 3)
            # print(fingers1, fingers2, res)
            if fingers2[4] == 0:
                path = sender.transfer(str(duty_cycle))
                cv2.circle(img, (info[4], info[5]), 10, (0, 255, 0), cv2.FILLED)
                print(duty_cycle)

            # arduino.sendData(res)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cv2.putText(img, direction, (10, 120), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)  # 1ms delay
