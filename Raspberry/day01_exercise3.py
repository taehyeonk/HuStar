import RPi.GPIO as GPIO
from time import sleep
import GPIO_EX

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

LED_1_status = False
LED_2_status = False
LED_3_status = False
LED_4_status = False

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
    
    # if runningStep == 1:
    #     if keyData == -1:
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

def controlLed(keyData):
    global LED_1_status
    global LED_2_status
    global LED_3_status
    global LED_4_status

    if(keyData == 1):
        if(LED_1_status == False):
            GPIO.output(LED_1, GPIO.HIGH)
            LED_1_status = True
        else:
            GPIO.output(LED_1, GPIO.LOW)
            LED_1_status = False
    elif(keyData == 2):
        if(LED_2_status == False):
            GPIO.output(LED_2, GPIO.HIGH)
            LED_2_status = True
        else:
            GPIO.output(LED_2, GPIO.LOW)
            LED_2_status = False
    elif(keyData == 3):
        if(LED_3_status == False):
            GPIO.output(LED_3, GPIO.HIGH)
            LED_3_status = True
        else:
            GPIO.output(LED_3, GPIO.LOW)
            LED_3_status = False
    elif(keyData == 4):
        if(LED_4_status == False):
            GPIO.output(LED_4, GPIO.HIGH)
            LED_4_status = True
        else:
            GPIO.output(LED_4, GPIO.LOW)
            LED_4_status = False
    elif(not keyData == -1):
        GPIO.output(LED_1, GPIO.LOW)
        GPIO.output(LED_2, GPIO.LOW)
        GPIO.output(LED_3, GPIO.LOW)
        GPIO.output(LED_4, GPIO.LOW)
        LED_1_status = LED_2_status = LED_3_status = LED_4_status = False

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LED_1, GPIO.OUT, initial=False)
    GPIO.setup(LED_2, GPIO.OUT, initial=False)
    GPIO.setup(LED_3, GPIO.OUT, initial=False)
    GPIO.setup(LED_4, GPIO.OUT, initial=False)

    initKeypad()
    print("setup keypad pin")
    try:
        while True:
            keyData = readKeypad()
            controlLed(keyData)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()