#include <VitconBrokerComm.h>
#include <SoftPWM.h>
#include "DHT.h"
using namespace vitcon;

#define DHTPIN A1
#define DHTTYPE DHT22
#define PUMP 16
#define SOILHUMI A6

DHT dht(DHTPIN, DHTTYPE);
SOFTPWM_DEFINE_CHANNEL(A3);

int Soilhumi = 0;
float Temp;

bool fan_out_status;
bool pump_out_status;

void fan_out(bool var)
{
    fan_out_status = var;
}

void pump_out(bool var)
{
    pump_out_status = var;
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);

#define ITEM_COUNT 4

IOTItem *items[ITEM_COUNT] = {&FanStatus, &Fan, &PumpStatus, &Pump};

const char device_id[] = "d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup()
{
    Serial.begin(250000);
    comm.SetInterval(200);

    dht.begin();
    SoftPWM.begin(490);
    pinMode(PUMP, OUTPUT);
    pinMode(SOILHUMI, INPUT);
}

void loop()
{
    Temp = dht.readTemperature();
    Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);

    if(isnan(Temp) || isnan(Soilhumi)){
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }

    if (fan_out_status == true) {
        if(Temp >= 29) {
            SoftPWM.set(100);
        }
        else if(Temp <= 20) {
            SoftPWM.set(0);
        }
        else { // 20 < Temp < 29
            SoftPWM.set(65);
        }
    }
    else {
        SoftPWM.set(0);
    }

    if (pump_out_status == true) {
        if (Soilhumi >= 30 && Soilhumi <= 60) {
            digitalWrite(PUMP, HIGH);
        }
        else {
            digitalWrite(PUMP, LOW);
        }
    }
    else {
        digitalWrite(PUMP, LOW);
    }

    FanStatus.Set(fan_out_status);
    PumpStatus.Set(digitalRead(PUMP));
    comm.Run();
}