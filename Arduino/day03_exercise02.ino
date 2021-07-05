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

#include <SoftPWM.h>

#define LAMP 17
#define PUMP 16
SOFTPWM_DEFINE_CHANNEL(A3);


bool fan_out_status;
bool pump_out_status;
bool lamp_out_status;

void fan_out(bool val){//위젯으로부터 값을 받아옴
  fan_out_status=val;
}

void pump_out(bool val){
  pump_out_status=val;
}

void lamp_out(bool val){
  lamp_out_status=val;
}

//모듈 링크의 값을 위젯이랑 동기화
IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);

IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);

IOTItemBin LampStatus;
IOTItemBin Lamp(lamp_out);


#define ITEM_COUNT 9

IOTItem *items[ITEM_COUNT]={&dht22_temp, &dht22_humi, &soilhumi,
                            &FanStatus, &Fan,
                            &PumpStatus, &Pump,
                            &LampStatus, &Lamp                                     
};

const char device_id[]="f478244e22aa411a6aebc69f5294e85a";
BrokerComm comm (&Serial, device_id, items, ITEM_COUNT);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  comm.SetInterval(200);

  SoftPWM.begin(490);
  pinMode(LAMP,OUTPUT);
  pinMode(PUMP,OUTPUT);
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

  if(fan_out_status==true) SoftPWM.set(100);
  else SoftPWM.set(0);
  digitalWrite(PUMP, pump_out_status);
  digitalWrite(LAMP, lamp_out_status);


  //모듈링크 값을 위젯으로 보내줌
  //없으면 위젯값을 모듈링크에 읽기만 하고
  FanStatus.Set(fan_out_status);
  LampStatus.Set(digitalRead(LAMP));
  PumpStatus.Set(digitalRead(PUMP));
  //comm.Run();

  dht22_temp.Set(Temp);
  dht22_humi.Set(Humi);
  soilhumi.Set(Soilhumi);
  comm.Run();
}