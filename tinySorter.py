import arduino
import cv2  # Import the OpenCV Library
import serial
import numpy as np  # Import the Numpy library
from tensorflow.keras.models import load_model
from keras import __version__


#Rahmen
img = cv2.imread("Bilder/Rahmen.png")
img = cv2.resize(img, (1200, 800))

#Kameraeinstellungen
camera = cv2.VideoCapture(0)  # create a VideoCapture object with the 'first' camera (your webcam)
camera.set(3, 320)
camera.set(4, 240)
camera.set(5, 60)
size = (224, 224)
#camera.set(15, 1.0)

#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

#KI-Modell
model = load_model('keras_model.h5', compile=False)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#Globale Variablen
Start = True
programmnummer = 1
ausgabe =""

anzahl_steine = 0
anzahl_steine_gesamt = 0
prozentwert = 0

Gelb_4x2 = 0
Blau_2x2 = 0
Gelb_2x2 = 0
Gelb_1x2 = 0
Grau_4x2 = 0
Rot_4x2 = 0
Blau_4x2 = 0

richtung = ""




labels = []
with open('labels.txt') as datei:
    for line in datei:
        zeile, label = line.split()
        labels.append(label)
print(labels)

#Funktion Dashboard anzeige
def dashboard():
    imgbearbeiten = img  # ausgebe bild zurücksetzen
    # dashboard bauen und ausgeben
    imgbearbeiten[75:315, 805:1125] = frame  # Cam auf Bild kopieren
    cv2.imshow("Image", imgbearbeiten)
    # cv2.imshow("Image", frame)

#Funltion steinerkennen
def steinerkennen():
    # Bild auswerten
    # bild normalisieren
    bild_res = cv2.resize(frame, size)
    bild_normalisiert = (bild_res.astype(np.float32) / 127) - 1
    # Load the image into the array
    data[0] = bild_normalisiert
    # run the inference
    prediction = model.predict(data)
    # print(prediction[0][programmnummer])
    # maxwar = str(int(100 * prediction.max()))
    # print(prediction)
    return prediction

#Funktion Kommunikation
def kommunikationlesen():
    serialread = int(arduino.readline())
    print(serialread)
    if serialread > 0:
       Start = True
       programmnummer = serialread
    elif serialread == 0:
       Start = False

# Funktion Wahrscheinlichkeitsberechnung
def prediktionauswerten(prediction):
    ausgewertete_steine = 0
    ausgewertete_steine_gesamt = 0
    prozent = 0

    if prediction[0][programmnummer] > 0.8:
        #arduino.write(bytes(1, 'utf-8'))
        richtung = "Links"
        print(richtung)
        print(labels[prediction.argmax()])
        ausgewertete_steine  = ausgewertete_steine +1
        ausgewertete_steine_gesamt = ausgewertete_steine_gesamt + 1

    elif prediction[0][0] < 0.1:
        #arduino.write(bytes(0, 'utf-8'))
        richtung = "Rechts"
        print(richtung)
        print(labels[prediction.argmax()])
        ausgewertete_steine_gesamt = ausgewertete_steine_gesamt + 1
    else:
        print("warten")
        print(labels[prediction.argmax()])

    anzahl_steine = ausgewertete_steine
    anzahl_steine_gesamt = ausgewertete_steine_gesamt


    if anzahl_steine > 0:
        prozent = anzahl_steine_gesamt / anzahl_steine
        prozentwert = prozent

    print(" Gesamt: "+ str(anzahl_steine_gesamt)+ "\n Gesuchte Steine: "+ str(anzahl_steine) +"\n Gefunden %: "+ str(prozent) )



# main loop - Hauptprogramm
while (True):
    ret, frame = camera.read()  # Capture frame by frame
    # kommunikationlesen()

    if Start == True:
        prediction = steinerkennen()
        prediktionauswerten(prediction)


    dashboard()

    if cv2.waitKey(1) & 0xFF == ord(' ') or cv2.waitKey(5) & 0xFF == 27:  # Stop if spacebar is detected
        break
camera.release()  # Cleanup after spacebar is detected.
cv2.destroyAllWindows()
