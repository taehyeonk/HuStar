#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

SOFTPWM_DEFINE_CHANNEL(A3);

bool fan_out_status;
bool timeset = false;
bool Interval_Mup_status;
bool Interval_Sup_status;


int Minute = 0;
int Seconds = 1;
int32_t PWM = 60;
uint32_t TimeSum = 0;
uint32_t TimeCompare;

uint32_t TimePushDelay = 0;
uint32_t TimerStartTime = 0;

void fan_pwm_out(int32_t var) {
    PWM = var;
}

void fan_out(bool var) {
    fan_out_status = var;
}

void timeset_out(bool val) {
    timeset = val;
}

void Interval_Mup(bool val) {
    Interval_Mup_status = val;
}
void Interval_Sup(bool val) {
    Interval_Sup_status = val;
}

void IntervalReset(bool val) {
    if (!timeset && val)
    {
        Minute = 0;
        Seconds = 0;
    }
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemInt FanPwmValue;             // ItemIndex : ModLink에서 위젯으로 보내주는거
IOTItemInt FanPwm(fan_pwm_out);     // WriteIndex : 위젯에서 ModLink로 보내주는 거
IOTItemInt FanPwmGraph;

IOTItemBin StopStatus;
IOTItemBin Stop(timeset_out);

IOTItemBin IntervalMUP(Interval_Mup);
IOTItemBin IntervalSUP(Interval_Sup);
IOTItemBin IntervalRST(IntervalReset);

IOTItemInt label_Minterval;
IOTItemInt label_Sinterval;

#define ITEM_COUNT 12

IOTItem *items[ITEM_COUNT] = {&FanStatus, &Fan,
                              &FanPwmValue, &FanPwm, &FanPwmGraph,
                              &StopStatus, &Stop,
                              &label_Minterval, &label_Sinterval,
                              &IntervalMUP, &IntervalSUP, &IntervalRST};

const char device_id[] = "d139056dbc1e785995b82b4dec2e1854";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup() {
    Serial.begin(250000);
    comm.SetInterval(200);

    SoftPWM.begin(490);
}

void IntervalSet(bool timeset) {
    if (!timeset) {
        TimeSum = (uint32_t)(Minute * 60 + Seconds) * 1000;
        TimerStartTime = millis();

        if (millis() > TimePushDelay + 500) {
            Minute += Interval_Mup_status;
            if (Minute >= 60)
                Minute = 0;
            Seconds += Interval_Sup_status;
            if (Seconds >= 60)
                Seconds = 0;

            TimePushDelay = millis();
        }
    }

    else if (timeset) {
        TimeCompare = (millis() - TimerStartTime) / TimeSum;
    }
}
void loop() {

    if (fan_out_status == true) {
        IntervalSet(timeset);

        if (timeset) {
            if (TimeCompare < 1) {
                SoftPWM.set(PWM);
            }
            else {
                SoftPWM.set(0);
            }
        }
        else if (!timeset) {
            SoftPWM.set(PWM);
        }
    }
    else {
        SoftPWM.set(0);
    }

    FanPwmValue.Set(PWM);
    FanPwmGraph.Set(PWM);
    FanStatus.Set(fan_out_status);
    StopStatus.Set(timeset);
    label_Minterval.Set(Minute);
    label_Sinterval.Set(Seconds);
    comm.Run();
}