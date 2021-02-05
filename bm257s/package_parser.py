"""Parse package content to obtain measurement result"""

from .measurement import Measurement, VoltageMeasurement
from .package_reader import Symbol


def parse_voltage(pkg, prefix):
    """Parse voltage measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package
    :param prefix: Metric prefix of measurement
    :type prefix: str

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    value = pkg.segment_float()

    if Symbol.AC in pkg.symbols:
        current = VoltageMeasurement.CURRENT_AC
    elif Symbol.DC in pkg.symbols:
        current = VoltageMeasurement.CURRENT_DC

    return (
        Measurement.VOLTAGE,
        VoltageMeasurement(value=value, current=current, prefix=prefix),
    )


def parse_current(pkg, prefix):
    """Parse current measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package
    :param prefix: Metric prefix of measurement
    :type prefix: str

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_resistance(pkg, prefix):
    """Parse resistance measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package
    :param prefix: Metric prefix of measurement
    :type prefix: str

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_temperature(pkg, prefix):
    """Parse temperature measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package
    :param prefix: Metric prefix of measurement
    :type prefix: str

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_prefix(pkg):
    """Parse metrix prefix of measurement

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Packe

    :return: Prefix shown in measurement
    :rtype: str
    """
    if Symbol.KILO in pkg.symbols:
        return Measurement.PREFIX_KILO
    if Symbol.MEGA in pkg.symbols:
        return Measurement.PREFIX_MEGA
    if Symbol.MILLI in pkg.symbols:
        return Measurement.PREFIX_MILLI
    if Symbol.MICRO in pkg.symbols:
        return Measurement.PREFIX_MICRO

    return Measurement.PREFIX_NONE


def parse_package(pkg):
    """Parse package to obtain multimeter measurement

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    prefix = parse_prefix(pkg)

    if Symbol.VOLT in pkg.symbols:
        return parse_voltage(pkg, prefix)

    if Symbol.AMPERE in pkg.symbols:
        return parse_current(pkg, prefix)

    if Symbol.OHM in pkg.symbols:
        return parse_resistance(pkg, prefix)

    if pkg.symbols == set():
        return parse_temperature(pkg, prefix)

    raise RuntimeError("Cannot parse multimeter package configuration")
