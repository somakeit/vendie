import serial
from serial.tools import list_ports


def get_serial_device_from_description(description: str, baudrate: int = 9600, timeout: int = 10) -> serial.Serial:
    device = next((port.device for port in list(list_ports.comports()) if port.description == description), None)
    if device is None:
        return None
    return serial.Serial(device, baudrate, timeout=timeout)


if __name__ == '__main__':
    print([port.description for port in list(list_ports.comports())])
    test = get_serial_device_from_description('test')
    print(test)
