from enum import Enum
from dataclasses import dataclass




class SetupCommand(Enum):
    CONFIG_DATA = 0x00
    MAX_MIN_PRICES = 0x01


class VendCommand(Enum):
    VEND_REQUEST = 0x00
    VEND_CANCEL = 0x01
    VEND_SUCCESS = 0x02
    VEND_FAILURE = 0x03
    VEND_SESSION_COMPLETE = 0x04
    VEND_CASH_SALE = 0x05


class ReaderCommand(Enum):
    DISABLE = 0x00
    ENABLE = 0x01
    CANCEL = 0x02


class ExpansionCommand(Enum):
    REQUEST_ID = 0x03
    DIAGNOSTIC = 0xFF


class Command(Enum):
    RESET = 0x1060
    SETUP = 0x1161, SetupCommand
    POLL = 0x1262
    VEND = 0x1363, VendCommand
    READER = 0x1464, ReaderCommand
    EXPANSION = 0x1767, ExpansionCommand


import inspect


from typing import Type


def print_enum(e: Type[Enum|SuperNestedEnum]) -> None:
    for p in e:
        print(p.__dict__)
        try:
            assert(issubclass(p.value, Enum))
            print_enum(p.value)
        except (AssertionError, TypeError):
            print(p)


# ALL_COMMANDS = iter_enum()

if __name__ == '__main__':
    print_enum(Command)
