from enum import Enum
from abc import ABC, abstractmethod


def _method_enter_exit(f):
    def wrapper(*args, **kwargs):
        print(f'Entering {args[0].__class__.__name__}')
        print(f'Exiting {args[0].__class__.__name__}')
        return f(*args, *kwargs)
    return wrapper


class State(Enum):
    INACTIVE = 1
    DISABLED = 2
    ENABLED = 3
    SESSION_IDLE = 4
    VEND = 5


class BaseState(ABC):
    name: State

    @abstractmethod
    def run(self) -> State:
        pass


class Inactive(BaseState):
    name = State.INACTIVE

    @_method_enter_exit
    def run(self) -> State:
        return State.DISABLED


class Disabled(BaseState):
    name = State.DISABLED

    @_method_enter_exit
    def run(self) -> State:
        pass


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


def build_state_map():
    state_map = {}
    for _class in BaseState.__subclasses__():
        if _class.name in list(State):
            state_map[_class.name] = _class()

    return state_map


if __name__ == '__main__':
    print([state for state in list(State)])
