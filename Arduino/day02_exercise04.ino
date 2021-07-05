
#include <U8g2lib.h>
#include <SoftPWM.h>
#include "DHT.h"
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/U8X8_PIN_NONE);

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6
#define PUMP 16
#define LAMP 17

DHT dht(DHTPIN, DHTTYPE);
SOFTPWM_DEFINE_CHANNEL(A3);

uint32_t DHTTime = 2000; // 2초 간격
uint32_t SoilhumiTime = 3000; // 3초 간격
uint32_t LEDTime = 1000;

uint32_t DHT_ST = 0;
uint32_t Soilhumi_ST = 0;
uint32_t LED_ST = 0;

int Soilhumi = 0;
float Temp;
float Humi;
float Pwm;
bool Led = false;

String FanState;
String PumpState;
String LEDState;


void setup() {
    dht.begin();
    u8g2.begin();
    SoftPWM.begin(490);
    pinMode(SOILHUMI, INPUT);
    pinMode(PUMP, OUTPUT);
    pinMode(LAMP, OUTPUT);

    DHT_ST = millis();
    Soilhumi_ST = millis();
    LED_ST = millis();
}

void loop() {
    if((millis() - DHT_ST) > DHTTime) {
        Temp = dht.readTemperature();
        Humi = dht.readHumidity();

        if(isnan(Temp) || isnan(Humi)) {
            Serial.println(F("Failed to read from DHT sensor!"));
            return;
        }

        if(Temp >= 29) {
            SoftPWM.set(100);
            Pwm = 100;
            FanState = "ON";
        }
        else if(Temp <= 20) {
            SoftPWM.set(0);
            Pwm = 0;
            FanState = "OFF";
        }
        else {
            SoftPWM.set(65);
            Pwm = 65;
            FanState = "ON";
        }

        OLEDdraw();
        DHT_ST = millis();
    }

    if ((millis() - Soilhumi_ST) > SoilhumiTime) {
        Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);

        if(isnan(Soilhumi)) {
            Serial.println(F("Failed to read from DHT sensor!"));
            return;
        }

        if (Soilhumi >= 30 && Soilhumi <= 60) {
            digitalWrite(PUMP, HIGH);
            PumpState = "ON";
        }
        else {
            digitalWrite(PUMP, LOW);
            PumpState = "OFF";
        }

        OLEDdraw();
        Soilhumi_ST = millis();
    }

    if ((millis() - LED_ST) > LEDTime) {
        if (Led == true) {
            digitalWrite(LAMP, HIGH);
            LEDState = "ON";
            Led = false;
        }
        else {
            digitalWrite(LAMP, LOW);
            LEDState = "OFF";
            Led = true;
        }

        OLEDdraw();
        LED_ST = millis();
    }
}

void OLEDdraw() {
    u8g2.clearBuffer();

    u8g2.setFont(u8g2_font_ncenB08_te);
    u8g2.drawStr(1, 10, "Exercise 04");

    u8g2.drawStr(1, 22, "DT:");
    u8g2.setCursor(20, 22);
    u8g2.print(Temp);
    u8g2.drawStr(49, 22, "\xb0");
    u8g2.drawStr(54, 22, "C");

    u8g2.drawStr(61, 22, "|DH:");
    u8g2.setCursor(90, 22);
    u8g2.print(Humi);
    u8g2.drawStr(118, 22, "%");

    u8g2.drawStr(1, 32, "Soil Humi:");
    u8g2.setCursor(85, 32);
    u8g2.print(Soilhumi);
    u8g2.drawStr(100, 32, "%");

    u8g2.drawStr(1, 42, "FAN:");
    u8g2.setCursor(40, 42);
    u8g2.print(FanState);
    u8g2.setCursor(85, 42);
    u8g2.print(Pwm);
    u8g2.drawStr(118, 42, "%");

    u8g2.drawStr(1, 52, "PUMP:");
    u8g2.setCursor(50, 52);
    u8g2.print(PumpState);

    u8g2.drawStr(1, 62, "LED:");
    u8g2.setCursor(30, 62);
    u8g2.print(LEDState);
    u8g2.drawStr(63, 62, "Time:");
    u8g2.setCursor(100, 62);
    u8g2.print(LEDTime / 1000);
    u8g2.drawStr(108, 62, "s");

    u8g2.sendBuffer();
}