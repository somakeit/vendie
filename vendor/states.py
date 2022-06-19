from enum import Enum


class State(Enum):
    INACTIVE = 1
    DISABLED = 2
    ENABLED = 3
    SESSION_IDLE = 4
    VEND = 5

    


if __name__ == '__main__':
    print([state for state in list(State)])

    print(State.INACTIVE)