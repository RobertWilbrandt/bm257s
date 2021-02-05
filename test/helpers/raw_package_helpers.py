"""Helper methods for creating and checking raw data packages"""

# Example from "spec" that should read "AC 513.6V"
EXAMPLE_RAW_PKG = b"\x02\x1A\x20\x3C\x47\x50\x6A\x78\x8F\x9F\xA7\xB0\xC0\xD0\xE5"


def change_byte_index(data, pos, index):
    """Changes the byte index at a specific position in a package to a different value

    :param data: Raw data package
    :type data: bytes
    :param pos: Index of byte to change
    :type pos: int
    :param index: New index
    :type index: int

    :return: Raw data package with changed byte
    :rtype: bytes
    """
    data_part_mask = (1 << 5) - 1
    new_byte = bytes([(index << 4) | (data[pos] & data_part_mask)])

    return data[0:pos] + new_byte + data[pos + 1 :]  # noqa: E203
