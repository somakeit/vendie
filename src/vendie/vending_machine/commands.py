from dataclasses import dataclass, field
from enum import StrEnum
from typing import Self

from vendie.vending_machine import calculate_checksum, verify_checksum


class VMCCommand(StrEnum):
    RESET = '10'
    SETUP = '11'
    POLL = '12'
    VEND = '13'
    READER = '14'
    EXPANSION = '17'



@dataclass
class VendingMachineCommand:
    command: VMCCommand
    data: str = ''
    checksum: str = ''

    def __post_init__(self):
        data_str = self.command.value + self.data
        assert verify_checksum(data_str, self.checksum)

    @classmethod
    def from_ascii_data(cls, ascii_data: str) -> Self:
        command_str: str = ''
        data_str: str = ''
        checksum_str: str = ''

        if len(ascii_data) < 2:
            raise ValueError('Command too short')

        if len(ascii_data) == 2:
            command_str = ascii_data
        else:
            command_str = ascii_data[0:2]
            data_str = ascii_data[2:-2]
            checksum_str = ascii_data[-2:]

        if checksum_str == '':
            checksum_str = calculate_checksum(command_str + data_str)

        assert verify_checksum(command_str + data_str, checksum_str)

        return cls(command=VMCCommand(command_str), data=data_str, checksum=checksum_str)

    def __str__(self):
        return self.command.value + self.data + self.checksum


if __name__ == '__main__':
    resp = VendingMachineCommand(VMCCommand.RESET, checksum='10')
    print(resp)
    print(repr(resp))