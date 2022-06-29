from enum import Enum


# class Command(Enum):
#     RESET = 0x1060
#     SETUP = 0x1161
#     POLL = 0x1262
#     VEND = 0x1363
#     READER = 0x1464
#     EXPANSION = 0x1767
#
#
# class SubCommands(Enum):
#     SETUP_CONFIG_DATA = 0x00
#     SETUP_MAX_MIN_PRICES = 0x01
#     VEND_VEND_REQUEST = 0x00
#     VEND_VEND_CANCEL = 0x01
#     VEND_VEND_SUCCESS = 0x02
#     VEND_VEND_FAILURE = 0x03
#     VEND_SESSION_COMPLETE = 0x04
#     VEND_CASH_SALE = 0x05
#     READER_DISABLE = 0x00
#     READER_ENABLE = 0x01
#     READER_CANCEL = 0x02
#     EXPANSION_REQUEST_ID = 0x03
#     EXPANSION_DIAGNOSTIC = 0xFF

class Command(Enum):
    _SETUP_BASE = 0x1161
    _VEND_BASE = 0x1363
    _READER_BASE = 0x1464
    _EXPANSION_BASE = 0x1767

    RESET = 0x1060

    SETUP_CONFIG_DATA = 0x116100
    SETUP_MAX_MIN_PRICES = 0x116101

    POLL = 0x1262

    VEND_REQUEST = 0x136300
    VEND_CANCEL = 0x136301
    VEND_SUCCESS = 0x136302
    VEND_FAILURE = 0x136303
    VEND_SESSION_COMPLETE = 0x136304
    VEND_CASH_SALE = 0x136305

    READER_DISABLE = 0x146400
    READER_ENABLE = 0x146401
    READER_CANCEL = 0x146402

    EXPANSION_REQUEST_ID = 0x176703
    EXPANSION_DIAGNOSTIC = 0x1767FF


if __name__ == '__main__':
    serial_command = 0x136300
    try:
        actual_command = Command(serial_command)
    except ValueError:
        actual_command = None

    print(hex(serial_command))
    print(actual_command.name)
