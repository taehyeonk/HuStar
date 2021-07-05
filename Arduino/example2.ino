#include <VitconBrokerComm.h>
using namespace vitcon;
#include <SoftPWM.h>

#define LAMP 17
#define PUMP 16
SOFTPWM_DEFINE_CHANNEL(A3);

bool fan_out_status;
bool pump_out_status;
bool lamp_out_status;

void fan_out(bool var)
{
    fan_out_status = var;
}

void pump_out(bool var)
{
    pump_out_status = var;
}

void lamp_out(bool var)
{
    lamp_out_status = var;
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);
IOTItemBin LampStatus;
IOTItemBin Lamp(lamp_out);

#define ITEM_COUNT 6

IOTItem *items[ITEM_COUNT] = {&PumpStatus, &Pump,
                              &LampStatus, &Lamp,
                              &FanStatus, &Fan};

const char device_id[] = "d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(250000);
    comm.SetInterval(200);

    SoftPWM.begin(490);
    pinMode(LAMP, OUTPUT);
    pinMode(PUMP, OUTPUT);
}

void loop()
{
    if (fan_out_status == true) SoftPWM.set(100);
    else SoftPWM.set(0);
    digitalWrite(PUMP, pump_out_status);
    digitalWrite(LAMP, pump_out_status);

    FanStatus.Set(fan_out_status);
    LampStatus.Set(digitalRead(LAMP));
    PumpStatus.Set(digitalRead(PUMP));
    comm.Run();
}