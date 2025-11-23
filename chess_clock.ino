#include "SevSegShift.h"
SevSeg sevseg;

// timers (seconds)
int play_time = 301;
int play_time_1 = play_time;
int play_time_2 = play_time;

const int buttonA = A0;
const int buttonB = A1;

int ledA = A3;
int ledB = A4;

int ledPlayer1;
int ledPlayer2;

int buttonPlayer1;
int buttonPlayer2;
bool playersAssigned = false;

int activePlayer = 2;
unsigned long previousMillis = 0;
const unsigned long interval = 1000;

void setup() {
  byte numDigits = 4;
  byte digitPins[] = {2, 5, 6, 13};
  byte segmentPins[] = {3, 7, 11, 9, 8, 4, 12, 10};

  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, true,
               false, true, false);
  sevseg.setBrightness(90);

  Serial.begin(9600);
  pinMode(buttonA, INPUT_PULLUP);
  pinMode(buttonB, INPUT_PULLUP);
}

void loop() {

  if (!playersAssigned) {
    if (digitalRead(buttonA) == LOW) {
      buttonPlayer1 = buttonA;
      ledPlayer1 = ledA;
      buttonPlayer2 = buttonB;
      ledPlayer2 = ledB;
      playersAssigned = true;
      activePlayer = 2;
      delay(300);
    }
    else if (digitalRead(buttonB) == LOW) {
      buttonPlayer1 = buttonB;
      ledPlayer1 = ledB;
      buttonPlayer2 = buttonA;
      ledPlayer2 = ledA;
      playersAssigned = true;
      activePlayer = 2;
      delay(300);
    }

    sevseg.setNumber(9999, 0);
    sevseg.refreshDisplay();
    return;
  }


  if (digitalRead(buttonPlayer1) == LOW) {
    activePlayer = 2;
  }

  if (digitalRead(buttonPlayer2) == LOW) {
    activePlayer = 1;
  }


  unsigned long currentMillis = millis();


  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (activePlayer == 1 && play_time_1 > 0) play_time_1--;
    if (activePlayer == 2 && play_time_2 > 0) play_time_2--;
  }


  int t = (activePlayer == 1) ? play_time_1 : play_time_2;
  int minutes = t / 60;
  int seconds = t % 60;

  sevseg.setNumber(minutes * 100 + seconds, 2);
  sevseg.refreshDisplay();

  if (play_time_1 == 0 || play_time_2 == 0) {
    if (play_time_1 == 0){
      digitalWrite(ledPlayer1, HIGH);
    } else{
      digitalWrite(ledPlayer2, HIGH);
    }
      sevseg.refreshDisplay();
      while (true);
  }
}




