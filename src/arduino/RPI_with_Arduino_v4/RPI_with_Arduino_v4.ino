#include <Servo.h>
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
int waterinlet = 24;
int wateroutlet = 25;
int picam = 26;
bool taskdone = true;

void setup() {
  Serial.begin(9600);
  pinMode (waterin, OUTPUT); //consider adding real inlet?
  pinMode (waterout, OUTPUT); //consider adding real outlet?
  pinMode (ultrasonic, OUTPUT);
  pinMode (waterpump, OUTPUT);
  pinMode (fan, OUTPUT);
  pinMode (uv, OUTPUT);
  pinMode (DFsensor, INPUT);
  pinMode (Topsensor, INPUT);
  pinMode (waterpump1, OUTPUT);
  pinMode (waterinlet, OUTPUT);
  pinMode (wateroutlet, OUTPUT);
  pinMode (picam, OUTPUT);
  Servo1.attach(ServoPin); 
}

void loop(){
  Servo1.write(180); //bring syringes up

  
  if (Serial.available() > 0){
    int inByte = Serial.read()-'0';
    switch (inByte){
      case 1:
      digitalWrite(picam, LOW);
      washing();
      rinsing();
      digitalWrite(picam, HIGH);
      Serial.println(taskdone, BIN);
      break;

      case 2:
      digitalWrite(picam, LOW);
      drying();
      Serial.println(taskdone, BIN);
      digitalWrite(picam, HIGH);
      break;

      case 3:
      digitalWrite(picam, LOW);
      sterilising();
      Serial.println(taskdone, BIN);
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
      digitalWrite (waterinlet, LOW);
      digitalWrite (wateroutlet, LOW);
      digitalWrite(picam, LOW);
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
        digitalWrite (waterinlet, HIGH);
        Serial.println("Water inlet ON");
        int Toplevel = digitalRead(Topsensor);

        if (Toplevel == LOW){
          digitalWrite(waterin, LOW); //water inlet OFF
          digitalWrite (waterinlet, LOW);
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
        digitalWrite (wateroutlet, HIGH);
        Serial.println("Water outlet ON");
        int DFlevel = digitalRead(DFsensor);

        if (DFlevel == LOW){
          digitalWrite(waterout, LOW);//water outlet OFF
          digitalWrite (wateroutlet, HIGH);
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
      digitalWrite(fan, LOW);
      Serial.println("Fans OFF");
      Serial.println("Drying Process Completed");  
}

void sterilising(){
  Serial.println("Sterilising Process Start");
  digitalWrite(uv, HIGH);
  Serial.println("UV ON");
  delay(10000); //recommended sterilising time, 15 mins
  digitalWrite(uv, LOW);
  Serial.println("UV OFF");
  Serial.println("Sterilising Process Completed");   
}

void rinsing(){// Rinsing Function                         
      int DFlevel = digitalRead(DFsensor);
      int Toplevel = digitalRead (Topsensor);
      Serial.println("Rinsing Process Start");
      delay(5000);
      
      while (Toplevel == HIGH){
        digitalWrite(waterin, HIGH); //water inlet ON
        digitalWrite (waterinlet, HIGH);
        Serial.println("Water inlet ON");
        int Toplevel = digitalRead(Topsensor);

        if (Toplevel == LOW){
          digitalWrite(waterin, LOW); //water inlet OFF
          digitalWrite (waterinlet, LOW);
          Serial.println("Water inlet OFF");
          Serial.println("Moving Syringes");
          delay(1000);
          Servo1.write(135); //bring syringes up
          delay(1000);          
          Servo1.write(90); //bring syringes down
          delay(1000);
          Servo1.write(135); //bring syringes up
          delay(1000);          
          Servo1.write(180); //bring syringes down          
          break;                   
        }
      }
      
      while (DFlevel == HIGH){
        digitalWrite (waterout, HIGH);//water outlet ON
        digitalWrite (wateroutlet, HIGH);
        Serial.println(DFlevel); //print 1 when still detecting water
        int DFlevel = digitalRead(DFsensor);

        if (DFlevel == LOW){
          digitalWrite(waterout, LOW);//water outlet OFF
          digitalWrite (wateroutlet, HIGH);          
          Servo1.write(180); //bring syringes up
          Serial.println("Rinsing Process Completed");
          break;
          }        
      }    
}


      
