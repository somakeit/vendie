from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


class State(Enum):
    INACTIVE = 1
    DISABLED = 2
    ENABLED = 3
    SESSION_IDLE = 4
    VEND = 5

    


class BaseState(ABC):
    name: State

    @abstractmethod
    def run(self):
        pass


class Inactive(BaseState):
    name = State.INACTIVE

    def run(self):
        pass


class Disabled(BaseState):
    name = State.DISABLED

    def run(self):
        pass


class Enabled(BaseState):
    name = State.ENABLED

    def run(self):
        pass


class SessionIdle(BaseState):
    name = State.SESSION_IDLE

    def run(self):
        pass


class Vend(BaseState):
    name = State.VEND

    def run(self):
        pass


if __name__ == '__main__':
    print([state for state in list(State)])
