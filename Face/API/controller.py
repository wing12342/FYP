import time
import serial

ser = serial.Serial('COM4', 115200, timeout=0.050)


def door(state):
    b = True
    while b:
        print(state)
        ser.write(str(state).encode())
        time.sleep(3)
        b = False