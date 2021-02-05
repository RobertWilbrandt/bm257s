"""Parse package content to obtain measurement result"""

from .package_reader import Symbol


def parse_voltage(pkg):
    """Parse voltage measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_current(pkg):
    """Parse current measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_resistance(pkg):
    """Parse resistance measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_temperature(pkg):
    """Parse temperature measurement from package

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    raise NotImplementedError("Type of measurement is not yet supported")


def parse_package(pkg):
    """Parse package to obtain multimeter measurement

    :param pkg: Package to parse
    :type pkg: bm257s.package_parser.Package

    :return: Multimeter measurement type and measurement
    :rtype: tuple
    """
    if Symbol.VOLT in pkg.symbols:
        return parse_voltage(pkg)

    if Symbol.AMPERE in pkg.symbols:
        return parse_current(pkg)

    if Symbol.OHM in pkg.symbols:
        return parse_resistance(pkg)

    if pkg.symbols == set():
        return parse_temperature(pkg)

    raise RuntimeError("Cannot parse multimeter package configuration")
