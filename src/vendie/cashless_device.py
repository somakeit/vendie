import time
from typing import override, overload

from serial import Serial
from enum import StrEnum

from vendie.vending_machine.commands import VendingMachineCommand, VMCCommand
from vendie.vending_machine.responses import VendingMachineResponse, VMCResponse


class State(StrEnum):
    INACTIVE = 'inactive'
    DISABLED = 'disabled'
    ENABLED = 'enabled'
    SESSION_IDLE = 'session_idle'
    VEND = 'vend'


class CashlessDevice:
    def __init__(self, vending_machine: Serial, card_reader: Serial):
        self.vending_machine: Serial = vending_machine
        self.card_reader: Serial = card_reader

        self.initial_state: State = State.INACTIVE
        self.current_state: State = self.initial_state

        self.current_card: str | None = None

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
            raise ValueError(f"No handler for state {self.current_state}")
        return func()

    def handle_inactive_state(self):
        self.vending_machine.flush()
        self.send_vending_machine_data(VendingMachineResponse(VMCResponse.RESET, data='00'))
        time.sleep(1)

        setup_config_data: str | None = None
        setup_prices_data: str | None = None

        while None in (setup_config_data, setup_prices_data):
            command = VendingMachineCommand.from_ascii_data(self.get_vending_machine_data())

            if command.command is VMCCommand.SETUP:
                if command.data.startswith('00'):
                    setup_config_data = command.data
                    print(f"{setup_config_data=}")
                elif command.data.startswith('01'):
                    setup_prices_data = command.data
                    print(f"{setup_prices_data=}")

        return State.DISABLED

    def handle_disabled_state(self):
        while True:
            command = VendingMachineCommand.from_ascii_data(self.get_vending_machine_data())
            if command.command == VMCCommand.READER and command.data.startswith('01'):
                return State.ENABLED
            elif command.command == VMCCommand.EXPANSION and command.data.startswith('00'):
                self.send_vending_machine_data(VendingMachineResponse(VMCResponse.PERIPHERAL_ID, data=command.data[2:]))
            elif command.command == VMCCommand.RESET:
                return State.INACTIVE

    def handle_enabled_state(self):
        print("Waiting for a member fob...")
        self.current_card = None
        while True:
            member_card = self.get_card_reader_data(once=True)
            raw_command = self.get_vending_machine_data(once=True)
            if member_card is None and raw_command is None:
                continue

            if member_card:
                print(f"Member fob read: {member_card}")
                self.current_card = member_card
                return State.SESSION_IDLE

            if raw_command:
                command = VendingMachineCommand.from_ascii_data(raw_command)
                print(repr(command))
                if command.command == VMCCommand.READER and command.data.startswith('00'):
                    return State.DISABLED
                elif command.command == VMCCommand.RESET:
                    return State.INACTIVE

    def handle_session_idle_state(self):
        self.send_vending_machine_data(VendingMachineResponse(VMCResponse.BEGIN_SESSION, data='FFFF'))
        while True:
            command = VendingMachineCommand.from_ascii_data(self.get_vending_machine_data())
            print(repr(command))
            if command.command == VMCCommand.RESET:
                return State.INACTIVE
            elif command.command == VMCCommand.VEND and command.data.startswith('00'):
                price = command.data[2:6]
                print(f"{price=}")
                print(f"{int(price, 16)=}")

                item = command.data[6:10]
                print(f"{item=}")
                print(f"{int(item, 16)=}")

                self.send_vending_machine_data(VendingMachineResponse(VMCResponse.VEND_APPROVED))


    def send_vending_machine_data(self, data: VendingMachineResponse):
        print(f"Sent: {data}")
        self.vending_machine.write(bytes.fromhex(str(data)))
        if data.response in (VMCResponse.RESET,):
            self.get_vending_machine_data()

    def get_vending_machine_data(self, once: bool = False) -> str | None:
        while (not (data := self.vending_machine.read_until(b'\x03').decode()[1:-1])) or data == '00':
            if once:
                return None
        print(f"Received: {data}")
        return data

    def get_card_reader_data(self, once: bool = False) -> str | None:
        while not (data := self.card_reader.read_until(b'\x03').decode()[1:-1]):
            if once:
                return None
        return data
