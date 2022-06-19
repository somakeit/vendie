from enum import Enum
from abc import ABC, abstractmethod


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

    def run(self) -> State:
        print("Entering Inactive")
        return State.DISABLED


class Disabled(BaseState):
    name = State.DISABLED

    def run(self) -> State:
        print("Entering Disabled")


class Enabled(BaseState):
    name = State.ENABLED

    def run(self) -> State:
        pass


class SessionIdle(BaseState):
    name = State.SESSION_IDLE

    def run(self) -> State:
        pass


class Vend(BaseState):
    name = State.VEND

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

    print(State.get_class(State.INACTIVE))
