from vendie.states import State
from vendie.serial_factory import SerialFactory
from vendie.config import RFID_SERIAL_PORT, MDB_SERIAL_PORT, MDB_SERIAL_PORT_DESCRIPTION, RFID_SERIAL_PORT_DESCRIPTION
from serial import Serial


class CashlessDevice:
    def __init__(self):
        self.current_state: State | None = None
        self.card_reader: Serial | None = SerialFactory.get_serial_device(port=RFID_SERIAL_PORT, description=RFID_SERIAL_PORT_DESCRIPTION)
        self.vending_machine: Serial | None = SerialFactory.get_serial_device(port=MDB_SERIAL_PORT, description=MDB_SERIAL_PORT_DESCRIPTION)

    def check_connections(self) -> bool:
        if self.card_reader is None:
            print('Card reader not found')
        else:
            print(f'Card reader found at port {self.card_reader.port}')

        if self.vending_machine is None:
            print('Vending machine not found')
        else:
            print(f'Vending machine found at port {self.vending_machine.port}')

        return None not in (self.card_reader, self.vending_machine)

    def start(self):
        if not self.check_connections():
            return

        while True:
            pass

