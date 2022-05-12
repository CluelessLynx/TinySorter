import cv2  # Import the OpenCV Library
import serial
import warnings
import numpy as np  # Import the Numpy library
import sys
import os
import time
from tensorflow.keras.models import load_model


img = cv2.imread("Bilder/Rahmen.png") #
img = cv2.resize(img, (1200, 800))


camera = cv2.VideoCapture(0)  # create a VideoCapture object with the 'first' camera (your webcam)
camera.set(3,320)
camera.set(4,240)
camera.set(5,60)
size = (224, 224)
#camera.set(15, 1.0)

#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)


model = load_model('keras_model.h5', compile=False)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
Start = True

def dashboard():
    imgbearbeiten = img  # ausgebe bild zurücksetzen
    # dashboard bauen und ausgeben
    imgbearbeiten[75:315, 805:1125] = frame  # Cam auf Bild kopieren
    cv2.imshow("Image", imgbearbeiten)
    # cv2.imshow("Image", frame)


def steinerkennen():
    # Bild auswerten
    # bild normalisieren
    bild_res = cv2.resize(frame, size)
    bild_normalisiert = (bild_res.astype(np.float32) / 127) - 1
    # Load the image into the array
    data[0] = bild_normalisiert
    # run the inference
    prediction = model.predict(data)
    maxwar = str(int(100 * prediction.max()))
    print(prediction)

def kommunikationlesen():
    serialread = int(arduino.readline())
    print(serialread)
    if serialread > 0:
       Start = True
       programmnummer = serialread
    elif serialread == 0:
       Start == False


# main loop
while (True):
    ret, frame = camera.read()  # Capture frame by frame
    # kommunikationlesen()

    if Start == True:
        steinerkennen()

    dashboard()

    if cv2.waitKey(1) & 0xFF == ord(' ') or cv2.waitKey(5) & 0xFF == 27:  # Stop if spacebar is detected
        break
camera.release()  # Cleanup after spacebar is detected.
cv2.destroyAllWindows()
