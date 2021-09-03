#include <Servo.h>
#include "DHT.h"
#define DHTPIN 13     
#define DHTTYPE DHT11
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
int waterpump1 = 23;


void setup() {
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
  pinMode (waterpump1, OUTPUT);
  Servo1.attach(ServoPin); 
}

void loop() {
  int DFlevel = digitalRead(DFsensor);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float hic = dht.computeHeatIndex(t, h, false);
  Servo1.write(0); //bring syringes up
  Serial.print(F(" Humidity: "));
  Serial.print(h);
  Serial.println("%");
  Serial.print(F("Temperature: "));
  Serial.print(t);
  Serial.println(F("C "));
  delay(60000); // Sending temperature and humidity to RPI every 60s

  
  if (Serial.available() > 0){
    int inByte = Serial.read() - '0';
    switch (inByte){
      case 1: // RPI "FULL CYCLE pressed - need to decide how ML comes in for each function"
        washing();
        rinsing();
        drying();
        Serial.println("done");
        break;

      case 2:
        drying();
        Serial.println("done");
        break;

      
      default://OFF all components
        digitalWrite (waterin, LOW);
        digitalWrite (waterout, LOW);
        digitalWrite (ultrasonic, LOW);
        digitalWrite (waterpump, LOW);
        digitalWrite (fan, LOW);
        digitalWrite (uv, LOW);
        digitalWrite (DFsensor, LOW);
        digitalWrite (Topsensor, LOW);
        digitalWrite (waterpump1, LOW);
        break;
    }
  }
}

void washing(){// Washing Function
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
          digitalWrite(waterpump1, HIGH); //water pump1 ON
          Serial.println("Ultrasonic and Waterpump ON");
          delay(10000); // ultra-sonic wash ON for __s
          digitalWrite(ultrasonic, LOW); //ultra-sonic wash OFF
          digitalWrite(waterpump, LOW); //water pump OFF
          digitalWrite(waterpump1, LOW); //water pump1 OFF

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
          Serial.println("Rinsing Process Completed");
          break;
          }        
      }  
}

void drying(){// Drying Function
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

void rinsing(){// Rinsing Function                         
      int DFlevel = digitalRead(DFsensor);
      int Toplevel = digitalRead (Topsensor);
      Serial.println("Rinsing Process Start");
      delay(5000);
      
      while (Toplevel == HIGH){
        digitalWrite(waterin, HIGH); //water inlet ON
        Serial.println("Water inlet ON");
        int Toplevel = digitalRead(Topsensor);

        if (Toplevel == LOW){
          digitalWrite(waterin, LOW); //water inlet OFF
          Serial.println("Water inlet OFF");
          Serial.println("Moving Syringes");
          delay(1000);
          Servo1.write(45); //bring syringes up
          delay(1000);          
          Servo1.write(90); //bring syringes down
          delay(1000);
          Servo1.write(45); //bring syringes up
          delay(1000);          
          Servo1.write(0); //bring syringes down          
          break;                   
        }
      }
      
      while (DFlevel == HIGH){
        digitalWrite (waterout, HIGH);//water outlet ON
        Serial.println(DFlevel); //print 1 when still detecting water
        int DFlevel = digitalRead(DFsensor);

        if (DFlevel == LOW){
          digitalWrite(waterout,+ LOW);//water outlet OFF
          Servo1.write(0); //bring syringes up
          Serial.println("Rinsing Process Completed");
          break;
          }        
      }    
}
