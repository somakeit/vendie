from .states import State, build_state_map, BaseState
from .config import PORT_DESCRIPTIONS
from .functions import get_serial_device_from_description
import serial


class CashlessDevice:
    def __init__(self):
        self.current_state: State = State.INACTIVE
        self._state_map: dict[State:BaseState] = build_state_map(self)
        self.card_reader = None
        self.vendor = None

        self._init_devices()

    def _init_devices(self):
        self.card_reader = get_serial_device_from_description(PORT_DESCRIPTIONS['card_reader'])
        self.vendor = get_serial_device_from_description(PORT_DESCRIPTIONS['vendor'])

        print(f'Card Reader ({PORT_DESCRIPTIONS["card_reader"]})'
              f' {"found" if self.card_reader is not None else "not found!"}')
        print(f'Card Reader ({PORT_DESCRIPTIONS["vendor"]})'
              f' {"found" if self.card_reader is not None else "not found!"}')




    def start(self):
        while True:
            next_state = self._state_map[self.current_state].run()

            if next_state is None:
                break

            self.set_state(next_state)

    def set_state(self, state: State):
        self.current_state = state
