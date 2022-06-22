import serial
from serial.tools import list_ports


def get_serial_device_from_description(description: str):
    return next((port.description for port in list(list_ports.comports()) if port.description == description), None)


if __name__ == '__main__':
    test = serial.Serial(get_serial_device_from_description('test'), 9600, 10)
    print(test)
