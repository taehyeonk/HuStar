import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import RPi.GPIO as GPIO
from time import sleep
import GPIO_EX

from types import GetSetDescriptorType
import numpy as np
import cv2
import pickle
import threading

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

# Keypad
def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)

def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
            sleep(0.001)
        else:
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
            sleep(0.001)
    return rowNum

def readCol():
    keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            keypadstate = keypadstate + (i + 2)
            sleep(0.5)
    return keypadstate

def readKeypad():
    global g_preData
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)
    sleep(0.001)
    if(row1Data != -1):
        keyData = row1Data
    
    runningStep = selectRow(2)
    row2Data = readCol()
    selectRow(0)
    sleep(0.001)
    if(row2Data != -1):
        keyData = row2Data + 3

    runningStep = selectRow(3)
    row2Data = readCol()
    selectRow(0)
    sleep(0.001)
    if(row2Data != -1):
        keyData = row2Data + 6

    runningStep = selectRow(4)
    row2Data = readCol()
    selectRow(0)
    sleep(0.001)
    if(row2Data != -1):
        if(row2Data == 1):
            keyData = "*"
        elif(row2Data == 2):
            keyData = 0
        elif(row2Data == 3):
            keyData = "#"

    sleep(0.1)

    if keyData == -1:
        return -1
    
    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    print("\r\nKeypad Data : %s" % keyData)

    return keyData

# LCD
def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0, 0)
    sleep(1.0)

def displayText(text='', col=0, row=0):
    lcd.cursor_position(col, row)
    lcd.message = text

def clearTextlcd():
    lcd.clear()
    lcd.message = 'clear LCD\nGoodbye!'
    sleep(2.0)
    lcd.clear()

def inputPassword():
    count = 0
    passwd = ''
    while True:
        if count == 4:
            break

        keyData = readKeypad()
        if keyData != -1:
            passwd += str(keyData)
            count += 1
    return passwd



def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    initKeypad()
    initTextlcd()
    print("setup keypad pin")
    print("start textlcd program ...")
    passwd1 = ''
    passwd2 = ''
    count = 0
    try:
        line = "input password!"
        lcd.clear()
        displayText(line, 0, 0)
        sleep(2.0)
        
        passwd1 = inputPassword()
        
        lcd.clear()
        displayText(passwd1, 0, 0)
        sleep(2.0)
        
        lcd.clear()
        line = "confirm password!"
        displayText(line, 0, 0)
        sleep(2.0)

        passwd2 = inputPassword()

        lcd.clear()
        displayText(passwd1, 0, 0)
        if(passwd1 == passwd2):
            displayText("CORRECT", 0, 1)
        else:
            displayText("FAIL", 0, 1)
        sleep(3.0)

    except KeyboardInterrupt:
        GPIO.cleanup()
    except KeyboardInterrupt:
        clearTextlcd()
    

if __name__ == '__main__':
    global t1
    t1 = threading.Thread(target=CV)
    t1.daemon = True
    t1.start()

    global t2
    t2 = threading.Thread(target=main)
    t2.daemon = True
    t2.start()

    app.run()









led_status = 0


def controlDevice():
	while True:
		if(led_status == 1):
			GPIO.output(4, 1)
		else:
			GPIO.output(4, 0)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)



def CV():
    global led_status

    face_cascade = cv2.CascadeClassifier(
        'cascades/data/haarcascade_frontalface_alt2.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')


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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w]  # (ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 4 and conf <= 85:
                #print(5: #id_)
                #print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

                if name == "obama":
                    led_status = 1
                else:
                    led_status = 0

            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            #subitems = smile_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in subitems:
            #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()