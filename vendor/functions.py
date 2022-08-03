import serial
from serial.tools import list_ports


def get_serial_device_from_description(description: str, baud_rate: int = 9600, timeout: int | float = 10) -> serial.Serial:
    device = next((port.device for port in list(list_ports.comports()) if port.description == description), None)
    if device is not None:
        return serial.Serial(device, baud_rate, timeout=timeout)


def flush_serial(device: serial.Serial):
    device.flush()
    device.flushInput()
    device.flushOutput()


if __name__ == '__main__':
    print([port.description for port in list(list_ports.comports())])
    test = get_serial_device_from_description('test')
    print(test)
