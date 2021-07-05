import sys
import time
import smbus

def readReg(address):
    cmd_00h = bus.read_byte_data(address, 0x00)
    print("cmd_00h = %02X\n"%cmd_00h)
    cmd_01h = bus.read_byte_data(address, 0x01)
    print("cmd_01h = %02X\n"%cmd_01h)
    cmd_02h = bus.read_byte_data(address, 0x02)
    print("cmd_02h = %02X\n"%cmd_02h)
    cmd_03h = bus.read_byte_data(address, 0x03)
    print("cmd_03h = %02X\n"%cmd_03h)
    cmd_40h = bus.read_byte_data(address, 0x40)
    print("cmd_40h = %02X\n"%cmd_40h)
    cmd_41h = bus.read_byte_data(address, 0x41)
    print("cmd_41h = %02X\n"%cmd_41h)
    cmd_42h = bus.read_byte_data(address, 0x42)
    print("cmd_42h = %02X\n"%cmd_42h)
    cmd_43h = bus.read_byte_data(address, 0x43)
    print("cmd_43h = %02X\n"%cmd_43h)
    cmd_44h = bus.read_byte_data(address, 0x44)
    print("cmd_44h = %02X\n"%cmd_44h)
    cmd_45h = bus.read_byte_data(address, 0x45)
    print("cmd_45h = %02X\n"%cmd_45h)
    cmd_46h = bus.read_byte_data(address, 0x46)
    print("cmd_46h = %02X\n"%cmd_46h)
    cmd_4fh = bus.read_byte_data(address, 0x4f)
    print("cmd_4fh = %02X\n"%cmd_4fh)

CONFIGURATION = 0x03
I2C_ADDRESS = 0x20
IN = 1
OUT = 0
HIGH = 1
LOW = 0
bus = smbus.SMBus(1)
address = 0x20

def setup(pin, mode):
    configData = bus.read_byte_data(address, 0x03)
#    print("configData = %02X\n"%configData)
    if mode == OUT:
        configData &= ~(1<<pin)
    elif mode == IN:
        #print("pin = %02X\n"%pin)
        configData |= 1<<pin
#        print("configData = %02X\n"%configData)
    bus.write_byte_data(address, 0x03, configData)
    
    configData = bus.read_byte_data(address, 0x03)
#    print("configData = %02X\n"%configData)

def output(pin, signal):
    portData = bus.read_byte_data(address, 0x01)
#    print("portData = %02X\n"%portData)
    if signal == HIGH:
        portData |= 1<<pin
    elif signal == LOW:
        portData &= ~(1<<pin)
    bus.write_byte_data(address, 0x01, portData)

def input(pin):
    portData = bus.read_byte_data(address, 0x00)
    return ((portData>>pin)&0x01)

def main():
    setup(7, IN)
    
    try:
        while True:
#            output(1, HIGH)
#            output(7, HIGH)
#            time.sleep(3)
#            output(1, LOW)
#            output(7, LOW)
#            time.sleep(3)

            data = input(7)
            print("data = %d\n"%data)
            
    except  KeyboardInterrupt:
        bus.write_byte_data(0x20, 0x01, 0x00)
        sys.exit()

if __name__== '__main__':
    main()
