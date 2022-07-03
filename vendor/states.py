from enum import Enum
from abc import ABC, abstractmethod
from .responses import Response
from .functions import flush_serial
from .commands import Command
from .config import ENCODING, DEBUG, SHOW_ENTER_EXIT


def _method_enter_exit(f):
    def wrapper(*args, **kwargs):
        if SHOW_ENTER_EXIT:
            print(f'Entering the {args[0].__class__.__name__} state')
        func = f(*args, *kwargs)
        if SHOW_ENTER_EXIT:
            print(f'Exiting the {args[0].__class__.__name__} state')
        return func
    return wrapper


class State(Enum):
    INACTIVE = 1
    DISABLED = 2
    ENABLED = 3
    SESSION_IDLE = 4
    VEND = 5


class BaseState(ABC):
    name: State

    def __init__(self, state_machine):
        self._state_machine = state_machine
        self.card_reader = state_machine.card_reader
        self.vendor = state_machine.vendor

    @abstractmethod
    def run(self) -> State:
        pass


class Inactive(BaseState):
    name = State.INACTIVE

    @_method_enter_exit
    def run(self) -> State:
        flush_serial(self.vendor)
        flush_serial(self.card_reader)

        # Send reset command
        self._state_machine.send_response(Response.JUST_RESET)

        config_data_received = False
        config_prices_received = False
        read_count = 0

        # It turns out that the responses to the SETUP commands are not needed
        while not (config_data_received and config_prices_received):
            command_str = self._state_machine.read_command()
            command = Command.find_command(command_str)
            read_count += 1
            if DEBUG:
                print(f'{command_str=}')
                print(f'{command=}')

            match command:
                case Command.SETUP_CONFIG_DATA:
                    config_data_received = True
                case Command.SETUP_MAX_MIN_PRICES:
                    config_prices_received = True
                case _:
                    if read_count > 10:
                        print('Setup not received! Attempting reset!')
                        return State.INACTIVE
                # case _:
                #     self._state_machine.send_response(Response.CMD_OUT_OF_SEQUENCE)

        return State.DISABLED


class Disabled(BaseState):
    name = State.DISABLED

    @_method_enter_exit
    def run(self) -> State:
        command = None
        while True:
            command_str = self._state_machine.read_command()
            command = Command.find_command(command_str)
            if DEBUG:
                print(f'{command_str=}')
                print(f'{command=}')

            match command:
                case Command.READER_ENABLE:
                    break
                case Command.RESET:
                    return State.INACTIVE
                case _:
                    self._state_machine.send_response(Response.CMD_OUT_OF_SEQUENCE)

        return State.ENABLED


class Enabled(BaseState):
    name = State.ENABLED

    @_method_enter_exit
    def run(self) -> State:
        print('Waiting for card...')
        while True:
            flush_serial(self.card_reader)
            UID = self.card_reader.read().decode(ENCODING)

            command_str = self._state_machine.read_command()
            command = Command.find_command(command_str)
            if DEBUG:
                print(f'{command_str=}')
                print(f'{command=}')
            if UID != '':
                print(f'{UID=}')
                continue

            match command:
                case Command.RESET:
                    return State.INACTIVE
                case Command.READER_DISABLE:
                    return State.DISABLED


class SessionIdle(BaseState):
    name = State.SESSION_IDLE

    @_method_enter_exit
    def run(self) -> State:
        pass


class Vend(BaseState):
    name = State.VEND

    @_method_enter_exit
    def run(self) -> State:
        pass


def build_state_map(state_machine):
    """ Using a dictionary comprehension to condense a dictionary-building for-loop to 1 line in a pythonic way """
    return {_class.name: _class(state_machine) for _class in BaseState.__subclasses__() if _class.name in list(State)}


if __name__ == '__main__':
    print([state for state in list(State)])
