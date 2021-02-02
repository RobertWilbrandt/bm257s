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


def minus_from_data(data):
    """Read the minus sign from a data bytestring

    :param data: Received multimeter data, aligned to 15-byte package
    :type data: bytes

    :return: Minus occupancy
    :rtype: bool
    """
    return data[3] & 0b1


def symbols_from_data(data):
    """Parse symbols from a data bytestring

    :param data: Received multimeter data, aligned to 15-byte package
    :type data: bytes

    :return: List of detected symbols
    :rtype: list
    """
    result = []
    if bool(data[12] & 0b00000100):
        result = result + [BM257sLCD.SYMBOL_OHM]
    if bool(data[11] & 0b00000001):
        result = result + [BM257sLCD.SYMBOL_k]
    if bool(data[11] & 0b00000010):
        result = result + [BM257sLCD.SYMBOL_M]

    return result


class SegmentString:
    """Representation of the segment display portion of a bm257s lcd display

    :param minus: Whether minus segment is shown
    :type minus: bool
    :param chars: List of segment characters
    :type chars: list
    :param dots: List of segment dot occupancies
    :type dots: list
    """

    def __init__(self, minus, chars, dots):
        self.minus = minus
        self.chars = chars
        self.dots = dots

    def string_value(self, start_i=0, end_i=3, ignore_dots=False, ignore_minus=False):
        """Read string value from segments

        Includes dots if present.

        :param start_i: First segment to consider
        :type start_i: int
        :param end_i: Last segment to consider
        :type end_i: int
        :param ignore_dots: Whether to ignore dots in string
        :type ignore_dots: bool
        :param ignore_minus: Whether to ignore the minus sign
        :type ignore_minus: bool

        :return: String shown by segments
        :rtype: str
        """
        if not ignore_minus and self.minus:
            result = "-"
        else:
            result = ""

        for i in range(start_i, end_i):
            result = result + self.chars[i]

            if self.dots[i] and not ignore_dots:
                result = result + "."

        result = result + self.chars[end_i]

        return result

    def int_value(self, start_i=0, end_i=3):
        """Try to parse integer value from segments

        :param start_i: First segment to consider
        :type start_i: int
        :param end_i: Last segment to consider
        :type end_i: int

        :return: Number shown by segments or None
        :rtype: int
        """
        sign = -1 if self.minus else 1

        try:
            if all(not dot for dot in self.dots[start_i:end_i]):
                value_str = "".join(self.chars[start_i : end_i + 1])  # noqa: E203
                return sign * int(value_str)
        except ValueError:
            pass

        return None

    def float_value(self, start_i=0, end_i=3):
        """Read float value from segments

        :param start_i: First segment to consider
        :type start_i: int
        :param end_i: Last segment to consider
        :type end_i: int

        :return: Float shown by segments or None
        :rtype: float
        """
        sign = -1 if self.minus else 1

        val_str = self.string_value(start_i, end_i)
        val_str_raw = self.string_value(
            start_i, end_i, ignore_dots=True, ignore_minus=True
        )
        if val_str_raw.isdigit():
            try:
                return sign * float(val_str)
            except ValueError:
                pass

        return None


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
        (False, False, False, False, False, False, False): " ",
        (False, False, False, True, True, True, False): "L",
    }

    SYMBOL_OHM = 1
    SYMBOL_k = 2
    SYMBOL_M = 3

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
        minus = minus_from_data(self._data)

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

        return SegmentString(minus, characters, dots)

    def symbols(self):
        """Parses symbols shown

        :return: List of shown symbols
        :rtype: list
        """
        return symbols_from_data(self._data)
