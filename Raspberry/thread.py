# python3 exercise4.py
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

is_Obama = 0

def face_detect():
    global is_Obama

    face_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_alt2.xml')
    # eye_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_eye.xml')
    # smile_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_smile.xml')


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("../../OpenCV-Python-Series/src/recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open("../../OpenCV-Python-Series/src/pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

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
                if name != 'obama':
                    is_Obama = 0
                else:
                    is_Obama = 1
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

# LED
LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_4, LED_3]

# flag on flask request
led_on = False

# led
def turn_led(num):
    global led_on
    if led_on:
        GPIO.output(LEDs[:num], 1)
        GPIO.output(LEDs[num:], 0)
    else:
        GPIO.output(LEDs, 0)

# thread 2
def smart_home():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=GPIO.LOW)

    print("smartHome activate")

    while True:
        try:            
            # on-off by flags
            turn_led(4)

        except KeyboardInterrupt:
            lcd.clear()
            spi.close()
            GPIO.cleanup()
        except RuntimeError as error:
            print(error.args[0])

# =================================================================================================
# Flask Server w/ IFTTT

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"


@app.route('/led/<onoff>')
def led_onoff(onoff):
    global led_on

    if onoff == "on":
        led_on = True

    elif onoff == "off":
        led_on = False

    return "led"


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

    app.run(host='0.0.0.0', port=5000, debug=True)
