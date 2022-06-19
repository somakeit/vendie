from enum import Enum


class Command(Enum):
    RESET = '0x1060'
    SETUP = '0x1161'
    POLL = '0x1262'
    VEND = '0x1363'
    READER = '0x1464'
    EXPANSION = '0x1767'
