"""Representation of bm257s LCD"""


def segment_from_data(data, pos):
    """Reads a segment configuration from a data bytestring

    :param data: Received multimeter data, aligned to 15-byte package
    :type data: bytes
    :param pos: Position of segment to read
    :type pos: int

    :return: Segment configuration
    :rtype: tuple
    """
    seg_start = 3 + pos * 2
    seg_bytes = data[seg_start : seg_start + 2]  # noqa: E203
    return (
        bool(seg_bytes[0] & 0b1000),  # A
        bool(seg_bytes[1] & 0b1000),  # B
        bool(seg_bytes[1] & 0b0010),  # C
        bool(seg_bytes[1] & 0b0001),  # D
        bool(seg_bytes[0] & 0b0010),  # E
        bool(seg_bytes[0] & 0b0100),  # F
        bool(seg_bytes[1] & 0b0100),  # G
    )


def dot_from_data(data, pos):
    """Read a dot occupancy from a data bytestring

    :param data: Received multimeter data, aligned to 15-byte package
    :type data: bytes
    :param pos: Position of dot to read
    :type pos: int

    :return: Dot occupancy
    :rtype: bool
    """
    return data[5 + pos * 2] & 0b1


class SegmentString:
    """Representation of the segment display portion of a bm257s lcd display

    :param chars: List of segment characters
    :type chars: list
    :param dots: List of segment dot occupancies
    :type dots: list
    """

    def __init__(self, chars, dots):
        self.chars = chars
        self.dots = dots

    def int_value(self, start_i=0, end_i=3):
        """Try to parse integer value from segments

        :param start_i: First segment to consider
        :type start_i: int
        :param end_i: Last segment to consider
        :type end_i: int

        :return: Number shown by segments or None
        :rtype: int
        """
        try:
            if all(not dot for dot in self.dots[start_i:end_i]):
                value_str = "".join(self.chars[start_i : end_i + 1])  # noqa: E203
                return int(value_str)
        except ValueError:
            pass

        return None

    def string_value(self, start_i=0, end_i=3):
        """Read string value from segments

        Includes dots if present.

        :param start_i: First segment to consider
        :type start_i: int
        :param end_i: Last segment to consider
        :type end_i: int

        :return String shown by segments
        :rtype: str
        """
        result = ""
        for i in range(start_i, end_i + 1):
            result = result + self.chars[i]

            if self.dots[i]:
                result = result + "."

        return result


class BM257sLCD:
    """Representation of bm257s lcd display
    """

    SEGMENT_VALUES = {
        (True, True, True, True, True, True, False): "0",
        (False, True, True, False, False, False, False): "1",
        (True, True, False, True, True, False, True): "2",
        (True, True, True, True, False, False, True): "3",
        (False, True, True, False, False, True, True): "4",
        (True, False, True, True, False, True, True): "5",
        (True, False, True, True, True, True, True): "6",
        (True, True, True, False, False, False, False): "7",
        (True, True, True, True, True, True, True): "8",
        (True, True, True, True, False, True, True): "9",
        (True, False, False, True, True, True, False): "C",
        (True, False, False, False, True, True, True): "F",
        (False, False, False, False, False, False, True): "-",
    }

    def __init__(self):
        self._data = None

    def set_data(self, data):
        """Update display segment data

        :param data: New display segment data in 15 byte aligned package
        :type data: bytes
        """
        self._data = data

    def segment_data(self):
        """Parses data shown in 7-segment display

        :return: Content of 7-segment display
        :rtype: SegmentString
        :raise RuntimeError: If a segment shows an unknown configuration
        """
        characters = []
        for i in range(0, 4):
            segment_conf = segment_from_data(self._data, i)
            if segment_conf in self.SEGMENT_VALUES:
                characters = characters + [self.SEGMENT_VALUES[segment_conf]]
            else:
                raise RuntimeError(
                    f"Unknown segment configuration at segment {i}", segment_conf
                )

        dots = [dot_from_data(self._data, i) for i in range(0, 3)]

        return SegmentString(characters, dots)
