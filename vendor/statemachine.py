from .responses import Response
from .states import State, build_state_map, BaseState
from .config import PORT_DESCRIPTIONS, ENCODING, API_TO_USE
from .functions import get_serial_device_from_description
from .commands import Command

import serial


class CashlessDevice:
    def __init__(self):
        self.current_state: State = State.INACTIVE
        self.card_reader = None
        self.vendor = None
        self.api = API_TO_USE()

        self._init_devices()

        self._state_map: dict[State:BaseState] = build_state_map(self)

    def _init_devices(self):
        self.card_reader = get_serial_device_from_description(PORT_DESCRIPTIONS['card_reader'])
        self.vendor = get_serial_device_from_description(PORT_DESCRIPTIONS['vendor'], timeout=4)

        print(f'Card Reader ({PORT_DESCRIPTIONS["card_reader"]})'
              f' {"found" if self.card_reader is not None else "not found!"}')
        print(f'Vendor ({PORT_DESCRIPTIONS["vendor"]})'
              f' {"found" if self.vendor is not None else "not found!"}')

    def start(self):
        if None in (self.card_reader, self.vendor):
            print('Not all devices found... cannot start')
            return

        while True:
            next_state = self._state_map[self.current_state].run()

            if next_state is None:
                break

            self.set_state(next_state)

    def set_state(self, state: State):
        self.current_state = state

    def read_command(self) -> Command:
        """Reads until Hex value 03 which signifies end of command"""
        command = self.vendor.read_until(b'\x03').decode(ENCODING)
        print(f'{command=}')
        command = command[1:-1]
        return command

    def send_response(self, response: Response, data: str = ''):
        self.vendor.write(bytes.fromhex(response.value + data + Response.ACKNOWLEDGE.value))


