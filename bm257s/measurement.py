"""Representation of measurements taken by bm257s multimeter"""


class Measurement:
    def __init__(self):
        pass

    TEMPERATURE = "TEMPERATURE"


class TemperatureMeasurement:
    UNIT_CELSIUS = 1
    UNIT_FAHRENHEIT = 2

    def __init__(self, unit, value):
        self.unit = unit
        self.value = value

    def __str__(self):
        if self.unit == self.UNIT_CELSIUS:
            return f"{self.value} °C"
        if self.unit == self.UNIT_FAHRENHEIT:
            return f"{self.value} F"

        return self
