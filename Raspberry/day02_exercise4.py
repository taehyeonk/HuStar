import board
import adafruit_dht
import RPi.GPIO as GPIO
import timeit

dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)

FAN_PIN1 = 18
FAN_PIN2 = 27

def onFan():
    GPIO.output(FAN_PIN1, GPIO.HIGH)
    GPIO.output(FAN_PIN2, GPIO.LOW)

def offFan():
    GPIO.output(FAN_PIN1, GPIO.LOW)
    GPIO.output(FAN_PIN2, GPIO.LOW)

def controlFan(temp, humi):
    if (temp >= 28 or humi >= 60):
        onFan()
    else:
        offFan()

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN1, GPIO.OUT, initial=False)
    GPIO.setup(FAN_PIN2, GPIO.OUT, initial=False)
    print("main() program")

    start_time = 0
    while True:
        if(timeit.default_timer() - start_time >= 1.0):
            try:
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity
                print("Temp: {:.1f}C   Humidity: {}%".format(temperature_c, humidity))

                controlFan(temperature_c, humidity)

                start_time = timeit.default_timer()
            except RuntimeError as error:
                print(error.args[0])
            except KeyboardInterrupt:
                GPIO.cleanup()

if __name__ == '__main__':
    main()