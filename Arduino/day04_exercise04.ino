#include "DHT.h"
#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

#define LAMP 17
#define PUMP 16
#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6
SOFTPWM_DEFINE_CHANNEL(A3);

DHT dht(DHTPIN, DHTTYPE);

uint32_t DataCaptureDelay = 2000;
uint32_t DataCapture_ST = 0;
int Soilhumi = 0;
float Temp;
float Humi;

int Hour=0;
int Minute=1;

bool autoB_out_status;
bool lampT_out_status;

bool fan_out_status;
bool pump_out_status;
bool lamp_out_status;

bool timeset = false;
bool Interval_Hup_status;
bool Interval_Mup_status;

void autoB_out(bool val)
{
    autoB_out_status = val;
}
void timeset_out(bool val) {
    timeset = val;
}

void fan_out(bool val)
{
    fan_out_status = val;
}
void pump_out(bool val)
{
    pump_out_status = val;
}
void lamp_out(bool val)
{
    lamp_out_status = val;
}

void Interval_Hup(bool val) {
    Interval_Hup_status = val;
}
void Interval_Mup(bool val) {
    Interval_Mup_status = val;
}

void IntervalReset(bool val) {
    if (!timeset && val)
    {
        Hour = 0;
        Minute = 0;
    }
}

IOTItemBin autoBStatus;
IOTItemBin autoB(autoB_out);
IOTItemBin lampTStatus;
IOTItemBin lampT(timeset_out);

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);
IOTItemBin LampStatus;
IOTItemBin Lamp(lamp_out);

IOTItemBin IntervalHUP(Interval_Hup);
IOTItemBin IntervalMUP(Interval_Mup);
IOTItemBin IntervalRST(IntervalReset);
IOTItemInt label_Hinterval;
IOTItemInt label_Minterval;

IOTItemFlo dht22_temp;
IOTItemFlo dht22_humi;
IOTItemInt soilhumi;

#define ITEM_COUNT 18

IOTItem *items[ITEM_COUNT] = {&autoBStatus, &autoB, &lampTStatus, &lampT,
                              &FanStatus, &Fan, &PumpStatus, &Pump, &LampStatus, &Lamp,
                              &IntervalHUP, &IntervalMUP, &IntervalRST,
                              &label_Hinterval, &label_Minterval,
                              &dht22_temp, &dht22_humi, &soilhumi};

const char device_id[] = "d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup()
{
    Serial.begin(250000);
    comm.SetInterval(200);

    dht.begin();
    SoftPWM.begin(490);
    pinMode(LAMP, OUTPUT);
    pinMode(PUMP, OUTPUT);
    pinMode(SOILHUMI, INPUT);

    DataCapture_ST = millis();
}

void loop()
{
    Soilhumi = map(analogRead(SOILHUMI), 0, 1023, 100, 0);
    Humi = dht.readHumidity();
    Temp = dht.readTemperature();

    if (fan_out_status == true)
        SoftPWM.set(100);
    else
        SoftPWM.set(0);
    digitalWrite(PUMP, pump_out_status);
    digitalWrite(LAMP, lamp_out_status);

    //모듈링크 값을 위젯으로 보내줌
    //없으면 위젯값을 모듈링크에 읽기만 하고
    dht22_temp.Set(Temp);
    dht22_humi.Set(Humi);
    soilhumi.Set(Soilhumi);
    FanStatus.Set(fan_out_status);
    PumpStatus.Set(digitalRead(PUMP));
    LampStatus.Set(digitalRead(LAMP));
    
    comm.Run();
}