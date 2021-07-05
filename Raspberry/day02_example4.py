import RPi.GPIO as GPIO
from time import sleep

ON = 1
OFF = 0

FAN_PIN1 = 18
FAN_PIN2 = 27

def onFan():
    GPIO.output(FAN_PIN1, GPIO.HIGH)
    GPIO.output(FAN_PIN2, GPIO.LOW)

def offFan():
    GPIO.output(FAN_PIN1, GPIO.LOW)
    GPIO.output(FAN_PIN2, GPIO.LOW)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN1, GPIO.OUT, initial=False)
    GPIO.setup(FAN_PIN2, GPIO.OUT, initial=False)
    print("Setup FAN pin as outputs")
    print("main() program")

    try:
        while True:
            onFan()
            sleep(3.0)
            offFan()
            sleep(1.0)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()