
import cv2              #Import the OpenCV Library
import numpy as np      #Import the Numpy library
import sys

camera = cv2.VideoCapture(0) #create a VideoCapture object with the 'first' camera (your webcam)

while(True):
    ret, frame = camera.read()             # Capture frame by frame   
    img = cv2.imread("Bilder/Rahmen.png")
    img = cv2.resize(img,(1200,800))
    frame = cv2.resize(frame,(250,200))#Load the image file into memory
    img[75:275,875:1125]=frame
    cv2.imshow("Image", img) 
    
    if cv2.waitKey(1) & 0xFF == ord(' '):  # Stop if spacebar is detected
        break

camera.release()                           # Cleanup after spacebar is detected.
cv2.destroyAllWindows()




