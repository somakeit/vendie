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
    _SETUP_BASE = '11'
    _VEND_BASE = '13'
    _READER_BASE = '14'
    _EXPANSION_BASE = '17'

    RESET = '10'

    SETUP_CONFIG_DATA = '1100'
    SETUP_MAX_MIN_PRICES = '1101'

    POLL = '12'

    VEND_REQUEST = '1300'
    VEND_CANCEL = '1301'
    VEND_SUCCESS = '1302'
    VEND_FAILURE = '1303'
    VEND_SESSION_COMPLETE = '1304'
    VEND_CASH_SALE = '1305'

    READER_DISABLE = '1400'
    READER_ENABLE = '1401'
    READER_CANCEL = '1402'

    EXPANSION_REQUEST_ID = '1700'
    EXPANSION_DIAGNOSTIC = '17FF'

    def __bytes__(self):
        bytes.fromhex(self.value)


if __name__ == '__main__':
    pass
