from dataclasses import dataclass, field
from enum import StrEnum
from typing import Self

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
    data: str | None = None
    checksum: str | None = None

    @classmethod
    def from_ascii_data(cls, ascii_data: str) -> Self:
        command_str: str = ''
        data_str: str | None = None
        checksum_str: str | None = None

        assert len(ascii_data) % 2 == 0, "Invalid format"

        if len(ascii_data) < 2:
            raise ValueError('Command too short')

        if len(ascii_data) == 2:
            command_str = ascii_data
        else:
            command_str = ascii_data[0:2]
            data_str = ascii_data[2:-2]
            checksum_str = ascii_data[-2:]

        assert verify_checksum(command_str, data_str, checksum_str)

        return cls(command=VMCCommand(command_str), data=data_str, checksum=checksum_str)

def verify_checksum(command_hex: str, data_hex: str, expected_checksum_hex: str) -> bool:
    """
    Verify if the checksum matches the sum of the command_hex and data_hex.

    :param command_hex: The command string in hex format.
    :param data_hex: The data string in hex format.
    :param expected_checksum_hex: The expected checksum in hex format.
    :return: True if the checksum matches, False otherwise.
    """

    # Convert hex strings to bytes
    command_bytes = bytes.fromhex(command_hex)
    data_bytes = bytes.fromhex(data_hex)

    # Calculate the sum of the byte values and limit to 2 hex characters (1 byte)
    total_sum = sum(command_bytes) + sum(data_bytes)
    total_sum &= 0xFF  # Ensure it is within 0x00 - 0xFF

    # Convert the calculated checksum to hex without '0x' prefix and uppercase it
    calculated_checksum_hex = f"{total_sum:02X}"

    # Ensure the expected checksum is in the correct format
    expected_checksum_hex = expected_checksum_hex.upper().zfill(2)

    # Print debug information (optional)
    print(f'Command Bytes: {command_bytes}')
    print(f'Data Bytes: {data_bytes}')
    print(f'Total Sum: {total_sum}')
    print(f'Calculated Checksum: {calculated_checksum_hex}')
    print(f'Expected Checksum: {expected_checksum_hex}')

    # Verify the checksum
    return calculated_checksum_hex == expected_checksum_hex
