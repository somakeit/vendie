from enum import StrEnum
from idlelib.configdialog import tracers
from types import new_class

from serial import Serial

from vendie import data_with_checksum
from vendie.commands import VMCCommand
from vendie.responses import VMCResponse
from vendie.config import DEBUG, MAXIMUM_CREDIT


class State(StrEnum):
    INACTIVE = 'inactive'
    DISABLED = 'disabled'
    ENABLED = 'enabled'
    SESSION_IDLE = 'session_idle'
    VEND = 'vend'

    @property
    def index(self):
        return list(State).index(self)


class CashlessDevice:
    def __init__(self, vending_machine: Serial, card_reader: Serial):
        self.vending_machine: Serial = vending_machine
        self.card_reader: Serial = card_reader

        self.initial_state: State = State.INACTIVE
        self.current_state: State = self.initial_state

        self.member_card: str | None = None
        self.vend_request: str | None = None

    def start(self):
        while True:
            print(f"New State: {self.current_state}")
            new_state = self.run_current_state()
            if new_state is None:
                break

            self.current_state = new_state

    def run_current_state(self):
        func_name = f"handle_{self.current_state.value.lower()}_state"
        func = getattr(self, func_name, None)
        if func is None:
            raise ValueError(f"No handler for state {repr(self.current_state)}")
        return func()

    def handle_inactive_state(self):
        self.vending_machine.flush()

        self.send_vending_machine_data(data_with_checksum(VMCResponse.SESSION_CANCEL_REQUEST))
        self.get_vending_machine_data(once=True)

        self.send_vending_machine_data(data_with_checksum(VMCResponse.RESET + '00'))

        setup_config_data: str | None = None
        setup_prices_data: str | None = None

        while None in (setup_config_data, setup_prices_data):
            command = self.get_vending_machine_data()

            if command.startswith(VMCCommand.SETUP):
                data = command.replace(VMCCommand.SETUP, '')
                if data.startswith('00'):
                    setup_config_data = data
                    print(f"{setup_config_data=}")
                elif data.startswith('01'):
                    setup_prices_data = data
                    print(f"{setup_prices_data=}")

        return State.DISABLED

    def handle_disabled_state(self):
        while True:
            command = self.get_vending_machine_data()
            if command.startswith(VMCCommand.RESET):
                return State.INACTIVE

            elif command.startswith(VMCCommand.READER):
                data = command.replace(VMCCommand.READER, '')
                if data.startswith('01'):
                    return State.ENABLED
            elif command.startswith(VMCCommand.EXPANSION):
                pass
            else:
                self.send_vending_machine_data(data_with_checksum(VMCResponse.COMMAND_OUT_OF_SEQUENCE + '02'))

    def handle_enabled_state(self):
        self.member_card = None
        print("Waiting for member card...")
        while True:
            command = self.get_vending_machine_data(once=True)
            if command:
                if command.startswith(VMCCommand.RESET):
                    return State.INACTIVE

                if command.startswith(VMCCommand.READER):
                    data = command.replace(VMCCommand.READER, '')
                    if data.startswith('00'):
                        return State.DISABLED

            member_card = self.get_card_reader_data(once=True)
            if member_card:
                self.member_card = member_card
                self.send_vending_machine_data(data_with_checksum(VMCResponse.BEGIN_SESSION + MAXIMUM_CREDIT))
                return State.SESSION_IDLE

    def handle_session_idle_state(self):
        self.vend_request = None
        while True:
            command = self.get_vending_machine_data()
            if command.startswith(VMCCommand.VEND):
                data = command.strip(VMCCommand.VEND)
                if data.startswith('04'):
                    self.send_vending_machine_data(data_with_checksum(VMCResponse.END_SESSION))
                    return State.DISABLED
                if data.startswith('00'):
                    self.vend_request = command
                    return State.VEND

    def handle_vend_state(self):
        print(f"{self.member_card = }")

        price = int(self.vend_request[5:8], 16)
        item = int(self.vend_request[9:12], 16)

        print(f"£{price/100:.2f}")
        print(f"Slot {slot_to_lettered(item)}")

        self.send_vending_machine_data(data_with_checksum(VMCResponse.VEND_APPROVED))
        return State.SESSION_IDLE

    def send_vending_machine_data(self, data: str):
        DEBUG and print(f"Sent: {data}")
        self.vending_machine.write(bytes.fromhex(data))
        if any(data.startswith(resp) for resp in (VMCResponse.RESET,)):
            self.get_vending_machine_data()

    def get_vending_machine_data(self, /, once: bool = False) -> str | None:
        while (not (data := self.vending_machine.read_until(b'\x03').decode()[1:-1])) or data == '00':
            if once:
                return None
        DEBUG and print(f"Received: {data}")
        return data

    def get_card_reader_data(self, /, once: bool = False) -> str | None:
        while not (data := self.card_reader.read_until(b'\x03').decode()[1:-1]):
            if once:
                return None
        return data.strip()

def slot_to_lettered(slot_number: int) -> str:
    # Determine the letter (row) using integer division
    letter = chr(ord('A') + slot_number // 8)

    # Determine the number (column) using modulo
    number = (slot_number % 8) + 1

    return f"{letter}{number}"