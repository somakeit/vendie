from serial import Serial
from serial.tools import list_ports
from os import PathLike


class SerialFactory:
    @staticmethod
    def _get_serial_from_port_description(description: str, baudrate: int = 9600, timeout: int | float = 10) -> Serial | None:
        for port in list(list_ports.comports()):
            if port.description == description:
                return Serial(port.device, baudrate=baudrate, timeout=timeout)

        return None

    @staticmethod
    def _get_serial_from_port(port: PathLike, baudrate: int = 9600, timeout: int | float = 10) -> Serial | None:
        try:
            return Serial(port, baudrate=baudrate, timeout=timeout)
        except Exception as e:
            return None

    @staticmethod
    def get_serial_device(port: PathLike = None, description: str = None, baudrate: int = 9600, timeout: int | float = 10) -> Serial | None:
        device = None

        # Try Serial port if passed in
        if port:
            device =  SerialFactory._get_serial_from_port(port, baudrate=baudrate, timeout=timeout)

        # Otherwise try by description
        if not device and description:
            device = SerialFactory._get_serial_from_port_description(description, baudrate=baudrate, timeout=timeout)

        return device


