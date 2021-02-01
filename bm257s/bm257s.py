"""Serial interface library for brymen bm257s multimeters"""
import serial

from .lcd import BM257sLCD
from .measurement import Measurement, TemperatureMeasurement


def parse_lcd(lcd):
    """Parse measurement information from received lcd display state

    :param lcd: Current lcd display state
    :type lcd: BM257sLCD

    :return: Name of measurement quantity and measurement
    :rtype: tuple
    """

    segment_data = lcd.segment_data()

    if len(segment_data) == 2:
        value = segment_data[0]
        unit_string = segment_data[1]

        if not isinstance(value, int) or not isinstance(unit_string, str):
            return None

        unit_mapping = {
            "C": TemperatureMeasurement.UNIT_CELSIUS,
            "F": TemperatureMeasurement.UNIT_FAHRENHEIT,
        }
        if unit_string in unit_mapping:
            return (
                Measurement.TEMPERATURE,
                TemperatureMeasurement(unit=unit_mapping[unit_string], value=value),
            )

        raise RuntimeError("Unknown temperature unit", unit_string)

    if len(segment_data) == 1:
        if segment_data[0] == "---C":
            return (
                Measurement.TEMPERATURE,
                TemperatureMeasurement(
                    unit=TemperatureMeasurement.UNIT_CELSIUS, value=None
                ),
            )

        if segment_data[0] == "---F":
            return (
                Measurement.TEMPERATURE,
                TemperatureMeasurement(
                    unit=TemperatureMeasurement.UNIT_FAHRENHEIT, value=None
                ),
            )

    raise RuntimeError("Cannot parse segment data", segment_data)


class BM257sSerialInterface:
    """Serial interface used to communicate with brymen bm257s multimeters

    :param port: Device name to use
    :type port: str
    :param read_timeout: Maximum timeout for waiting while reading
    :type read_timeout: float
    :raise RuntimeError: If opening port is not possible
    """

    def __init__(self, port="/dev/ttyUSB0", read_timeout=0.0):
        self._lcd = BM257sLCD()

        try:
            self._serial = serial.Serial(
                port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                timeout=read_timeout,
            )
        except serial.SerialException as ex:
            raise RuntimeError(f"Could not open port {port}", ex)

    def read(self):
        """Reads measurement from multimeter

        :return: Tuple indicating measured quantity and corresponding measurement or
                 None in case of timeout
        :rtype: tuple
        """
        data = self._serial.read(15)
        if len(data) < 15:
            return None

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
