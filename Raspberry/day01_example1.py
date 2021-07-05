import RPi.GPIO as GPIO
from time import sleep

LED_1 = 4

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED_1, GPIO.OUT, initial=False)
    print("main() program running...")

    try:
        while True:
            GPIO.output(LED_1, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_1, GPIO.LOW)
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()