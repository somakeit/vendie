def calculate_checksum(data_hex: str) -> str:
    data_bytes = bytes.fromhex(data_hex)

    # Calculate the sum of the byte values and limit to 2 hex characters (1 byte)
    total_sum = sum(data_bytes)
    total_sum &= 0xFF  # Ensure it is within 0x00 - 0xFF

    # Convert the calculated checksum to hex without '0x' prefix and uppercase it
    calculated_checksum_hex = f"{total_sum:02X}"

    return calculated_checksum_hex.upper()

def data_with_checksum(data: str):
    return data + calculate_checksum(data)


def verify_checksum(data_hex: str, expected_checksum_hex: str) -> bool:

    # Convert the calculated checksum to hex without '0x' prefix and uppercase it
    calculated_checksum_hex = calculate_checksum(data_hex)

    # Ensure the expected checksum is in the correct format
    expected_checksum_hex = expected_checksum_hex.upper().zfill(2)

    # Verify the checksum
    return calculated_checksum_hex == expected_checksum_hex