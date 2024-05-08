hex_str = '0x37'
byte = b'37'
byte_str = '37'

print(f'{int(hex_str, 16)=}')
print(f'{int(byte, 16)=}')
print(f'{int(byte.decode(), 16)=}')
print(f'{hex(55)=}')
print(f'{byte_str.encode()=}')

print(hex(int('00010010', 2)))

print(f'{bin(55)=}')

print(bin(int('03FFFF01', 16)))