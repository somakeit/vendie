from enum import Enum
from abc import ABC, abstractmethod, ABCMeta


class State(Enum):
    INACTIVE = 1
    DISABLED = 2
    ENABLED = 3
    SESSION_IDLE = 4
    VEND = 5


class AbstractState(ABC, metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(cls):
        raise NotImplementedError


class InactiveState(AbstractState):
    name: State.INACTIVE


if __name__ == '__main__':
    s = InactiveState()
