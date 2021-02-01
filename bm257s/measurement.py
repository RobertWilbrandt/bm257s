"""Representation of measurements taken by bm257s multimeter"""


class Measurement:
    def __init__(self):
        pass

    TEMPERATURE = "TEMPERATURE"
    RESISTANCE = "RESISTANCE"


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
    """

    def __init__(self, value):
        self.value = value

        super().__init__()

    def __str__(self):
        if self.value is not None:
            return f"{self.value}Ω"

        return "0.L"
