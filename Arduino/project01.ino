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

uint32_t TimePushDelay = 0;

// 온도, 습도, 토양 습도 2초 간격으로 갱신
uint32_t THS_Delay = 2000;
uint32_t THS_ST = 0;

uint32_t Fan_ST = 0;
uint32_t Pump_ST = 0;
uint32_t Led_ST = 0;

int Soilhumi = 0;
float Temp;
float Humi;

// fan 관련 변수
bool fan_light;
bool fan_action_btn = false;
int32_t fan_time;
bool fan_out_status = false;
int32_t fan_temp_1 = 24;
int32_t fan_temp_2 = 30;
int fan_pwm_1 = 70;
int fan_pwm_2 = 100;
bool fan_pwm_1_up;
bool fan_pwm_1_down;
bool fan_pwm_2_up;
bool fan_pwm_2_down;

// pump 관련 변수
bool pump_light;
bool pump_action_btn = false;
int32_t pump_time;
bool pump_out_status = false;
int32_t pump_humi_1 = 30;
int32_t pump_humi_2 = 60;
bool pump_term_status;
int pump_term_seconds = 0;
uint32_t Pump_Term_ST = 0;
uint32_t pump_term_seconds_sum = 0;
uint32_t pump_term_seconds_compare;
bool pump_term_up;
bool pump_term_down;

// led 관련 변수
bool led_light;
bool led_action_btn = false;
int32_t led_time;
bool led_out_status = false;
uint32_t Led_Term_ST = 0;
uint32_t led_term_seconds_sum = 0;
uint32_t led_term_seconds_compare;
int led_hour = 0;
int led_minute = 0;
int led_seconds = 0;
bool led_hour_up;
bool led_hour_down;
bool led_minute_up;
bool led_minute_down;
bool led_seconds_up;
bool led_seconds_down;
bool led_set;

// FAN 관련 함수
void fan_out(bool val) {
    fan_out_status = val;
}
void fan_actionBtn_out(bool val) {
    fan_action_btn = val;
}
void fan_time_out(int32_t val) {
    fan_time = val;
}
void fan_temp1_out(int32_t val) {
    fan_temp_1 = val;
}
void fan_temp2_out(int32_t val) {
    fan_temp_2 = val;
}
void fan_pwm1_up(bool val) {
    fan_pwm_1_up = val;
}
void fan_pwm1_down(bool val) {
    fan_pwm_1_down = val;
}
void fan_pwm2_up(bool val) {
    fan_pwm_2_up = val;
}
void fan_pwm2_down(bool val) {
    fan_pwm_2_down = val;
}
void fan_resetBtn_out(bool val) {
    if(val){
        fan_pwm_1 = 0;
        fan_pwm_2 = 0;
    }
}

// PUMP 관련 함수
void pump_out(bool val) {
    pump_out_status = val;
}
void pump_actionBtn_out(bool val) {
    pump_action_btn = val;
}
void pump_time_out(int32_t val) {
    pump_time = val;
}
void pump_humi1_out(int32_t val) {
    pump_humi_1 = val;
}
void pump_humi2_out(int32_t val) {
    pump_humi_2 = val;
}
void pump_term_out(bool val) {
    pump_term_status = val;
}
void pump_term_up_out(bool val) {
    pump_term_up = val;
}
void pump_term_down_out(bool val) {
    pump_term_down = val;
}

// LED 관련 함수
void led_out(bool val) {
    led_out_status = val;
}
void led_actionBtn_out(bool val) {
    led_action_btn = val;
}
void led_time_out(int32_t val) {
    led_time = val;
}
void Led_Hup(bool val) {
    led_hour_up = val;
}
void Led_Hdown(bool val) {
    led_hour_down = val;
}
void Led_Mup(bool val) {
    led_minute_up = val;
}
void Led_Mdown(bool val) {
    led_minute_down = val;
}
void Led_Sup(bool val) {
    led_seconds_up = val;
}
void Led_Sdown(bool val) {
    led_seconds_down = val;
}
void Led_Set(bool val) {
    led_set = val;
}
void Led_Reset(bool val) {
    if(val){
        led_hour = 0;
        led_minute = 0;
        led_seconds = 0;
    }
}

// 온도, 습도, 토양 습도 위젯
IOTItemFlo dht22_temp;
IOTItemFlo dht22_humi;
IOTItemInt soilhumi;

// FAN 관련 위젯
    // 수동 조작
IOTItemBin FanActionLight;
IOTItemBin FanActionButton(fan_actionBtn_out);
IOTItemInt FanActionTimeValue;
IOTItemInt FanActionTime(fan_time_out);
    // Auto 토글
IOTItemBin FanAutoStatus;
IOTItemBin FanAuto(fan_out);
    // 자동 조작
IOTItemInt FanTemp1Value;                       // 구동 온도 기준 progress bar 1
IOTItemInt FanTemp1(fan_temp1_out);             // 구동 온도 기준 progress bar 1
IOTItemInt FanTemp2Value;                       // 구동 온도 기준 progress bar 2
IOTItemInt FanTemp2(fan_temp2_out);             // 구동 온도 기준 progress bar 2
IOTItemInt FanTemp1PWM;                         // 풍량 1
IOTItemInt FanTemp2PWM;                         // 풍량 2
IOTItemBin FanTemp1PWM_up(fan_pwm1_up);         // 풍량 1 up 버튼
IOTItemBin FanTemp1PWM_down(fan_pwm1_down);     // 풍량 1 donw 버튼
IOTItemBin FanTemp2PWM_up(fan_pwm2_up);         // 풍량 2 up 버튼
IOTItemBin FanTemp2PWM_down(fan_pwm2_down);     // 풍량 2 down 버튼
IOTItemBin FanPWMReset(fan_resetBtn_out);       // 풍량 세팅 초기화 버튼

// PUMP 관련 위젯
    // 수동 조작
IOTItemBin PumpActionLight;
IOTItemBin PumpActionButton(pump_actionBtn_out);
IOTItemInt PumpActionTimeValue;
IOTItemInt PumpActionTime(pump_time_out);
    // Auto 토글
IOTItemBin PumpAutoStatus;
IOTItemBin PumpAuto(pump_out);
    // 자동 조작
IOTItemInt PumpHumiStartValue;
IOTItemInt PumpHumiStart(pump_humi1_out);
IOTItemInt PumpHumiEndValue;
IOTItemInt PumpHumiEnd(pump_humi2_out);
IOTItemBin PumpActionTermStatus;
IOTItemBin PumpActionTerm(pump_term_out);
IOTItemInt PumpTerm;
IOTItemBin PumpTerm_up(pump_term_up_out);
IOTItemBin PumpTerm_down(pump_term_down_out);

// LED 관련 위젯
    // 수동 조작
IOTItemBin LedActionLight;
IOTItemBin LedActionButton(led_actionBtn_out);
IOTItemInt LedActionTimeValue;
IOTItemInt LedActionTime(led_time_out);
    // Auto 토글
IOTItemBin LedAutoStatus;
IOTItemBin LedAuto(led_out);
    // 자동 조작
IOTItemInt LedTermHour;
IOTItemBin LedTermHour_up(Led_Hup);
IOTItemBin LedTermHour_down(Led_Hdown);
IOTItemInt LedTermMinute;
IOTItemBin LedTermMinute_up(Led_Mup);
IOTItemBin LedTermMinute_down(Led_Mdown);
IOTItemInt LedTermSeconds;
IOTItemBin LedTermSeconds_up(Led_Sup);
IOTItemBin LedTermSeconds_down(Led_Sdown);
IOTItemBin LedTermSet(Led_Set);
IOTItemBin LedTermReset(Led_Reset);

#define ITEM_COUNT 52

IOTItem *items[ITEM_COUNT] = {
    &dht22_temp, &dht22_humi, &soilhumi,
    &FanActionLight, &FanActionButton, &FanActionTimeValue, &FanActionTime, &FanAutoStatus, &FanAuto,
    &FanTemp1Value, &FanTemp1, &FanTemp2Value, &FanTemp2, &FanTemp1PWM, &FanTemp2PWM, &FanTemp1PWM_up, &FanTemp1PWM_down, &FanTemp2PWM_up, &FanTemp2PWM_down, &FanPWMReset,
    &PumpActionLight, &PumpActionButton, &PumpActionTimeValue, &PumpActionTime, &PumpAutoStatus, &PumpAuto,
    &PumpHumiStartValue, &PumpHumiStart, &PumpHumiEndValue, &PumpHumiEnd, &PumpActionTermStatus, &PumpActionTerm, &PumpTerm, &PumpTerm_up, &PumpTerm_down,
    &LedActionLight, &LedActionButton, &LedActionTimeValue, &LedActionTime, &LedAutoStatus, &LedAuto,
    &LedTermHour, &LedTermHour_up, &LedTermHour_down, &LedTermMinute, &LedTermMinute_up, &LedTermMinute_down, &LedTermSeconds, &LedTermSeconds_up, &LedTermSeconds_down, &LedTermSet, &LedTermReset
};

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

    THS_ST = millis();
    Fan_ST = millis();
    Pump_ST = millis();
    Led_ST = millis();

    Pump_Term_ST = millis();
    Led_Term_ST = millis();
}

void PumpIntervalSet(bool timeset) {
    if (!timeset) { // 시간 설정 스위치가 OFF일 때
        pump_term_seconds_sum=(uint32_t)pump_term_seconds * 1000;
        Pump_Term_ST = millis();
    }
    else if (timeset) {
        pump_term_seconds_compare = (millis() - Pump_Term_ST) / pump_term_seconds_sum;
    }
}

void LedIntervalSet(bool timeset) {
    if (timeset) { // SET 버튼 클릭 시
        led_term_seconds_sum = (uint32_t)(led_hour*3600 + led_minute*60 + led_seconds) * 1000;
        Led_Term_ST = millis();
    }
    else if (!timeset) {
        led_term_seconds_compare = (millis() - Led_Term_ST) / led_term_seconds_sum;
    }
}

void loop()
{
    // 2초 간격으로 온도, 습도, 토양 습도 체크
    if((millis() - THS_ST) > THS_Delay) {
        Temp = dht.readTemperature();
        Humi = dht.readHumidity();
        Soilhumi = map(analogRead(SOILHUMI), 0, 1023, 100, 0);

        // if(isnan(Temp) || isnan(Humi) || isnan(Soilhumi)) {
        //     Serial.println(F("Failed to read from DHT sensor!"));
        //     return;
        // }

        THS_ST = millis();
    }

    // [FAN 동작]
    if(fan_out_status == false) {  // 수동 조작일 경우
        if(fan_action_btn == true) {    // 동작 버튼을 누르면
            Fan_ST = millis();
        }
        else {
            if((millis() - Fan_ST) < fan_time * 1000) {
                SoftPWM.set(100);
                fan_light = true;
            }
            else {
                SoftPWM.set(0);
                fan_light = false;
            }
        }
    }
    else {
        if(Temp >= fan_temp_1 && Temp < fan_temp_2) {
            SoftPWM.set(fan_pwm_1);
            fan_light = true;
        }
        else if(Temp >= fan_temp_2) {
            SoftPWM.set(fan_pwm_2);
            fan_light = true;
        }
        else {
            SoftPWM.set(0);
            fan_light = false;
        }
    }
    // 버튼 동작
    if(fan_pwm_1_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            fan_pwm_1 += 5;
            if(fan_pwm_1 > 100) {
                fan_pwm_1 = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(fan_pwm_1_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            fan_pwm_1 -= 5;
            if(fan_pwm_1 < 0) {
                fan_pwm_1 = 100;
            }
            TimePushDelay = millis();
        }
    }
    if(fan_pwm_2_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            fan_pwm_2 += 5;
            if(fan_pwm_2 > 100) {
                fan_pwm_2 = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(fan_pwm_2_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            fan_pwm_2 -= 5;
            if(fan_pwm_2 < 0) {
                fan_pwm_2 = 100;
            }
            TimePushDelay = millis();
        }
    }

    // [PUMP 동작]
    PumpIntervalSet(pump_term_status);
    if(pump_out_status == false) {  // 수동 조작일 경우
        if(pump_action_btn == true){    // 동작 버튼을 누르면
            Pump_ST = millis();
        }
        else {
            if((millis() - Pump_ST) < pump_time * 1000) {
                digitalWrite(PUMP, HIGH);
                pump_light = true;
            }
            else {
                digitalWrite(PUMP, LOW);
                pump_light = false;
            }
        }
    }
    else {
        if (Soilhumi >= pump_humi_1 && Soilhumi <= pump_humi_2) {
            if (pump_term_status == true) { //토글동작
                if (pump_term_seconds_compare % 2 == 0) {
                    digitalWrite(PUMP, LOW);
                    pump_light = false;
                }
                else if (pump_term_seconds_compare % 2 == 1) {
                    digitalWrite(PUMP, HIGH);
                    pump_light = true;
                }
            }
            else {  //일반 동작
                digitalWrite(PUMP, HIGH);
                pump_light = true;
            }
        }
        else {
            digitalWrite(PUMP, LOW);
            pump_light = false;
        }
    }
    // 버튼 동작
    if(pump_term_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            pump_term_seconds += 1;
            if(pump_term_seconds >= 60) {
                pump_term_seconds = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(pump_term_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            pump_term_seconds -= 1;
            if(pump_term_seconds < 0) {
                pump_term_seconds = 59;
            }
            TimePushDelay = millis();
        }
    }

    // [LED 동작]
    LedIntervalSet(led_set);
    if(led_out_status == false) {  // 수동 조작일 경우
        if(led_action_btn == true){ // 동작 버튼을 누르면
            Led_ST = millis();
        }
        else {
            if((millis() - Led_ST) < led_time * 1000) {
                digitalWrite(LAMP, HIGH);
                led_light = true;
            }
            else {
                digitalWrite(LAMP, LOW);
                led_light = false;
            }
        }
    }
    else {
        if (led_term_seconds_compare % 2 == 0) {
            digitalWrite(LAMP, LOW);
            led_light = false;
        }
        else if (led_term_seconds_compare % 2 == 1) {
            digitalWrite(LAMP, HIGH);
            led_light = true;
        }
    }
    // 버튼 동작
    if(led_hour_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_hour += 1;
            if(led_hour >= 24) {
                led_hour = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(led_hour_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_hour -= 1;
            if(led_hour < 0) {
                led_hour = 23;
            }
            TimePushDelay = millis();
        }
    }
    if(led_minute_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_minute += 1;
            if(led_minute >= 60) {
                led_minute = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(led_minute_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_minute -= 1;
            if(led_minute < 0) {
                led_minute = 59;
            }
            TimePushDelay = millis();
        }
    }
    if(led_seconds_up == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_seconds += 1;
            if(led_seconds >= 60) {
                led_seconds = 0;
            }
            TimePushDelay = millis();
        }
    }
    if(led_seconds_down == true) {
        if(millis() >= TimePushDelay + 1000) {
            led_seconds -= 1;
            if(led_seconds < 0) {
                led_seconds = 59;
            }
            TimePushDelay = millis();
        }
    }

    // 온도, 습도, 토양 습도 출력
    dht22_temp.Set(Temp);
    dht22_humi.Set(Humi);
    soilhumi.Set(Soilhumi);

    FanActionLight.Set(fan_light);
    FanActionTimeValue.Set(fan_time);
    FanAutoStatus.Set(fan_out_status);
    FanTemp1Value.Set(fan_temp_1);
    FanTemp2Value.Set(fan_temp_2);
    FanTemp1PWM.Set(fan_pwm_1);
    FanTemp2PWM.Set(fan_pwm_2);

    PumpActionLight.Set(pump_light);
    PumpActionTimeValue.Set(pump_time);
    PumpAutoStatus.Set(pump_out_status);
    PumpHumiStartValue.Set(pump_humi_1);
    PumpHumiEndValue.Set(pump_humi_2);
    PumpActionTermStatus.Set(pump_term_status);
    PumpTerm.Set(pump_term_seconds);

    LedActionLight.Set(led_light);
    LedActionTimeValue.Set(led_time);
    LedAutoStatus.Set(led_out_status);
    LedTermHour.Set(led_hour);
    LedTermMinute.Set(led_minute);
    LedTermSeconds.Set(led_seconds);
    
    comm.Run();
}