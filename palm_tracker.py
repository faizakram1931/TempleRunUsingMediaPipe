#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 23:13:17 2022

@author: faizakram
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 22:21:13 2022

@author: faizakram
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 00:01:46 2022

@author: faizakram
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 23:55:10 2022

@author: faizakram
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 22:37:22 2022

@author: faizakram
"""
#https://poki.com/en/g/temple-run-2
import cv2
import mediapipe as mp
import math
from pynput.keyboard import Key, Controller
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
kb = Controller()
vid = cv2.VideoCapture(0)

def mapping_to_image_resolution(x,y,h,w):
  cx, cy = int(x * w), int(y * h)
  return cx,cy

def get_euclidean_distance(rx,ry,cx,cy):
    m_dist = ((rx - cx)*(rx - cx)) + ((ry - cy)*(ry - cy))
    return math.sqrt(m_dist)

def press_and_release(button):
    kb.press(button)
    kb.release(button)

def get_location_of_finger_parts(results,imgH, imgW):
    landMarkList = []
    
    if results.multi_handedness:
        label = results.multi_handedness[0].classification[0].label  # label gives if hand is left or right
        #account for inversion in webcams
        if label == "Left":
            label = "Right"
        elif label == "Right":
            label = "Left"
    
    if results.multi_hand_landmarks:  # returns None if hand is not found
        hand = results.multi_hand_landmarks[0] #results.multi_hand_landmarks returns landMarks for all the hands

        for id, landMark in enumerate(hand.landmark):
            xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
            landMarkList.append([id, xPos, yPos, label])
    return landMarkList


mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.9,
                      min_tracking_confidence=0.5)

h,w = 960,1280
rx,ry = int(w/2),int(h/2)
l_index = 0
r_index = 1
prev_state = 0
current_state = 0
key_pressed = ''
while(1):
    count = 0
    ret, frame = vid.read()
    if ret == True:
        frame = cv2.flip(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),1)
        results = hands.process(frame)
        handLandmarks = get_location_of_finger_parts(results, h, w)
        if(len(handLandmarks) != 0):
            
            #Count number of fingers
            if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
                count = count+1
            elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
                count = count+1
            if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
                count = count+1
            if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
                count = count+1
            if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
                count = count+1
            if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
                count = count+1
            
            cv2.putText(frame, 'NUMBER OF FINGERS FOUND: ' + str(count), (50, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,69,0), 5)
            
            prev_state = current_state
            if(count == 1):
                if handLandmarks[8][2] < handLandmarks[6][2]:
                    index_finger_mcp_x,index_finger_mcp_y = handLandmarks[5][1],handLandmarks[5][2]
                    index_finger_tip_x,index_finger_tip_y = handLandmarks[8][1],handLandmarks[8][2]
                    
                    if(index_finger_mcp_y != index_finger_tip_y):
                        slope = ((index_finger_mcp_x - index_finger_tip_x)/(index_finger_mcp_y-index_finger_tip_y))
                        
                        angle = round(math.degrees(math.atan(slope)))
                        cv2.putText(frame, 'ANGLE: ' + str(angle), (50, 200), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,69,0), 5)
                        if(angle > 15):
                            current_state = 1
                        elif(angle < -15):
                            current_state = 2
                        else:
                            current_state = 7
            elif(count == 2):
                current_state = 4
            elif(count == 5):
                current_state = 5
            elif(count == 4):
                current_state = 3
            else:
                current_state = 6

            if(prev_state != current_state):
                if(current_state == 1):
                    key_pressed = 'LEFT ARROW'
                    cv2.putText(frame, 'LEFT ARROW',  (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
                    press_and_release(Key.left)
                elif(current_state == 2):
                    key_pressed = 'RIGHT ARROW'
                    cv2.putText(frame, 'RIGHT ARROW', (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
                    press_and_release(Key.right)
                elif(current_state == 4):  
                    key_pressed = 'UP ARROW'
                    press_and_release(Key.up)
                    cv2.putText(frame, 'UP ARROW',    (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
                elif(current_state == 5):
                    key_pressed = 'DOWN ARROW'
                    press_and_release(Key.down)
                    cv2.putText(frame, 'DOWN ARROW',  (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
                elif(current_state == 3):
                    key_pressed = 'RESTARTING'
                    cv2.putText(frame, 'SPACE BAR',   (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
                    press_and_release(Key.space)
            else:
                cv2.putText(frame, 'IDLE', (50, 300), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 0), 5)
             
    cv2.putText(frame, 'LAST KEY PRESSED: ' + key_pressed,(50, 400), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 200, 50), 5)
    frame = cv2.resize(frame,(640,480))
    cv2.imshow('frame', cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()