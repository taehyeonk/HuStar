#include <U8g2lib.h>
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/U8X8_PIN_NONE);

#define SOILHUMI A6
#define PUMP 16

int Soilhumi = 0;

void setup(){
    u8g2.begin();
    pinMode(SOILHUMI, INPUT);
    pinMode(PUMP, OUTPUT);
}

void loop(){
    Soilhumi = map(analogRead(SOILHUMI), 0, 1023, 100, 0);

    if (isnan(Soilhumi))
    {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }

    if (Soilhumi <= 30) {
        digitalWrite(PUMP, HIGH);    
    }
    else if (Soilhumi >= 60) {
        digitalWrite(PUMP, LOW);
    }
    else { // Test를 수월하게 하기 위해 (30 < Soilhumi < 60)일때 OFF 동작
        digitalWrite(PUMP, LOW);
    }

    OLEDdraw();
}

void OLEDdraw()
{
    u8g2.clearBuffer();

    u8g2.setFont(u8g2_font_ncenB08_te);
    u8g2.drawStr(1, 15, "Exercise 03");

    u8g2.drawStr(15, 36, "Soilhumi:");
    u8g2.setCursor(85, 36);
    u8g2.print(Soilhumi);
    u8g2.drawStr(116, 36, "%");

    u8g2.sendBuffer();
}