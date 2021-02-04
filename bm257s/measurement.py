"""Representation of measurements taken by bm257s multimeter"""
# pylint: disable=R0903
# Remove this once usage becomes clearer


class Measurement:
    """Generic measurement representation"""

    def __init__(self):
        pass

    TEMPERATURE = "TEMPERATURE"
    RESISTANCE = "RESISTANCE"
    VOLTAGE = "VOLTAGE"

    PREFIX_NONE = ""
    PREFIX_KILO = "k"
    PREFIX_MEGA = "M"


class TemperatureMeasurement(Measurement):
    """Representation of temperature measurement

    :param unit: Unit of measurement, either UNIT_CELSIUS or UNIT_FAHRENHEIT
    :type unit: int
    :param value: Measured temperature or None if no probe is connected
    :type value: int
    """

    UNIT_CELSIUS = 1
    UNIT_FAHRENHEIT = 2

    def __init__(self, unit, value):
        self.unit = unit
        self.value = value

        super().__init__()

    def __str__(self):
        value_str = "--" if self.value is None else self.value

        if self.unit == self.UNIT_CELSIUS:
            unit_str = "°C"
        elif self.unit == self.UNIT_FAHRENHEIT:
            unit_str = "F"

        return f"{value_str} {unit_str}"


class ResistanceMeasurement(Measurement):
    """Representation of resistance measurement

    :param value: Measured resistance or None if open loop
    :type value: float
    :param prefix: Metrix prefix of measurement
    :type prefix: int
    """

    def __init__(self, value, prefix=Measurement.PREFIX_NONE):
        self.value = value
        self.prefix = prefix

        super().__init__()

    def __str__(self):
        if self.value is not None:
            return f"{self.value}{self.prefix}Ω"

        return "0.L"


class VoltageMeasurement(Measurement):
    """Representation of voltage measurement

    :param value: Measured voltage
    :type value: float
    :param current: Type of current measured
    :type current: int
    """

    CURRENT_AC = 1
    CURRENT_DC = 2

    def __init__(self, value, current):
        self.value = value
        self.current = current

        super().__init__()

    def __str__(self):
        current_postfix = {self.CURRENT_AC: " [~]", self.CURRENT_DC: ""}
        return f"{self.value}V{current_postfix[self.current]}"
