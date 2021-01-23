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


class BM257sLCD:
    """Representation of bm257s lcd display
    """

    SEGMENT_VALUES = {
        (True, True, True, True, True, True, False): 0,
        (False, True, True, False, False, False, False): 1,
        (True, True, False, True, True, False, True): 2,
        (True, True, True, True, False, False, True): 3,
        (False, True, True, False, False, True, True): 4,
        (True, False, True, True, False, True, True): 5,
        (True, False, True, True, True, True, True): 6,
        (True, True, True, False, False, False, False): 7,
        (True, True, True, True, True, True, True): 8,
        (True, True, True, True, False, True, True): 9,
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
        """Parses data shown in 7-segment displays

        TODO: Don't ignore dots

        :return: List of recognized datums
        :rtype: list
        """
        result = []
        cur_part = None

        for i in range(0, 4):
            segment_conf = segment_from_data(self._data, i)

            if segment_conf in self.SEGMENT_VALUES:
                segment_data = self.SEGMENT_VALUES[segment_conf]

                if cur_part is None:
                    cur_part = segment_data
                elif isinstance(segment_data, int):
                    if isinstance(cur_part, int):
                        cur_part = 10 * cur_part + segment_data
                    else:
                        result = result + [cur_part]
                        cur_part = segment_data
                elif isinstance(segment_data, str):
                    if isinstance(cur_part, str):
                        cur_part = cur_part + segment_data
                    else:
                        result = result + [cur_part]
                        cur_part = segment_data
                else:
                    raise RuntimeError(
                        f"Cannot handle segment data for segment {i}",
                        segment_data,
                        segment_conf,
                    )

            else:
                raise RuntimeError(
                    f"Unable to parse segment {i}: Unknown configuration", segment_conf
                )

        if cur_part is not None:
            result = result + [cur_part]

        return result
