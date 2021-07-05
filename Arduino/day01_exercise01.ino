
#include <U8g2lib.h>
#include "DHT.h"
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/U8X8_PIN_NONE);

#define SOILHUMI A6
#define DHTPIN A1
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

uint32_t DataCaptureDelay = 3000;
uint32_t DataCapture_ST = 0;

float Temp;
float Humi;
int Soilhumi = 0;

void setup()
{
    dht.begin();
    u8g2.begin();
    pinMode(SOILHUMI, INPUT);

    DataCapture_ST = millis();
}

void loop()
{
    if ((millis() - DataCapture_ST) > DataCaptureDelay)
    {
        Humi = dht.readHumidity();
        Temp = dht.readTemperature();
        Soilhumi = map(analogRead(SOILHUMI), 0, 1023, 100, 0);

        if (isnan(Humi) || isnan(Temp) || isnan(Soilhumi))
        {
            Serial.println(F("Failed to read from DHT sensor!"));
            return;
        }

        OLEDdraw();
        DataCapture_ST = millis();
    }
}

void OLEDdraw()
{
    u8g2.clearBuffer();

    u8g2.setFont(u8g2_font_ncenB08_te);
    u8g2.drawStr(1, 15, "Exercise 01");

    u8g2.drawStr(15, 36, "Temp.");
    u8g2.setCursor(85, 36);
    u8g2.print(Temp);
    u8g2.drawStr(114, 36, "\xb0");
    u8g2.drawStr(11, 36, "C");

    u8g2.drawStr(15, 47, "Humidity");
    u8g2.setCursor(85, 47);
    u8g2.print(Humi);
    u8g2.drawStr(116, 47, "%");

    u8g2.drawStr(15, 58, "Soilhumi");
    u8g2.setCursor(85, 58);
    u8g2.print(Soilhumi);
    u8g2.drawStr(116, 58, "%");


    u8g2.sendBuffer();
}