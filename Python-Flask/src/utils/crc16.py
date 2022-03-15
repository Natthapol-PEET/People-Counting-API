import numpy as np


def crc16(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)

    poly = 0x8005
    # crc = 0x0000
    crc = 0xFFFF
    for b in data:
        # crc ^= (0xFF & b)
        crc ^= b
        for _ in range(0, 8):
            # if (crc & 0x0001):
            if (crc & 0x01):
                # crc = ((crc >> 1) & 0xFFFF) ^ poly
                crc = crc >> 1
                crc ^= 0xA001
            else:
                # crc = ((crc >> 1) & 0xFFFF)
                crc = crc >> 1

    # reverse byte order if you need to
    # crc = (crc << 8) | ((crc >> 8) & 0xFF)

    return np.uint16(crc)


# input = '0400000000000003000A780000000000000000000002000000000000000000000000000000000000000000110305111126000A00141E0000'
# output = bytearray.fromhex(input)

# manually creating bytearray
# print("{} --> {}".format(input, hex(crc16(b'\xff\xfe\x00\x04'))))

# do it for me
# print("{} --> {} - {}".format(input, hex(crc16(output)), crc16(output)))
# print("-------------------------- -------------------------- -------------------------- -------------------------- 0x9351")

def crc16Encode(input):
    output = bytearray.fromhex(input)

    return hex(crc16(output))[2:]
