
# python3 [filename.py]
# ./ngrok http 5000
# googlesamples-assistant-pushtotalk

# if display error:
# export DISPLAY=:0.0
# xhost +local:root
# xhost +localhost

# smarthome module
import RPi.GPIO as GPIO
import GPIO_EX
import adafruit_dht
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import spidev
import timeit

# flask module
from flask import Flask

# AI module
import numpy as np
import cv2
import pickle
import threading

# ETC
from time import sleep, time

# =================================================================================================
# Thread1 - Face Detection

is_Obama = False
is_Obama_pir = False
is_Clinton = False

def face_detect():
    global is_Obama
    global is_Obama_pir
    global is_Clinton

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    # eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    # smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                #print(5: #id_)
                #print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
                # added code
                if name == 'obama':
                    is_Obama = True
                    is_Obama_pir = True

                if name == 'clinton':
                    is_Clinton = True

                # added code - end

            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            #subitems = smile_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in subitems:
            #   cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



# ====================================================================================================
# Thread2 - Smart Home Control

# LCD
# Raspberry Pi pin setup
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D19)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0, 0)

def displayText(text='', col=0, row=0):
    lcd.cursor_position(col, row)
    lcd.message = text

def clearTextlcd():
    lcd.clear()
    lcd.message = 'clear LCD\nGoodbye!'
    sleep(2.0)
    lcd.clear()

# CDS, GAS
spi = spidev.SpiDev()
CDS_CHANNEL = 0
GAS_CHANNEL = 1

def initMcp3208():
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi.mode = 3

def buildReadCommand(channel):
    startBit = 0x04
    singleEnded = 0x08

    configBit = [startBit | ((singleEnded | (channel & 0x07)) >> 2), (channel & 0x07) << 6, 0x00]

    return configBit

def processAdcValue(result):
    byte2 = (result[1] & 0x0F)
    return (byte2 << 8) | result[2]

def analogRead(channel):
    if(channel > 7) or (channel < 0):
        return -1
    
    r = spi.xfer2(buildReadCommand(channel))
    adc_out = processAdcValue(r)
    return adc_out
    
def controlMcp3208(channel):
    analogVal = analogRead(channel)
    return analogVal

def readSensor(channel):
    return controlMcp3208(channel)

# DHT11
dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)
temp = 0
humi = 0

# PIR
PIR_PIN = 7
pirState = False
pir_start_time = timeit.default_timer()
timeCheck = False # 일단 한번 Motion Detected를 하면 3초 동안 시간을 확인하기 위한 변수

def readPir():
    global pirState, pir_start_time, is_Obama_pir, timeCheck

    input_state = GPIO_EX.input(PIR_PIN)
    if input_state == True:
        if pirState == False:
            # Motion Detected
            is_Obama_pir = False
            timeCheck = True
            pir_start_time = timeit.default_timer()
        pirState = True
    else:
        if pirState == True:
            # Motion Ended
            pass
        pirState = False
        

#---------------------------------------------------
# LED
LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_4, LED_3]

# FAN
FAN_PIN1 = 18
FAN_PIN2 = 27
FANs = [FAN_PIN1, FAN_PIN2]

# BUZZER
BUZZER_PIN = 7

scale = [261, 294, 329, 349, 392, 440, 493, 523]
melodyList = [2, 0, 4, 7]
noteDurations = [0.5, 0.5, 0.5, 0.5]


# flag on flask request
led_on = False
fan_on = False
buz_on = False
auto_on = False

# led
def turn_led(num):
    if led_on:
        GPIO.output(LEDs[:num], 1)
        GPIO.output(LEDs[num:], 0)
    else:
        GPIO.output(LEDs, 0)

# fan
def turn_fan():
    if fan_on:
        GPIO.output(FAN_PIN1, 1)
        GPIO.output(FAN_PIN2, 0)
    else:
        GPIO.output(FAN_PIN1, 0)
        GPIO.output(FAN_PIN2, 0)

# buzzer
def playBuzzer(pwm, melodyList, noteDurations):
    pwm.start(100)
    pwm.ChangeDutyCycle(50)

    for i in range(len(melodyList)):
        pwm.ChangeFrequency(scale[melodyList[i]])
        sleep(noteDurations[i])
    pwm.stop()

def turn_buz(pwm):
    if buz_on:
        playBuzzer(pwm, melodyList, noteDurations)
    else:
        pwm.stop()

# thread 2
def smart_home():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FANs, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, 100)
    GPIO_EX.setup(PIR_PIN, GPIO_EX.IN)

    initMcp3208()

    print("smartHome activate")

    global is_Clinton
    lcd.clear()
    displayText("Face Checking", 0, 0)
    while True:
        if is_Obama == True:
            if inputPwdKeypad() == True:
                break
        if is_Clinton == True:
            lcd.clear()
            displayText('Access Denied')
            sleep(1.0)
            is_Clinton = False
            lcd.clear()
            displayText("Face Checking", 0, 0)
    
    if pwd_corret == True:

        start_time = timeit.default_timer()
        global timeCheck # pir timecheck를 좀 더 수월하게 하기 위한 처리
        while True:
            try:
                # 1초 간격으로 센서 동작 (PIR 제외)
                if(timeit.default_timer() - start_time >= 2.0):
                    global temp, humi, CdsVal, GasVal

                    # DHT11 action
                    temp = dhtDevice.temperature
                    humi = dhtDevice.humidity
                    # CDS action
                    CdsVal = readSensor(CDS_CHANNEL)
                    # GAS action
                    GasVal = readSensor(GAS_CHANNEL)

                    # PIR action
                    readPir()
                    if timeCheck == True:
                        # 때가 되면
                        if timeit.default_timer() - pir_start_time >= 3.0:
                            if is_Obama_pir == False:
                                playBuzzer(pwm, melodyList, noteDurations)
                            timeCheck = False

                    # LCD 출력
                    line1 = "T." + str(temp) + "C H." + str(humi) + "% " + "P." + str(pirState)
                    line2 = "C." + str(CdsVal) + " G." + str(GasVal)
                    lcd.clear()
                    displayText(line1, 0, 0)
                    displayText(line2, 0, 1)

                    # print("Temp: {:.1f}C   Humi: {}%".format(temp, humi))
                    # print("CDS Val=%d" % CdsVal)
                    # print("GAS Val=%d" % GasVal)
                    print("PIR 센서 상태 : ------------")
                    print("PIR Val={}".format(pirState))
                    print("---------------------------")

                    start_time = timeit.default_timer()

            
                # on-off by flags
                if auto_on:
                    # 자동 조작일 경우
                    if CdsVal > 3200:
                        turn_led(0)
                    elif CdsVal > 2400:
                        turn_led(1)
                    elif CdsVal > 1500:
                        turn_led(2)
                    elif CdsVal > 800:
                        turn_led(3)
                    else:
                        turn_led(4)
                    
                    if temp >= 28 or humi >= 60:
                        turn_fan()
                    else:
                        turn_fan()

                else:
                    # 수동 조작일 경우
                    turn_led(4)
                    turn_fan()
                    turn_buz(pwm)
                

            except KeyboardInterrupt:
                clearTextlcd()
                spi.close()
                GPIO.cleanup()
            except RuntimeError as error:
                print(error.args[0])

# =================================================================================================
# DoorLock
#KeyPad====================================================================================================================
ROW0_PIN = 0
ROW1_PIN = 1
ROW2_PIN = 2
ROW3_PIN = 3
COL0_PIN = 4
COL1_PIN = 5
COL2_PIN = 6
COL_NUM = 3
ROW_NUM = 4
g_preData = 0

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

pwd_corret = False

def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)


def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)        
        else:
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
        
    return rowNum


def readCol():
    keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            keypadstate = keypadstate + (i + 2)  
    return keypadstate


def readKeypad():
    global g_preData
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)

    if (row1Data != -1):
        keyData = row1Data

    if runningStep == 1:
        if keyData == -1:
            runningStep = selectRow(2)
            row2Data = readCol()
            selectRow(0)      
            if (row2Data != -1):
                keyData = row2Data + 3

    if runningStep == 2:
        if keyData == -1:
            runningStep = selectRow(3)
            row3Data = readCol()
            selectRow(0)
            if (row3Data != -1):
                keyData = row3Data + 6

    if runningStep == 3:
        if keyData == -1:
            runningStep = selectRow(4)
            row4Data = readCol()
            selectRow(0)
            if (row4Data != -1):
                if row4Data == 2:
                    keyData = 0
                if row4Data==1:
                    keyData='*'
                if row4Data==3:
                    keyData='#'
    sleep(0.1)
    if keyData == -1:
        return -1

    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    print("\r\nKeypad Data : %s" % keyData)
    return keyData

def inputPwdKeypad():
    global pwd_corret
    try:
        initKeypad()
        pwd='486#'
        lcd.clear()
        displayText('Input PWD',0,0)
        cnt=0
        num_list=[]
        while cnt<=3:
            keyData = readKeypad()
            if(keyData!=-1):
                num_list.append(keyData)
                cnt+=1
        
        num_str=",".join(str(n) for n in num_list)
        num_str=num_str.replace(',','')
        
        lcd.clear()
        displayText(num_str,0,0)
        if(pwd==num_str):
            pwd_corret=True
            displayText('CORRECT',0,5)
            sleep(1)
            return True
        else:
            displayText('FAIL',0,5)
            sleep(1)
            return False            
    except KeyboardInterrupt:
        clearTextlcd()

def quitKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], False)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], False)

#KeyPad====================================================================================================================


# =================================================================================================
# Flask Server w/ IFTTT

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>')
def led_onoff(onoff):
    global led_on

    if auto_on == False:
        if onoff == "on":
            led_on = True

        elif onoff == "off":
            led_on = False

    return "led"

@app.route('/fan/<onoff>')
def fan_onoff(onoff):
    global fan_on

    if auto_on == False:
        if onoff == "on":
            fan_on = True

        elif onoff == "off":
            fan_on = False

    return "fan"

@app.route('/buzzer/<onoff>')
def buz_onoff(onoff):
    global buz_on

    if auto_on == False:
        if onoff == "on":
            buz_on = True

        elif onoff == "off":
            buz_on = False

    return "buzzer"

@app.route('/auto/<onoff>')
def auto_onoff(onoff):
    global auto_on, led_on, fan_on, buz_on

    if onoff == "on":
        auto_on = True
        led_on = True
        fan_on = True
        buz_on = True

    elif onoff == "off":
        auto_on = False
        led_on = False
        fan_on = False
        buz_on = False

    return "auto"


# =================================================================================================
# execute code

if __name__ == "__main__":

    # run faceDetact function with thread t1
    global t1
    t1 = threading.Thread(target=face_detect)
    t1.daemon = True
    t1.start()

    # run smarthome function with thread t1
    global t2
    t2 = threading.Thread(target=smart_home)
    t2.daemon = True
    t2.start()

    app.run(host='0.0.0.0', port=5000, debug=False)