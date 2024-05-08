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
        self.api = state_machine.api

    @abstractmethod
    def run(self) -> State:
        pass


class Inactive(BaseState):
    name = State.INACTIVE

    @_method_enter_exit
    def run(self) -> State:
        flush_serial(self.vendor)
        # flush_serial(self.card_reader)

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
                print(f'{read_count=}')

            match command:
                case Command.SETUP_CONFIG_DATA:
                    config_data_received = True
                case Command.SETUP_MAX_MIN_PRICES:
                    config_prices_received = True
                case Command.RESET:
                    self._state_machine.send_response(Response.ACKNOWLEDGE)
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
                    self._state_machine.send_response(Response.ACKNOWLEDGE)
                    break
                case Command.EXPANSION_REQUEST_ID:
                    pass
                case Command.RESET:
                    self._state_machine.send_response(Response.ACKNOWLEDGE)
                    return State.INACTIVE
                case Command.READER_DISABLE:
                    self._state_machine.send_response(Response.ACKNOWLEDGE)
                    return State.DISABLED

        return State.ENABLED


class Enabled(BaseState):
    name = State.ENABLED

    @_method_enter_exit
    def run(self) -> State:
        print('Waiting for card...')
        valid_card = False
        while True:
            # flush_serial(self.card_reader)
            uid_raw = self.card_reader.read_until(b'\0d\0a', size=10)
            UID = uid_raw.decode(ENCODING)[:-2]

            # If we have a card read...
            if UID != '':
                print(f'Card {UID} read!')
                # Validate Card using API here
                api_data = {'card_uid': UID}
                if self.api.validate_card(data=api_data):
                    print("We have a winner :D")
                    self._state_machine.send_response(Response.BEGIN_SESSION)
                    return State.SESSION_IDLE
                else:
                    print('Invalid card!!!')
                    valid_card = False
            else:
                command_str = self._state_machine.read_command()
                command = Command.find_command(command_str)
                # if DEBUG:
                print(f'{command_str=}')
                print(f'{command=}')

                match command:
                    case Command.POLL if valid_card:
                        self._state_machine.send_response(Response.BEGIN_SESSION)
                        return State.SESSION_IDLE
                    case Command.RESET:
                        return State.INACTIVE
                    case Command.READER_DISABLE:
                        return State.DISABLED


class SessionIdle(BaseState):
    name = State.SESSION_IDLE

    @_method_enter_exit
    def run(self) -> State:
        while True:
            command_str = self._state_machine.read_command()
            command = Command.find_command(command_str)
            # if DEBUG:
            print(f'{command_str=}')
            print(f'{command=}')

            # command_str = self._state_machine.vendor.read(24)
            # command = Command.find_command(command_str)
            # # if DEBUG:
            # print(f'{command_str=}')
            # print(f'{command=}')

            match command:
                case Command.VEND_SESSION_COMPLETE:
                    self._state_machine.send_response(Response.END_SESSION)
                    return State.DISABLED
                case Command.EXPANSION_REQUEST_ID:
                    self._state_machine.send_response(Response.PERIPHERAL_ID)

            self._state_machine.send_response(Response.BEGIN_SESSION)


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
