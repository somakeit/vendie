from serial import Serial
from serial.serialutil import SerialException

from vendie.cashless_device import CashlessDevice
from vendie.config import VENDING_MACHINE_MDB_SERIAL_PORT, CARD_READER_SERIAL_PORT

def get_serial(port: str, **kwargs) -> Serial | None:
    try:
        serial = Serial(port, **kwargs)
    except SerialException:
        serial = None
    return serial

def main():
    vending_machine: Serial | None = get_serial(VENDING_MACHINE_MDB_SERIAL_PORT, timeout=10)
    card_reader: Serial | None = get_serial(CARD_READER_SERIAL_PORT, timeout=10)

    assert vending_machine is not None, "Failed to connect to vending machine"
    assert card_reader is not None, "Failed to connect to card reader"

    state_machine = CashlessDevice(vending_machine, card_reader)
    state_machine.start()




if __name__ == '__main__':
    main()