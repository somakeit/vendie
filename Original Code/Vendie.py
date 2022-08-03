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

err = 1
global ending
global UID
global price
ending = 0
cycle = 0

UID = 0
API_ENDPOINT = "https://dev.c38.co/smi/vend_api.php"


def waitForRFID():
    print('Waiting For Card')
    # wait for response
    err = 1
    UID = 0
    cardRdr.flush()
    cardRdr.flushInput()
    cardRdr.flushOutput()
    while 1:
        cardRdr.flush()
        cardRdr.flushInput()
        cardRdr.flushOutput()
        UID = cardRdr.read(10)
        if (UID.decode('UTF-8') != ""):
            print(UID)
            data = {'api_key': 'smi123', 'method': 'balance', 'card_uid': UID.decode('UTF-8')}
            # sending post request and saving response as response object
            r = requests.post(url=API_ENDPOINT, data=data)

            # extracting response text
            response = r.text
            print("Response: %s" % response)
            if (response == UID.decode('UTF-8')):
                print(datetime.datetime.now())
                print("Success: %s" % response)
                beginVend()
            else:
                print("ERROR: No Response from API")

            # waitForRFID()


def deductBal(price):
    print('Deduct from user credit')
    print(UID)
    print(price)
    data = {'api_key': 'smi123', 'method': 'vend', 'card_uid': UID, 'price': price}
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    response = r.text
    print("Response: %s" % response)


def beginVend():
    print('Begin session')
    # request controller info
    message_bytes = bytes.fromhex("00")
    vendSer.write(message_bytes)
    # wait for response
    err = 1
    while 1:
        mdb = vendSer.read_until(b'\x03')
        print(mdb)
        print(mdb.decode('ascii'))
        if mdb == b'\x02140115\x03':
            print('MATCH')
            err = 0
            break
        if mdb == b'':
            requestSessionEnd()

    if err > 0:
        vendSer.close()
        quit()

    # Next step
    startSession()


def startSession():
    print('start transaction')
    # Start transaction
    message_bytes = bytes.fromhex("03FFFF01")
    vendSer.write(message_bytes)
    # wait for user to choose item
    err = 1
    cycle = 0
    while 1:
        mdb = vendSer.read_until(b'\x03')
        print(mdb)
        price = 0
        priceInt = 0
        try:
            priceInt = str(int(mdb.decode('ascii', errors='ignore')[5:9], 16))
            price = mdb.decode('ascii', errors='ignore')[5:9]
        except:
            print(mdb.decode('ascii', errors='ignore'))

        # wait for selection
        if int(priceInt) > 0:
            print('MATCH')
            print("Price: " + str(int(price, 16)))
            # ack()
            err = 0
            break

        cycle += 1
        if cycle > 3:
            requestSessionEnd()

    if err > 0:
        requestSessionEnd()

    # Next step
    doTransaction(price)


def doTransaction(price):
    vendItem(price)


def vendItem(price):
    print('vend')
    # Start transaction
    msg = "0500" + price
    # request checksum
    message_bytes = bytes.fromhex(msg)
    vendSer.write(message_bytes)
    chk = vendSer.read(4)
    print(chk)
    print(chk[1:3])
    print(len(chk))
    msg = msg + chk[1:3].decode('utf-8')
    print(msg)
    message_bytes = bytes.fromhex(msg)
    vendSer.write(message_bytes)
    err = 1
    cycle = 0
    while 1:
        # b'\x02130417\x03'
        mdb = vendSer.read_until(b'\x03')
        print(mdb)
        print(mdb.decode('ascii'))
        if mdb == b'\x02130417\x03':
            print('Vended')
            deductBal(str(int(price, 16)))
            err = 0
            break
        if mdb == b'':
            requestSessionEnd()
    endSession()


def requestSessionEnd():
    print('Request End')
    # request controller info
    message_bytes = bytes.fromhex("0404")
    vendSer.write(message_bytes)
    # wait for response
    global ending
    while 1:
        mdb = vendSer.read_until(b'\x03')
        print(mdb)
        print(mdb.decode('ascii'))
        if mdb == b'\x02130417\x03':
            print('MATCH')
            err = 0
            break
        if mdb == b'':
            requestSessionEnd()
        ending += 1
        if ending > 3:
            # Timeout
            waitForRFID()
        # quit()
    if err > 0:
        vendSer.close()
        quit()
    # Next step
    endSession()


def endSession():
    print('End session')
    # request controller info
    message_bytes = bytes.fromhex("0707")
    vendSer.write(message_bytes)
    # wait for response
    while 1:
        mdb = vendSer.read_until(b'\x03')
        print(mdb)
        print(mdb.decode('ascii'))
        if mdb == b'\x02140115\x03':
            print('MATCH')
            waitForRFID()
            break

    if err > 0:
        vendSer.close()
        quit()


# requestSessionEnd()
# beginVend()

waitForRFID()