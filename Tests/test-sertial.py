import serial

from serial.tools import list_ports

for port in list(list_ports.comports()):
    print(port.__dict__)
    break