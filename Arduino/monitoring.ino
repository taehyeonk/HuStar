#include "DHT.h"
#include<VitconBrokerComm.h>
using namespace vitcon;

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6

DHT dht(DHTPIN, DHTTYPE);

uint32_t DataCaptureDelay=2000;
uint32_t DataCapture_ST=0;
int Soilhumi=0;
float Temp;
float Humi;

IOTItemFlo dht22_temp;
IOTItemFlo dht22_humi;
IOTItemInt soilhumi;


#define ITEM_COUNT 3

IOTItem *items[ITEM_COUNT]={&dht22_temp, &dht22_humi, &soilhumi};

const char device_id[]="d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm (&Serial, device_id, items, ITEM_COUNT);




void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  comm.SetInterval(200);

  dht.begin();
  pinMode(SOILHUMI, INPUT);
  DataCapture_ST=millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  Soilhumi=map(analogRead(SOILHUMI),0,1023,100,0);

  if(millis()-DataCapture_ST>DataCaptureDelay){
    Humi=dht.readHumidity();
    Temp=dht.readTemperature();
    DataCapture_ST=millis();
  }

  dht22_temp.Set(Temp);
  dht22_humi.Set(Humi);
  soilhumi.Set(Soilhumi);
  comm.Run();
}