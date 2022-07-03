from enum import Enum
from abc import ABC, abstractmethod
from .responses import Response
from .functions import flush_serial
from .commands import Command
from .config import ENCODING


def _method_enter_exit(f):
    def wrapper(*args, **kwargs):
        print(f'Entering the {args[0].__class__.__name__} state')
        func = f(*args, *kwargs)
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
        # self.vendor.write(bytes.fromhex(Response.JUST_RESET.value))

        while True:
            try:
                command_str = self._state_machine.read_command()
                # command = self.vendor.read_until(b'\x03').decode(ENCODING)
                print(command_str)
                try:
                    print(Command(command_str))
                except ValueError:
                    print('Unknown Command')
            except KeyboardInterrupt:
                break

        return State.DISABLED


class Disabled(BaseState):
    name = State.DISABLED

    @_method_enter_exit
    def run(self) -> State:
        return State.ENABLED


class Enabled(BaseState):
    name = State.ENABLED

    @_method_enter_exit
    def run(self) -> State:
        pass


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
