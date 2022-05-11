import cv2  # Import the OpenCV Library
import serial
import warnings
import numpy as np  # Import the Numpy library
import sys


img = cv2.imread("Bilder/Rahmen.png") #
img = cv2.resize(img, (1200, 800))

camera = cv2.VideoCapture(0)  # create a VideoCapture object with the 'first' camera (your webcam)
camera.set(3,320)
camera.set(4,240)
camera.set(5,60)
#camera.set(15, 1.0)

#arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

# main loop
while (True):
    ret, frame = camera.read()  # Capture frame by frame
    imgbearbeiten = img     # ausgebe bild zurücksetzen
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # frame = cv2.resize(frame, (250, 200))
    imgbearbeiten[75:315, 805:1125] = frame # Cam auf Bild kopieren
    cv2.imshow("Image", imgbearbeiten)

    if cv2.waitKey(1) & 0xFF == ord(' ') or cv2.waitKey(5) & 0xFF == 27:  # Stop if spacebar is detected
        break

camera.release()  # Cleanup after spacebar is detected.
cv2.destroyAllWindows()