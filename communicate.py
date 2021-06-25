import os
import time
import serial

def sendCommand(command):
    os.system('screen -S pico -X stuff \'' + command + '\\r\'')

def openConnection():
    os.system('screen -d -m -S pico /dev/tty.usbmodem* 9600')
    sendCommand('import usb_hid\\r')
    sendCommand('from adafruit_hid.mouse import Mouse\\r')
    sendCommand('mouse = Mouse(usb_hid.devices)\\r')
    print('initialized')

def closeConnection():
    os.system('screen -XS pico quit')
    print('uninitialized')

def moveMouse(x, y):
    print(str(x) + ' ' + str(y))
    sendCommand('mouse.move(x=' + str(x) + ',y=' + str(y) + ')')

def getRelativeCoords(curx, cury, x, y):
    relx = x - curx
    rely = y - cury

    return relx, rely

def sendSerialCommand(command, ser):
    command = command + '\r'
    command = str.encode(command)
    ser.write(command)     # write a string

def openSerialConnection():
    ser = serial.Serial('/dev/tty.usbmodem1112301', 115200)  # open serial port
    return ser

def closeSerialConnection(ser):
    ser.close()

def serialMoveMouse(ser, x, y):
    if x == 0:
        command = "mouse.move(y=" + str(y) + ")\r"
    else:
        if y == 0:
            command = "mouse.move(x=" + str(x) + ")\r"
        else:
            command = "mouse.move(x=" + str(x) + ", y=" + str(y) + ")\r"
    command = str.encode(command)
    ser.write(command)

def getCoordinatePlane(x, y, dimx=960, dimy=540):
    x = dimx -x
    y = dimy -y

    return x, y

