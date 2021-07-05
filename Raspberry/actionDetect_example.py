import RPi.GPIO as GPIO
from time import sleep
import GPIO_EX

PIR_PIN = 7
pirState = 0

def readPir(detect_state):
    global pirState
    while detect_state:
        input_state = GPIO_EX.input(PIR_PIN)
        if input_state == True:
            if pirState == 0:
                print("\r\nMotion Detected.")
            pirState = 1
            return 1
        else:
            if pirState == 1:
                print("\r\nMotion Ended.")
            pirState = 0
            return 0

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO_EX.setup(PIR_PIN, GPIO_EX.IN)

    print("start pir program ...")

    try:
        while True:
            readPir(1)
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()