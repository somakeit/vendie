from enum import Enum


class Command(Enum):
    RESET = 0x1060
    SETUP = 0x1161
    POLL = 0x1262
    VEND = 0x1363
    READER = 0x1464
    EXPANSION = 0x1767


class SubCommands(Enum):
    SETUP_CONFIG_DATA = 0x00
    SETUP_MAX_MIN_PRICES = 0x01
    VEND_VEND_REQUEST = 0x00
    VEND_VEND_CANCEL = 0x01
    VEND_VEND_SUCCESS = 0x02
    VEND_VEND_FAILURE = 0x03
    VEND_SESSION_COMPLETE = 0x04
    VEND_CASH_SALE = 0x05
    READER_DISABLE = 0x00
    READER_ENABLE = 0x01
    READER_CANCEL = 0x02
    EXPANSION_REQUEST_ID = 0x03
    EXPANSION_DIAGNOSTIC = 0xFF


if __name__ == '__main__':
    print(Command.SETUP.value | SubCommands.SETUP_CONFIG_DATA.value)
