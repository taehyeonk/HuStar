#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

SOFTPWM_DEFINE_CHANNEL(A3);

bool fan_out_status = false;
int32_t PWM = 60;

void fan_out(bool var) {
    fan_out_status = var;
}
void fan_pwm_out(int32_t var) {
    PWM = var;
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemInt FanPwmValue;
IOTItemInt FanPwm(fan_pwm_out);

#define ITEM_COUNT 4

IOTItem *items[ITEM_COUNT] = {&FanStatus, &Fan, &FanPwmValue, &FanPwm};

const char device_id[] = "d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup()
{
    Serial.begin(250000);
    comm.SetInterval(200);

    FanPwmValue.Set(PWM);
    SoftPWM.begin(490);
}

void loop()
{
    if (fan_out_status == true) {
        SoftPWM.set(PWM);
    }
    else {
        SoftPWM.set(0);
    }

    FanStatus.Set(fan_out_status);
    FanPwmValue.Set(PWM);
    comm.Run();
}