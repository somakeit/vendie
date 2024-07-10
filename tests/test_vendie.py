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
            return_serials[index] = Serial(port.device, 9600, timeout=10)

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

    while True:
        data = vending_mdb.read_until(b'\x03')

        if not data:
            continue

        _, *command_bytes, checksum = data
        command = bytes(command_bytes).decode('ascii')

        print(command)


