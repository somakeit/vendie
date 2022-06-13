from dataclasses import dataclass


class list_ports:
    """ Class to replicate serial.tools.list_tools"""
    @classmethod
    def comports(cls):
        return port_array


@dataclass
class ListPortInfo:
    device: str
    description: str


port_array = [
    ListPortInfo("USB2", "USB2.0-Serial"),
    ListPortInfo("FT232R", "FT232R USB UART - FT232R USB UART")
]
