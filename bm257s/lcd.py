"""Representation of bm257s LCD"""


class Segment:
    LETTER_C = (True, False, False, True, True, True, False)
    LETTER_F = (True, False, False, False, True, True, True)

    def __init__(self, segments):
        self._segments = segments

    def matches(self, segments):
        """Checks if this segment occupancy matches a fixed mask

        :param segments: Occupancy of fixed segment mask
        :type segments: tuple
        """
        return self._segments == segments


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
