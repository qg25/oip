#include <dht11.h>
dht11 DHT;
#define DHT11_PIN 4
bool JobDone = true;

void setup(){
  Serial.begin(9600);
  while (!Serial){
    ; // Wait for serial port to connect.
  }
  Serial.println("DHT TEST PROGRAM ");
  Serial.print("LIBRARY VERSION: ");
  Serial.println(DHT11LIB_VERSION);
  Serial.println();
  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
  
}

void loop(){
  if(Serial.available() > 0){
    int data = Serial.read() - '0';
    bool isDone = false;
    int counter = 1;
    Serial.print("Data: ");
    Serial.println(data);
    switch (data) {
      case 1:
        while(!isDone){
          Serial.print("Out Counter: ");
          Serial.println(counter);
          isDone = readHumidity(&counter);
        }
        break;
      case 2:
        Serial.println("do 2");
        delay(1000);
        Serial.println(JobDone, BIN);
        break;

      default:
        Serial.println("false");
        break;
    }
 }
}

bool readHumidity(int *count){
  int chk;
  Serial.print("DHT11, \t");
  chk = DHT.read(DHT11_PIN);    // READ DATA
  switch (chk){
    case DHTLIB_OK:
      Serial.print("OK,\t");
      break;
    case DHTLIB_ERROR_CHECKSUM:
      Serial.print("Checksum error,\t");
      break;
    case DHTLIB_ERROR_TIMEOUT:
      Serial.print("Time out error,\t");
      break;
    default:
      Serial.print("Unknown error,\t");
      break;
  }
  // DISPLAY DATA
  Serial.print("Counter: ");
  Serial.println(*count);
  Serial.print(DHT.humidity,1);
  Serial.print(",\t");
  Serial.println(DHT.temperature,1);
  *count += 1;
  delay(2000);
  if (*count == 3) {
    Serial.println(JobDone, BIN);
    return JobDone;
  }
  return !JobDone;
}
