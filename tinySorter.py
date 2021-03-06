# import arduino
import cv2  # Import the OpenCV Library
import serial
import numpy as np  # Import the Numpy library
from tensorflow.keras.models import load_model
from keras import __version__


#Rahmen
img = cv2.imread("Bilder/Rahmen.png")
img = cv2.resize(img, (1200, 800))

#Kameraeinstellungen
camera = cv2.VideoCapture(1)  # create a VideoCapture object with the 'first' camera (your webcam)
camera.set(3, 320)
camera.set(4, 240)
camera.set(5, 60)
size = (224, 224)
#camera.set(15, 1.0)

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

#KI-Modell
model = load_model('keras_model.h5', compile=False)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#Globale Variablen
programmnummer = 0
ausgabe =""

anzahl_steine = 0
anzahl_steine_gesamt = 0
prozentwert = 0.0

stein_gesamt = 0
stein_gefunden = 0
stein_jetzt = 0
stein_prozent = 0
waittime = 0

dashbordsteineanzeige = [0, 0, 0, 0, 0, 0, 0]

Gelb_4x2 = 0
Gelb_2x2 = 0

Blau_4x2 = 0
Blau_2x2 = 0

Rot_4x2 = 0
Rot_2x2 = 0

Grau_4x2 = 0



richtung = ""




labels = []
with open('labels.txt') as datei:
    for line in datei:
        zeile, label = line.split()
        labels.append(label)
print(labels)

#Funktion Dashboard anzeige
def dashboard(dashbordsteineanzeige, Bild):
    imgbearbeiten = Bild  # ausgebe bild zurücksetzen
    # dashboard bauen und ausgeben
    imgbearbeiten[75:315, 805:1125] = frame  # Cam auf Bild kopieren

    cv2.putText(img=imgbearbeiten, text='Tiny Sorter ', org=(170, 150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text='         4x2          2x2', org=(120, 210), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)

    cv2.putText(img=imgbearbeiten, text='Blau', org=(120, 270), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[3]), org=(285, 270), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[4]), org=(505, 270), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)

    cv2.putText(img=imgbearbeiten, text='Gelb', org=(120, 330), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[1]), org=(285, 330), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[2]), org=(505, 330), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)

    cv2.putText(img=imgbearbeiten, text='Rot', org=(120, 390), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[5]), org=(285, 390), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)
    cv2.putText(img=imgbearbeiten, text=str(dashbordsteineanzeige[6]), org=(505, 390), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=3)

    cv2.imshow("Image", imgbearbeiten)
    # cv2.imshow("Image", frame)


#Funltion steinerkennen
def steinerkennen(frame_ki):
    # Bild auswerten
    # bild normalisieren
    bild_res = cv2.resize(frame_ki, size)
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
    print(type(serialread))
    return serialread



# Funktion Wahrscheinlichkeitsberechnung
def prediktionauswerten(prediction):

    if prediction[0][programmnummer] > 0.6:
        arduino.write(bytes("2", 'utf-8'))
        richtung = "Links"
        print(richtung)
        print(labels[prediction.argmax()])  # gesuchter Stein
        gefunden = "True"

    elif prediction[0][0] < 0.3:
        arduino.write(bytes("1", 'utf-8'))
        richtung = "Rechts"
        print(richtung)
        print(labels[prediction.argmax()])
        gefunden ="False"

    else:
        print("warten")
        print(labels[prediction.argmax()])
        gefunden = "nichts"

    return gefunden


# main loop - Hauptprogramm
while (True):
    ret, frame = camera.read()  # Capture frame by frame
    frame_ki = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    stein_jetzt =""
    while arduino.in_waiting:
        programmnummer = kommunikationlesen()

    if programmnummer > 0:
        prediction = steinerkennen(frame_ki)
        if prediction[0][0] < 0.4 and waittime > 10:
            stein_jetzt = prediktionauswerten(prediction)
            waittime = 0
            print("stein sortiert")
        elif prediction[0][0] < 0.4:
            waittime = waittime + 1
            print(waittime)

        if stein_jetzt == "False":
            stein_gesamt = stein_gesamt + 1
            stein_jetzt = "nichts"

        if stein_jetzt == "True":
            stein_gesamt = stein_gesamt + 1
            stein_gefunden = stein_gefunden + 1
            stein_jetzt = "nichts"
            dashbordsteineanzeige[programmnummer] = dashbordsteineanzeige[programmnummer] + 1


        if stein_gesamt > 0:
            stein_prozent = stein_gefunden / stein_gesamt * 100

        # print("Gesamt: " + str(stein_gesamt) + "\nGefunden: " + str(stein_gefunden) + "\nin %:" + str(stein_prozent))

        # print (str(stein_jetzt)+ " STEIN JETZT")



    dashboard(dashbordsteineanzeige, img)

    if cv2.waitKey(1) & 0xFF == ord(' ') or cv2.waitKey(5) & 0xFF == 27:  # Stop if spacebar is detected
        break
camera.release()  # Cleanup after spacebar is detected.
cv2.destroyAllWindows()
