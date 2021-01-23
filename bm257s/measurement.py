"""Representation of measurements taken by bm257s multimeter"""


class Measurement:
    def __init__(self):
        pass

    TEMPERATURE = "TEMPERATURE"


class TemperatureMeasurement:
    UNIT_CELSIUS = 1
    UNIT_FAHRENHEIT = 2

    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        if self.unit == self.UNIT_CELSIUS:
            return "?? °C"
        if self.unit == self.UNIT_FAHRENHEIT:
            return "?? F"

        return self
