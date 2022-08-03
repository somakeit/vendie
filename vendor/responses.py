# Document = https://wiki.nottinghack.org.uk/images/d/d2/MDB_3.0.pdf # Note: Page 100
from enum import Enum


class Response(Enum):
    JUST_RESET = '00'
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
    CMD_OUT_OF_SEQUENCE = '0B'
    ACKNOWLEDGE = '0010'
    NOT_ACKNOWLEDGED = 'FF'

    def __bytes__(self):
        return bytes.fromhex(self.value)

# 00H - Just Reset
# 01H - Reader Config Data
# 02H - Display Request
# 03H - Begin Session
# 04H - Session Cancel
# Request
# 05H - Vend Approved
# 06H - Vend Denied
# 07H - End Session
# 08H - Cancelled
# 09H - Peripheral ID
# 0AH - Malfunction / Error
# 0BH - Cmd Out Of Sequence


if __name__ == '__main__':
    response = Response.MALFUNCTION_ERROR

    print(response)
    print(response.value)
    print(bytes(response))
    print(bytes(response).hex())