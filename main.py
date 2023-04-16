#INITIAL SETUP
#----------------------------------------------------------------
import cv2
from cvzone import HandTrackingModule, overlayPNG
import numpy as np
import os

# Load the intro, loss, and win screen images
folderPath = 'frames'
mylist = os.listdir(folderPath)
graphic = [cv2.imread(f'{folderPath}/{imPath}') for imPath in mylist]

intro =graphic[0]                   # read frames\img 1 in the intro variable
kill = graphic[1]                   # read frames\img 2 in the kill variable
winner =graphic[2]                  # read frames\img 3 in the winner variable
cam = cv2.VideoCapture(0)              #read the camera

cam = cv2.VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=1,detectionCon=0.77)

#INITILIZING GAME COMPONENTS
#----------------------------------------------------------------
folderPath2 = 'img'
mylist2 = os.listdir(folderPath2)
graphic2 =[cv2.imread(f'{folderPath2}/{imPath}')for imPath in mylist2]

sqr_img = graphic2[1]                  #read img\sqr (1) in the sqr_img variable
mlsa = graphic2[0]                      #read img\mlsa in the mlsa variable

#INTRO SCREEN WILL STAY UNTIL Q IS PRESSED
gameOver = False
NotWon =True

#GAME LOGIC UPTO THE TEAMS
#-----------------------------------------------------------------------------------------
while not gameOver:
    success, img = cam.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Draw the square image and the MLSA logo
    img[0:200, 0:200] = sqr_img
    img[200:330, 30:170] = mlsa

    if lmList:
        # Get the coordinates of the index finger tip
        x1, y1 = lmList[8][1:]

        # Check if the index finger is within the square
        if 0 < x1 < 200 and 0 < y1 < 200:
            # Draw a green circle around the finger tip if it's within the square
            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

            # Check if the finger has moved from left to right within the square
            if x1 > 100 and x1 < 200:
                # Player has won the game
                NotWon = False

    # Display the intro screen until the player presses Q
    if cv2.waitKey(1) == ord('q'):
        break
    cv2.imshow("Dalgona Cookie Game", intro)

#LOSS SCREEN
if NotWon:
    for i in range(10):
        # Display the loss screen for a few seconds
        cv2.imshow("Dalgona Cookie Game", kill)
        cv2.waitKey(500)
        cv2.imshow("Dalgona Cookie Game", intro)
        cv2.waitKey(500)

    # Wait for the player to press Q to exit
    while True:
        cv2.imshow("Dalgona Cookie Game", kill)
        if cv2.waitKey(1) == ord('q'):
            break

#WIN SCREEN
else:
    # Display the win screen until the player presses Q
    while True:
        cv2.imshow("Dalgona Cookie Game", winner)
        if cv2.waitKey(1) == ord('q'):
            break

#destroy all the windows
cam.release()
cv2.destroyAllWindows()
