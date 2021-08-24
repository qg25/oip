#include <Servo.h>
#include "DHT.h"
#define DHTPIN 13     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht (DHTPIN, DHTTYPE);
Servo Servo1;

// Declarations
int ServoPin = 2;
int waterin = 3;
int waterout = 4;
int ultrasonic = 5;
int waterpump = 6;
int fan = 7;
int uv = 8;
int Topsensor = 9;
int DFsensor = 22; 


void setup() {
  // put your setup code here, to run once (need to include all the componets used here):
  Serial.begin(9600);
  while (!Serial){
    ; // Wait for serial port to connect.
  }
  dht.begin();
  pinMode (waterin, OUTPUT);
  pinMode (waterout, OUTPUT);
  pinMode (ultrasonic, OUTPUT);
  pinMode (waterpump, OUTPUT);
  pinMode (fan, OUTPUT);
  pinMode (uv, OUTPUT);
  pinMode (DFsensor, INPUT);
  pinMode (Topsensor, INPUT);
  Servo1.attach(ServoPin); 
}

void loop() {
  // put your main code here, to run repeatedly
  int DFlevel = digitalRead(DFsensor);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float hic = dht.computeHeatIndex(t, h, false);
  Servo1.write(0); //bring syringes up

  
  if (Serial.available() > 0){
    int inByte = Serial.read() - '0';
    switch (inByte){
      case 1: // RPI "FULL CYCLE pressed"
        washing();
        drying();
        Serial.println("done");
        break;

      case 2:
        drying()
        Serial.println("done");
        break;
      
      default:
        Serial.print(F(" Humidity: "));
        Serial.print(h);
        Serial.println("%");
        Serial.print(F("Temperature: "));
        Serial.print(t);
        Serial.println(F("C "));
        break;
      //do nothing and all componenets are offed
    }
  }
}

void washing(){
      int DFlevel = digitalRead(DFsensor);
      int Toplevel = digitalRead (Topsensor);
      Serial.println("Washing Process Start");
      delay(5000);
      Servo1.write(90); //bring syringes down 
      
      while (Toplevel == HIGH){
        digitalWrite(waterin, HIGH); //water inlet ON
        Serial.println("Water inlet ON");
        int Toplevel = digitalRead(Topsensor);

        if (Toplevel == LOW){
          digitalWrite(waterin, LOW); //water inlet OFF
          Serial.println("Water inlet OFF");
          digitalWrite(ultrasonic, HIGH); // ultra-sonic wash ON
          digitalWrite(waterpump, HIGH); //water pump ON
          Serial.println("Ultrasonic and Waterpump ON");
          delay(10000); // ultra-sonic wash ON for __s
          digitalWrite(ultrasonic, LOW); //ultra-sonic wash OFF
          digitalWrite(waterpump, LOW); //water pump OFF
          Serial.println("Ultrasonic and Waterpump OFF");
          break;                   
        }
      }
      
      while (DFlevel == HIGH){
        digitalWrite (waterout, HIGH);//water outlet ON
        Serial.println(DFlevel); //print 1 when still detecting water
        int DFlevel = digitalRead(DFsensor);

        if (DFlevel == LOW){
          digitalWrite(waterout, LOW);//water outlet OFF
          Servo1.write(0); //bring syringes up
          Serial.println("Washing Process Completed");
          break;
          }        
      }  
}

void drying(){
      Serial.println("Drying Process Start");
      delay(5000);
      digitalWrite(fan, HIGH);
      Serial.println("Fans ON");
      delay(10000);
      digitalWrite(uv, HIGH);
      Serial.println("UV ON");
      delay(5000);
      digitalWrite(fan, LOW);
      digitalWrite(uv, LOW);
      Serial.println("Fans and UV OFF");
      Serial.println("Drying Process Completed");  
}
