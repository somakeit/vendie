from dataclasses import dataclass
from enum import StrEnum
from linecache import checkcache
from typing import Self

from vendie.vending_machine import calculate_checksum, verify_checksum


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
    COMMAND_OUT_OF_SEQUENCE = '0B'

@dataclass
class VendingMachineResponse:
    response: VMCResponse
    data: str = ''
    checksum: str = ''

    def __post_init__(self):
        data_str = self.response.value + self.data
        if not self.checksum:
            self.checksum = calculate_checksum(data_str)
        else:
            if not verify_checksum(data_str, self.checksum):
                print("Warning: Response checksum invalid... Recalculating")
                self.checksum = calculate_checksum(data_str)

    @classmethod
    def from_ascii_data(cls, ascii_data: str) -> Self:
        response_str: str = ''
        data_str: str = ''
        checksum_str: str = ''

        if len(ascii_data) < 2:
            raise ValueError('Command too short')

        if len(ascii_data) == 2:
            response_str = ascii_data
        else:
            response_str = ascii_data[0:2]
            data_str = ascii_data[2:-2]
            checksum_str = ascii_data[-2:]

        if checksum_str == '':
            checksum_str = calculate_checksum(response_str + data_str)

        assert verify_checksum(response_str + data_str, checksum_str)

        return cls(response=VMCResponse(response_str), data=data_str, checksum=checksum_str)

    def __str__(self):
        return self.response.value + self.data + self.checksum

if __name__ == '__main__':
    resp = VendingMachineResponse(VMCResponse.RESET, checksum='00')
    print(resp)
    print(repr(resp))