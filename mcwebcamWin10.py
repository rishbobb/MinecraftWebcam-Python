# Import Statements
import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui as gui
import time
import serial
import itertools
import signal
import sys
import pydirectinput

# Get relative coords
def getRelativeCoords(curx, cury, x, y):
    relx = x - curx
    rely = y - cury

    return relx, rely

# Cursor smoothening value
smoothening = 15

# Handle CTRL-C to exit gracefully
def signal_handler(signal, frame):
    print("Exiting program")
    cap.release()
    cv.destroyAllWindows()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

# Set mouse movement pause to 0 for smooth movement
gui.PAUSE = 0

# Get solution objects from mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Get video capture
cap = cv.VideoCapture(0)

# Variables to keep track of where the crosshair is
findx = 0
findy = 0

# Old values to average
oldx = 0
oldy = 0

# Shoulder movement list
walkingdiff = []
jumpingdiff = []
miningdiff = []
placingdiff = []

walk = False
jump = False
mining = False
placing = False

# Main while loop
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False,  smooth_landmarks=True) as pose:
    for i in itertools.count():

        # Get frame
        ret, frame = cap.read()

        # Flip frame
        frame = cv.flip(frame, 1)

        # Get pose data
        results = pose.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

        # Draw landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # pose_landmarks variable
        pose_landmarks = results.pose_landmarks
            
        # print pose landmarks
        if not results.pose_landmarks:
            continue

        # Get image dimensions
        image_height, image_width, _ = frame.shape
        
        # region Mining and using
        righthandy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * image_height
        lefthandy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * image_height

        miningdiff.append(righthandy)

        if len(miningdiff) < 5:
            continue

        miningworkingdata = np.diff(miningdiff)
        miningworkingdata = abs(miningworkingdata) > 100

        if True in miningworkingdata:
            #gui.click(button='left')
            gui.mouseDown(button='left')
            mining = True
        if not True in miningworkingdata and mining:
            gui.mouseUp(button='left')
            mining = False

        if len(miningdiff) == 20:
            miningdiff = []

        placingdiff.append(righthandy)
        
        if len(placingdiff) < 5:
            continue
        
        if lefthandy < 400 and not placing:
            gui.click(button='right')
            placing = True
        elif placing:
            placing = False


        # endregion
        
        # region Walking + Jumping
        walkingx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_width
        walkingdiff.append(walkingx)

        if len(walkingdiff) < 5:
            continue
        
        walkingworkingdata = np.diff(walkingdiff)
        walkingworkingdata = abs(walkingworkingdata) > 15
        if True in walkingworkingdata and not mining:
            #print('w!')
            gui.keyDown('ctrl')
            gui.keyDown('w')
            walk = True

        if not True in walkingworkingdata:                                                                                                    
            #print('not w')
            gui.keyUp('w')
            gui.keyUp('ctrl')
            walk = False
        
        # Reset every 60 samples
        if len(walkingdiff) == 15:
            walkingdiff = []


        # Jumping
        jumpingy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height
        jumpingdiff.append(jumpingy)

        jumpingworkingdata = np.diff(jumpingdiff)
        jumpingworkingdata = abs(jumpingworkingdata) > 40

        if True in jumpingworkingdata:
            gui.keyDown('space')
            jump = True
        else:
            gui.keyUp('space')
            jump = False

        if len(jumpingdiff) == 20:
            jumpingdiff = []

        # endregion

        # region Move Mouse
        x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width
        y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height
        x = int(x)
        y = int(y)

        # Scale to display size
        #x = x * 1
        #y = y * 1

        x = oldx + (x - oldx) / smoothening
        y = oldy + (y - oldy) / smoothening

        oldx = x
        oldy = y

        # Increase movement (trial and error)
        x = x * 18
        y = y * 15

        # Get the relative coordinates to move to
        x, y = getRelativeCoords(findx, findy, x, y)

        # Change to integer
        x = int(x)
        y = int(y)

        # Move the mouse
        if not walk and not jump and not mining:
            pydirectinput.move(x, y)
        
        # Update the find coordinates to keep track of location
        findx = findx + x
        findy = findy + y
    
        # endregion

        # Show frame    
        #cv.imshow("OpenCV", frame)

        # Exit key
        if cv.waitKey(20) & 0xFF==ord('d'):
            break

# Exit program
cap.release()
cv.destroyAllWindows()