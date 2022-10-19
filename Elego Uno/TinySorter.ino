#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <Servo.h> //Die Servobibliothek wird aufgerufen. Sie wird benötigt, damit die Ansteuerung des Servos vereinfacht wird.




Servo servoblau; //Erstellt fuer das Programm ein Servo mit dem Namen „servoblau“


// Pinbelegung Definieren
int AbfrageTasterStartGedrueckt = 0;
int AbfrageTasterAusGedrueckt = 0;
int LedRotPin = 9;
int LedGruenPin = 10;
int LedEinPin = 3;
int TasterStartPin = 4;
int TasterAusPin = 5;
int TasterSortierenHoch = 6;
int TasterSortierenRunter = 7;
int i = 0;
int programnummer = 0;



int zaehlerLinks = 0;
int zaehlerRechts = 0;



int zeit = 500;
int serialReadWert = 0;



// OLED display TWI address
#define OLED_ADDR 0x3C



Adafruit_SSD1306 display(-1);



#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif



void setup() {

  // Pinmode festlegen
  servoblau.attach(8); //Das Setup enthält die Information, dass das Servo an der Steuerleitung (gelb) mit Pin 8 verbunden wird. Hier ist natuerlich auch ein anderer Pin möglich.
  pinMode (LedRotPin, OUTPUT);
  pinMode (LedGruenPin, OUTPUT);
  pinMode (LedEinPin, OUTPUT);
  pinMode (TasterStartPin, INPUT_PULLUP);
  pinMode (TasterAusPin, INPUT_PULLUP);
  pinMode (TasterSortierenHoch, INPUT_PULLUP);
  pinMode (TasterSortierenRunter, INPUT_PULLUP);
  
    
  // Lampen initial ausschalten
  digitalWrite(LedRotPin, LOW);
  digitalWrite(LedGruenPin, LOW);
  digitalWrite(LedEinPin, LOW);
  
  // initialize and clear display
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
  display.display();


  
  // display Schrift Festlegen
  display.setTextSize(1);
  display.setTextColor(WHITE);
  displayaktualisieren();
  

  // Serialle Kommunikation einschalten
  Serial.begin(115200);
  Serial.setTimeout(1);
}




void loop()
{
  grundstellung();
  //Abfrage TasterStart gedrueckt
  if(digitalRead(TasterStartPin) == LOW && programnummer != 0)
  {
    Serial.print(programnummer);
    AbfrageTasterStartGedrueckt = 1;
    digitalWrite(LedEinPin, HIGH);
    cleanserialbuffer();
    lampenblinken();
    grundstellung();
    zaehlerLinks = 0;
    zaehlerRechts = 0;
    displayaktualisieren();
  }
  
  
  // Programnummer Umschalten
  if(digitalRead(TasterSortierenHoch) == LOW && programnummer < 6)
  {
    //Serial.print(1);
    programnummer = programnummer + 1;
    displayaktualisieren();
    delay(20);
    while(digitalRead(TasterSortierenHoch) == LOW);
    delay(20);
  }
  else if(digitalRead(TasterSortierenRunter) == LOW && programnummer > 1)
  {
    //Serial.print(2);
    programnummer = programnummer - 1;
    displayaktualisieren();
    delay(20);
    while(digitalRead(TasterSortierenRunter) == LOW);
    delay(20);
  }
  
  
  
  // Loop Program Gestartet
  while(AbfrageTasterStartGedrueckt == 1)
  {
    serialReadWert = Serial.readString().toInt();
    
    
    
    //Abfrage TasterAus gedrueckt
    if(digitalRead(TasterAusPin) == LOW)
    {
      AbfrageTasterAusGedrueckt = 1;
      AbfrageTasterStartGedrueckt = 0;
      Serial.print(0);
      lampenblinken();
      digitalWrite(LedEinPin, LOW);
    }
    else if(digitalRead(TasterSortierenHoch) == LOW || serialReadWert == 1) // Sortiernen Rechts
    {
      sortierenRechts();
      serialReadWert = 0;
    }
     else if(digitalRead(TasterSortierenRunter) == LOW || serialReadWert == 2) // Sortieren Links
    {
      sortierenLinks();
      serialReadWert = 0;
    }
  }
}



//Funktion Sortieren Rechts
void sortierenRechts()
{
    servoblau.write(103); //Position 2
    digitalWrite(LedRotPin, HIGH);
    delay(zeit); //Das Programm stoppt fuer x Sekunden Damit der motor sich auf position bewegen kann und der stein rausfallen kann
    grundstellung();
    
    // Zahl Links Hochzählen
    zaehlerLinks++;
    displayaktualisieren();
}



//Funktion Sortieren Links
void sortierenLinks()
{
  digitalWrite(LedGruenPin, HIGH);
  servoblau.write(72); //Position 2
  delay(zeit); //Das Programm stoppt fuer x Sekunden Damit der motor sich auf position bewegen kann und der stein rausfallen kann
  grundstellung();
  
  // Zahl Rechts Hochzählen
  zaehlerRechts++;
  displayaktualisieren();
}



//Funktion Grundstelleng
void grundstellung()
{
  digitalWrite(LedRotPin, LOW);
  digitalWrite(LedGruenPin, LOW);
  servoblau.write(87); //Position 3
}


// Lampen beim ein aus schalten Blincken lassen
void lampenblinken()
{
  for (i=0; i < 5 ; i++)
  {
    digitalWrite(LedRotPin, HIGH);
    digitalWrite(LedGruenPin, HIGH);
    delay(100);
    digitalWrite(LedRotPin, LOW);
    digitalWrite(LedGruenPin, LOW);
    delay(100);
  }
}



// Serial buffer Clearen
void cleanserialbuffer()
{
  while (Serial.available())
  {
    Serial.read();
  }
}



// Display aufbauen
void displayaktualisieren()
{
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(27,15);
  switch (programnummer) {
    case 0:
      display.print("Programm waelen");
      break;
    case 1:
      display.print("Gelb 2x4");
      break;
    case 2:
      display.print("Gelb 2x2");
      break;
    case 3:
      display.print("Blau 2x4");
      break;
    case 4:
      display.print("Blau 2x2");
      break;
    case 5:
      display.print("Rot 2x4");
      break;
    case 6:
      display.print("Rot 2x2");
      break;
  }
  display.setCursor(27,40);
  display.print(zaehlerRechts); 
  display.setCursor(90,40);
  display.print(zaehlerLinks);
  display.display();
}
