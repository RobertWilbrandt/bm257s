"""Serial interface library for brymen bm257s multimeters"""
import serial


def parse_lcd(data):
    """Parse measurement information from raw serial LCD data

    :param data: Raw serial data from device, aligned to 15-byte package
    :type data: bytes

    :return: Name of measurement quantity and measurement
    :rtype: tuple
    """
    segment_temp_celsius = (True, False, False, True, True, True, False)

    segments = [lcd_segment(data, i) for i in range(0, 4)]

    if segments[3] == segment_temp_celsius:
        return (Measurement.TEMPERATURE, TemperatureMeasurement())
    return None


def lcd_segment(data, pos):
    """Read one of the four segments from the LCD

    :param data: Raw serial data from device, aligned to 15-byte package
    :type data: bytes
    :param pos: Which segment to extract, left to right
    :type pos: int

    :return: Segment occupancy information
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


class Measurement:
    def __init__(self):
        pass

    TEMPERATURE = "TEMPERATURE"


class TemperatureMeasurement:
    def __init__(self):
        pass


class BM257sSerialInterface:
    """Serial interface used to communicate with brymen bm257s multimeters

    :param port: Device name to use
    :type port: str
    """

    def __init__(self, port="/dev/ttyUSB0"):
        self._serial = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
        )

    def read(self):
        """Reads measurement from multimeter

        :return: Tuple indicating measured quantity and corresponding measurement
        :rtype: tuple
        """
        data = self._serial.read(15)

        # Use counter in data to check if we got one whole package or need to "align"
        start_cnt = int((data[0] & 0b11110000) >> 4)
        if start_cnt != 0:
            left_to_read = 15 - start_cnt
            next_data = self._serial.read(left_to_read)
            data = data[15 - start_cnt :] + next_data  # noqa: E203

        return parse_lcd(data)

    def close(self):
        """Closes the used serial port
        """
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
