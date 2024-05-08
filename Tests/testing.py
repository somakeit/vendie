#!/usr/bin/python3

import serial
import string
import requests
import datetime
from serial.tools import list_ports

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

vendSer.flush()
cardRdr.flush()

def checksum(byte_str):
    total=0
    for i in range(0, len(byte_str), 2):
        hex_val = byte_str[i:i+2]
        dec_val = int(hex_val, 16)
        total += dec_val
    return total & 0xFF


vendSer.write(bytes.fromhex('00'))
while True:

    data = vendSer.read_until(bytes.fromhex('03'))
    print(data)
    data =  data[1:-1]
    print(f'{data=}')
    check_data, check_sum = data[:-2], int(data[-2:], 16)
    print(f'{checksum(check_data)=}')
    print(f'{check_sum=}')
    assert checksum(check_data) == check_sum

    match data:
        # Reader Enable
        case b'140115':
            # ACK
            vendSer.write(bytes.fromhex('00'))