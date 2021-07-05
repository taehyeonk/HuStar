
#include <U8g2lib.h>
#include <SoftPWM.h>
#include "DHT.h"
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

#define SOILHUMI A6
#define DHTPIN A1
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
SOFTPWM_DEFINE_CHANNEL(A3);

uint32_t DataCaptureDelay = 3000;
uint32_t DataCapture_ST = 0;

// int Soilhumi = 0;
float Temp;
float Pwm;
String OnOff;

void setup() {
    pinMode(SOILHUMI, INPUT);
    dht.begin();
    u8g2.begin();

    // SoftPWM.begin(490);
    DataCapture_ST = millis();
}

void loop() {
    if((millis() - DataCapture_ST) > DataCaptureDelay) {
        Temp = dht.readTemperature();
        // Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);

        if(isnan(Temp)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
        }

        if(Temp >= 30) {
            SoftPWM.set(100);
            Pwm = 100;
            OnOff = "ON";
        }
        else if(Temp <= 25) {
            SoftPWM.set(0);
            Pwm = 0;
            OnOff = "OFF";
        }
        else {
            SoftPWM.set(65);
            Pwm = 65;
            OnOff = "ON";
        }

        OLEDdraw();
        DataCapture_ST = millis();
    }
}

void OLEDdraw() {
    u8g2.clearBuffer();

    u8g2.setFont(u8g2_font_ncenB08_te);
    u8g2.drawStr(1, 15, "Exercise 02");

    u8g2.drawStr(15, 36, "Temp:");
    u8g2.setCursor(85, 36);
    u8g2.print(Temp);
    u8g2.drawStr(114, 36, "\xb0");
    u8g2.drawStr(11, 36, "C");
    u8g2.drawStr(15, 47, "PWM:");
    u8g2.setCursor(85, 47);
    u8g2.print(Pwm);
    u8g2.drawStr(116, 47, "%");

    u8g2.setCursor(85, 58);
    u8g2.print(OnOff);

    u8g2.sendBuffer();
}