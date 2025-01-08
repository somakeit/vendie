from enum import StrEnum


class VMCResponse(StrEnum):
    RESET = '00'
    READER_CONFIG_DATA = '01'
    DISPLAY_REQUEST = '02'
    BEGIN_SESSION = '03'
    SESSION_CANCEL_REQUEST = '04'
    VEND_APPROVED = '05'
    VEND_DENIED = '06'
    END_SESSION = '07'
    CANCELLED = '08'
    PERIPHERAL_ID = '09'
    MALFUNCTION_ERROR = '0A'
    COMMAND_OUT_OF_SEQUENCE = '0B'