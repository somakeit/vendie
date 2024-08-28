from serial import Serial
from serial.tools import list_ports
from contextlib import suppress

CARD_READER_SERIAL_DESCRIPTION = "USB2.0-Serial"
VENDING_MACHINE_MDB_DESCRIPTION = "FT232R USB UART - FT232R USB UART"


def connect_to_serial_devices(*descriptions: str) -> list[Serial | None]:
    return_serials: list = [None] * len(descriptions)

    for port in list(list_ports.comports()):
        with suppress(ValueError):
            index = descriptions.index(port.description)
            return_serials[index] = Serial(port.device, 9600, timeout=10, stopbits=1)

            print(f"Found '{port.description}' on {port.device}")

    return return_serials


if __name__ == '__main__':
    vending_mdb, card_reader = connect_to_serial_devices(VENDING_MACHINE_MDB_DESCRIPTION,
                                                         CARD_READER_SERIAL_DESCRIPTION)

    if None in (vending_mdb, card_reader):
        quit()

    card_reader: Serial
    vending_mdb: Serial

    card_reader.flush()
    vending_mdb.flush()

    vending_mdb.write(bytes.fromhex('00'))
    vending_mdb.write(bytes.fromhex('00'))
    vending_mdb.write(bytes.fromhex('00'))

    while True:
        data = vending_mdb.read_until(b'\x03')

        if not data:
            continue

        _, *command_bytes, checksum = data
        command = bytes(command_bytes).decode('ascii')

        print(command)
        if command.startswith('1401'):
            while True:
                fob = card_reader.read_until(b'\r\n', size=10)
                print(f"{fob=}")
                if fob:
                    vending_mdb.write(bytes.fromhex('03FFFF01'))
                    break
        if command.startswith('1300'):
            price = command[4:8]
            print(f"{price=}")
            print(f"{int(price, 16)=}")

            item = command[8:-2]
            print(f"{item=}")
            print(f"{int(item, 16)=}")
            msg = '0500' + price
            msg_bytes = bytes.fromhex(msg)

            vending_mdb.write(msg_bytes)

            data = vending_mdb.read_until(b'\x03')

            _, *command_bytes, checksum = data
            checksum_calc = bytes(command_bytes).decode('ascii')


            vending_mdb.write(bytes.fromhex(msg + checksum_calc))
        if command.startswith('1304'):
            vending_mdb.write(bytes.fromhex('0707'))






