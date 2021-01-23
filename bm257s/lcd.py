"""Representation of bm257s LCD"""


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
        return (
            bool(seg_bytes[0] & 0b1000),  # A
            bool(seg_bytes[1] & 0b1000),  # B
            bool(seg_bytes[1] & 0b0010),  # C
            bool(seg_bytes[1] & 0b0001),  # D
            bool(seg_bytes[0] & 0b0010),  # E
            bool(seg_bytes[0] & 0b0100),  # F
            bool(seg_bytes[1] & 0b0100),  # G
        )
