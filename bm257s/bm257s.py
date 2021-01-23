"""Serial interface library for brymen bm257s multimeters"""
import serial

from .lcd import BM257sLCD, Segment
from .measurement import Measurement, TemperatureMeasurement


def parse_lcd(lcd):
    """Parse measurement information from received lcd display state

    :param lcd: Current lcd display state
    :type lcd: BM257sLCD

    :return: Name of measurement quantity and measurement
    :rtype: tuple
    """

    segments = [lcd.segment(i) for i in range(0, 4)]

    if segments[3].matches(Segment.LETTER_C):
        return (
            Measurement.TEMPERATURE,
            TemperatureMeasurement(unit=TemperatureMeasurement.UNIT_CELSIUS),
        )
    if segments[3].matches(Segment.LETTER_F):
        return (
            Measurement.TEMPERATURE,
            TemperatureMeasurement(unit=TemperatureMeasurement.UNIT_FAHRENHEIT),
        )
    return None


class BM257sSerialInterface:
    """Serial interface used to communicate with brymen bm257s multimeters

    :param port: Device name to use
    :type port: str
    """

    def __init__(self, port="/dev/ttyUSB0"):
        self._lcd = BM257sLCD()

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

        self._lcd.set_data(data)
        return parse_lcd(self._lcd)

    def close(self):
        """Closes the used serial port
        """
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
