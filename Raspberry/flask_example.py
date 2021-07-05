import RPi.GPIO as GPIO

from flask import Flask
app = Flask(__name__)

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>')
def ledonoff(onoff):
    if onoff == "on":
        print("LED Turn on")
        GPIO.output(LED_1, 1)
        GPIO.output(LED_2, 1)
        GPIO.output(LED_3, 1)
        GPIO.output(LED_4, 1)

    elif onoff == "off":
        print("LED Turn off")
        GPIO.output(LED_1, 0)
        GPIO.output(LED_2, 0)
        GPIO.output(LED_3, 0)
        GPIO.output(LED_4, 0)

    return "LED"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_4, GPIO.OUT, initial=GPIO.LOW)
    app.run(host='0.0.0.0', port=5000, debug=True)