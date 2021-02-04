"""Serial interface library for brymen bm257s multimeters"""
import serial

from .lcd import BM257sLCD
from .measurement import (
    Measurement,
    ResistanceMeasurement,
    TemperatureMeasurement,
    VoltageMeasurement,
)


def parse_lcd(lcd):
    """Parse measurement information from received lcd display state

    :param lcd: Current lcd display state
    :type lcd: BM257sLCD

    :return: Name of measurement quantity and measurement
    :rtype: tuple
    :raise RuntimeError: If lcd state seems invalid
    """
    # pylint: disable=R0912
    # This method will get replaced soon

    segments = lcd.segment_data()
    symbols = set(lcd.symbols())

    res_symbols = {BM257sLCD.SYMBOL_OHM, BM257sLCD.SYMBOL_k, BM257sLCD.SYMBOL_M}
    vol_symbols = {BM257sLCD.SYMBOL_V, BM257sLCD.SYMBOL_AC, BM257sLCD.SYMBOL_DC}

    if symbols == set():
        temp_unit_mapping = {
            "C": TemperatureMeasurement.UNIT_CELSIUS,
            "F": TemperatureMeasurement.UNIT_FAHRENHEIT,
        }
        if segments.chars[3] in temp_unit_mapping:
            if segments.string_value(0, 2) == "---":
                value = None
            else:
                value = segments.int_value(0, 2)
                if value is None:
                    raise RuntimeError("Cannot parse temperature value")

            return (
                Measurement.TEMPERATURE,
                TemperatureMeasurement(
                    unit=temp_unit_mapping[segments.chars[3]], value=value
                ),
            )

    elif BM257sLCD.SYMBOL_OHM in symbols and symbols.issubset(res_symbols):
        if segments.string_value() == " 0.L ":
            return (Measurement.RESISTANCE, ResistanceMeasurement(value=None))

        value = segments.float_value()

        if BM257sLCD.SYMBOL_k in symbols:
            prefix = Measurement.PREFIX_KILO
        elif BM257sLCD.SYMBOL_M in symbols:
            prefix = Measurement.PREFIX_MEGA
        else:
            prefix = Measurement.PREFIX_NONE

        if value is not None:
            return (
                Measurement.RESISTANCE,
                ResistanceMeasurement(value=value, prefix=prefix),
            )

    elif BM257sLCD.SYMBOL_V in symbols and symbols.issubset(vol_symbols):
        value = segments.float_value()

        if BM257sLCD.SYMBOL_AC in symbols:
            current = VoltageMeasurement.CURRENT_AC
        elif BM257sLCD.SYMBOL_DC in symbols:
            current = VoltageMeasurement.CURRENT_DC

        return (Measurement.VOLTAGE, VoltageMeasurement(value=value, current=current))

    raise RuntimeError("Cannot parse LCD configuration")


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
            raise RuntimeError(f"Could not open port {port}", ex) from ex

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
        """Closes the used serial port"""
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
