from enum import StrEnum


class VMCCommand(StrEnum):
    RESET = '10'
    SETUP = '11'
    POLL = '12'
    VEND = '13'
    READER = '14'
    EXPANSION = '17'