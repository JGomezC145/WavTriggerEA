#include <Wire.h>
#include <Adafruit_RGBLCDShield.h>
#include <utility/Adafruit_MCP23017.h>
#include <Keypad.h>
#include <Metro.h>
#include <wavTrigger.h>
#include <string.h>
#include <AltSoftSerial.h>

#define LIGHT 0x7
#define LED 13

int sonido;

Adafruit_RGBLCDShield lcd = Adafruit_RGBLCDShield();
int boton;
int dato;

bool updS = false;  //actualiza toda la lcd
bool updP = false;  // actualiza la pista en lcd

wavTrigger wav;

Metro gLedMetro(500);   // LED blink interval timer
Metro gSeqMetro(6000);  // Sequencer state machine interval timer

byte gLedState = 0;   // LED State
int gSeqState = 0;    // Main program sequencer state
int gRateOffset = 0;  // WAV Trigger sample-rate offset
int gNumTracks;
int currentTrack = 0;
String currentDig = "";


/* 
Usar el puerto serial para comunicarse con el wav trigger. Si se usa Arduino Mega, se usa Serial1.
Si se usa Arduino Uno, se usa AltSoftSerial. Cambiar la linea 37 por #define wav altSerial en la libreria wavTrigger.h
Si se usa Arduino Mega, se usa Serial1. Cambiar la linea 38 por #define wav Serial1 en la libreria wavTrigger.h 
*/
//AltSoftSerial altSerial(10, 11); // RX, TX

char gWTrigVersion[VERSION_STRING_LEN];
String banco = "0";
String lastbanco = "0";

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setCursor(1, 0);
  lcd.print("Wav");
  lcd.setCursor(3, 1);
  lcd.print("Trigger EA");
  lcd.setBacklight(LIGHT);
  delay(3000);
  lcd.clear();
  lcd.print("Starting");
  pinMode(LED, OUTPUT);
  digitalWrite(LED, gLedState);

  delay(1000);

  wav.start();
  delay(100);

  wav.stopAllTracks();
  wav.samplerateOffset(0);

  wav.setReporting(true);



  delay(100);
  if (wav.getVersion(gWTrigVersion, VERSION_STRING_LEN)) {
    gLedState = 1;
    digitalWrite(LED, gLedState);
    Serial.println("version obtenida");
  } else {
    digitalWrite(LED, !gLedState);
    Serial.println("version no obtenida");
  }
  delay(1000);
  // Set loop tracks


  Serial.print("Numero de canciones: ");
  Serial.println(wav.getNumTracks());
  // get number of songs
  // print songs in lcd
  lcd.clear();
  lcd.print("Listo");
  delay(750);
  lcd.clear();
  lcd.print("Banco: " + String(banco));
}

void loop() {
  uint8_t buttons = lcd.readButtons();

  if (buttons) {
    if (buttons & BUTTON_UP) {
      if (banco.toInt() < 2) {
        banco = String(banco.toInt() + 1);
      }
      lcd.clear();
      lcd.print("Banco: " + String(banco));
      delay(750);
    }
    if (buttons & BUTTON_DOWN) {
      if (banco.toInt() > 0) {
        banco = String(banco.toInt() - 1);
      }
      lcd.clear();
      lcd.print("Banco: " + String(banco));
      delay(750);
    }
    if (buttons & BUTTON_SELECT) {
      wav.stopAllTracks();
    }
    if (buttons & BUTTON_LEFT) {
      wav.trackPause(sonido);
    }
    if (buttons & BUTTON_RIGHT) {
      wav.trackResume(sonido);
    }

  }





  lcd.setBacklight(LIGHT);
  
  
  dato = analogRead(A0);

  if (dato >= 95 && dato <= 105 ) { boton = 1; }
  if (dato >= 108 && dato <= 112) { boton = 2; }
  if (dato >= 123 && dato <= 128) { boton = 3; }
  if (dato >= 140 && dato <= 145) { boton = 4; }
  if (dato >= 165 && dato <= 170) { boton = 5; }
  if (dato >= 198 && dato <= 205) { boton = 6; }
  if (dato >= 249 && dato <= 256) { boton = 7; }
  if (dato >= 335 && dato <= 342) { boton = 8; }
  if (dato >= 505 && dato <= 512) { boton = 9; }

  
  if (boton && boton != 9) {
    sonido = banco.toInt() * 8 + boton;
    if (sonido == 1) {
      wav.trackLoop(1, 1);
    }
    if (sonido == 15) {
      wav.trackLoop(15, 1);
    }
    if (sonido == 16) {
      wav.trackLoop(16, 1);
    }

    if (sonido == 17) {
      wav.trackPlayPoly(17);
    } else {
      wav.trackPlaySolo(sonido);
    }
    delay(500);
    lcd.setCursor(0, 1);
    lcd.print("            ");
    lcd.setCursor(0, 1);
    lcd.print("Reprod: " + String(sonido));
    //return;
  }
  if (boton == 9) {
    wav.stopAllTracks();
    //wav.trackFade(sonido, -40, 3000, true);
    lcd.setCursor(0, 1);
    lcd.print("            ");
    lcd.setCursor(0, 1);
    lcd.print("Detenido");
  }

  if (boton != NULL) {
    boton = NULL;
  }
}

/**
 * @brief Imprime mensaje en la primera linea del LCD
 * 
 * @param msg Mensaje a imprimir
 */
void lclewr(String msg) {
  if (!updS) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(msg);
    updS = !updS;
    updP = !updP;
  }
}

// imprime mensaje (usualmente numero), en la segunda linea
void lcinpnum(String num) {
  updS = false;
  if (!updP) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pista:");
    lcd.setCursor(0, 1);
    lcd.print(num);
    updP = !updP;
  } else {
    lcd.setCursor(0, 1);
    lcd.print(num);
  }
}
