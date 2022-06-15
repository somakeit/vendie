# SoMakeIt Vending Machine - Cashless Payments Code
# Author:   Sam Cork
# Date:     June 2022
#
# More info about cashless payments: https://wiki.nottinghack.org.uk/wiki/Vending_Machine/Cashless_Device
import serial
from serial.tools import list_ports

card_reader = None
vendor_serial = None


def connect_to_vendor() -> (serial.Serial, serial.Serial):
    card_reader = None
    vendor_serial = None
    for port in list(list_ports.comports()):
        print('Found: ', port.description, ' - ', port.device)
        if port.description == "USB2.0-Serial":
            card_reader = serial.Serial(port.device, 9600, timeout=10)
            print('Assigned Card Reader')

        if port.description == "FT232R USB UART - FT232R USB UART":
            vendor_serial = serial.Serial(port.device, 9600, timeout=10)
            print('Assigned Vendor')

    return card_reader, vendor_serial


if __name__ == '__main__':
    card_reader, vendor_serial = connect_to_vendor()


