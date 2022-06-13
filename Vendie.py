# SoMakeIt Vending Machine - Cashless Payments Code
# Author:   Sam Cork
# Date:     June 2022
#
# More info about cashless payments: https://wiki.nottinghack.org.uk/wiki/Vending_Machine/Cashless_Device

from vendor import State
from spoofer import serial
from spoofer.serial.tools import list_ports


for port in list(list_ports.comports()):
    print('Found: ', port.description, ' - ', port.device)
    if port.description == "USB2.0-Serial":
        cardRdr = serial.Serial(port.device, 9600, timeout=10)
        print('Assigned Card Reader')

    if port.description == "FT232R USB UART - FT232R USB UART":
        vendSer = serial.Serial(port.device, 9600, timeout=10)
        print('Assigned Vender')

if 'vendSer' not in locals():
    print('Vender not found')
    quit()
if 'cardRdr' not in locals():
    print('Cardreader not found')
    quit()


print(cardRdr.read(10))