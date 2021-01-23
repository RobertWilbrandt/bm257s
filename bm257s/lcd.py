"""Representation of bm257s LCD"""


class Segment:
    """Representation of occupancy of a single LCD display segment

    :param segments: Occupancy information of display segment
    :type segments: tuple
    """

    LETTER_C = (True, False, False, True, True, True, False)
    LETTER_F = (True, False, False, False, True, True, True)

    DIGITS = [
        (True, True, True, True, True, True, False),  # 0
        (False, True, True, False, False, False, False),  # 1
        (True, True, False, True, True, False, True),  # 2
        (True, True, True, True, False, False, True),  # 3
        (False, True, True, False, False, True, True),  # 4
        (True, False, True, True, False, True, True),  # 5
        (True, False, True, True, True, True, True),  # 6
        (True, True, True, False, False, False, False),  # 7
        (True, True, True, True, True, True, True),  # 8
        (True, True, True, True, False, True, True),  # 9
    ]

    def __init__(self, segments):
        self._segments = segments

    def matches(self, segments):
        """Checks if this segment occupancy matches a fixed mask

        :param segments: Occupancy of fixed segment mask
        :type segments: tuple
        """
        return self._segments == segments

    def digit(self):
        """Returns digit represented by this segment

        :return: Digit represented by this segment
        :rtype: int
        :raise RuntimeError: If the current segment configuration does not represent a
                             digit
        """
        for (i, mask) in enumerate(self.DIGITS):
            if self.matches(mask):
                return i

        raise RuntimeError(
            "Current segment configuration does not represent a digit", self._segments
        )


class BM257sLCD:
    """Representation of bm257s lcd display
    """

    def __init__(self):
        self._data = None

    def set_data(self, data):
        """Update display segment data

        :param data: New display segment data in 15 byte aligned package
        :type data: bytes
        """
        self._data = data

    def segment(self, pos):
        """Read one of the four segments from the LCD

        :param pos: Which segment to extract, numbered from left to right
        :type pos: int

        :return: Segment occupancy information
        :rtype: tuple
        """
        seg_start = 3 + pos * 2
        seg_bytes = self._data[seg_start : seg_start + 2]  # noqa: E203
        return Segment(
            (
                bool(seg_bytes[0] & 0b1000),  # A
                bool(seg_bytes[1] & 0b1000),  # B
                bool(seg_bytes[1] & 0b0010),  # C
                bool(seg_bytes[1] & 0b0001),  # D
                bool(seg_bytes[0] & 0b0010),  # E
                bool(seg_bytes[0] & 0b0100),  # F
                bool(seg_bytes[1] & 0b0100),  # G
            )
        )

    def number(self, start_seg=0, end_seg=3):
        """Parse the number shown in a range of segments

        :param start_seg: First segment showing number (inclusive)
        :type start_seg: int
        :param end_seg: Last segment showing number (inclusive)
        :type end_seg: int

        :return: Number shown in specified range of segments
        :rtype: int
        :raise RuntimeError: If the segment range does not represent a number
        """
        segments = [self.segment(i) for i in range(start_seg, end_seg + 1)]
        digits = [seg.digit() for seg in segments]

        result = 0
        for i in digits:
            result = result * 10 + i

        return result
