from serial import Serial
from enum import StrEnum, auto

from vendie.vending_machine_commands import VendingMachineCommand


class State(StrEnum):
    INACTIVE = 'inactive'
    DISABLED = 'disabled'
    ENABLED = 'enabled'
    SESSION_IDLE = 'session idle'
    VEND = 'vend'


class CashlessDevice:
    def __init__(self, vending_machine: Serial, card_reader: Serial):
        self.vending_machine: Serial = vending_machine
        self.card_reader: Serial = card_reader

        self.initial_state: State = State.INACTIVE
        self.current_state: State = self.initial_state

    def start(self):
        while True:
            new_state = self.run_current_state()
            if new_state is None:
                break

            self.current_state = new_state

    def run_current_state(self):
        func_name = f"handle_{self.current_state.value.lower()}_state"
        func = getattr(self, func_name, None)
        if func is None:
            raise ValueError(f"No handler for state {self.current_state}")
        return func()

    def handle_inactive_state(self):
        self.send_vending_machine_data('00')
        while True:
            command = VendingMachineCommand.from_ascii_data(self.get_vending_machine_data())
            print(command)

    def send_vending_machine_data(self, data: str):
        self.vending_machine.write(bytes.fromhex(data))
        self.get_vending_machine_data()

    def get_vending_machine_data(self) -> str:
        while not (data := self.vending_machine.read_until(b'\x03').decode()[1:-1]):
            pass
        return data
