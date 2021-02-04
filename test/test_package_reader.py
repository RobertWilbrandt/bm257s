"""Unit tests for package reader module"""

import unittest

from bm257s.package_reader import Symbol, parse_package

from .helpers.raw_package_helpers import EXAMPLE_RAW_PKG, change_byte_index


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests"""

    def test_success(self):
        """Test of successfull test"""
        self.assertEqual("foo".upper(), "FOO")


class TestPackageParsing(unittest.TestCase):
    """Testcase for parsing of raw data packages"""

    def test_example_package(self):
        """Test parsing with 'spec'-provided example package"""
        # Example package should get parsed fine
        try:
            pkg = parse_package(EXAMPLE_RAW_PKG)
        except RuntimeError:
            self.fail("Falsely detected error in raw example package")

        self.assertEqual(
            pkg.symbols,
            {Symbol.AUTO, Symbol.AC, Symbol.VOLT, Symbol.SCALE},
            "Read correct symbols from example package",
        )
        self.assertEqual(
            pkg.segment_string(),
            "513.6",
            "Read correct segment string from example package",
        )

    def test_index_checking(self):
        self.assertRaises(
            RuntimeError,
            lambda _: parse_package(change_byte_index(EXAMPLE_RAW_PKG, 0, 1)),
            "Detect incremented first byte index",
        )
        self.assertRaises(
            RuntimeError,
            lambda _: parse_package(change_byte_index(EXAMPLE_RAW_PKG, 14, 13)),
            "Detect decremented last byte index",
        )
        self.assertRaises(
            RuntimeError,
            lambda _: parse_package(change_byte_index(EXAMPLE_RAW_PKG, 7, 12)),
            "Detect changed byte index in middle of package",
        )
