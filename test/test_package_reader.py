"""Unit tests for package reader module"""

import unittest

from bm257s.package_reader import PackageReader, Symbol, parse_package

from .helpers.mock_data_reader import MockDataReader
from .helpers.raw_package_helpers import EXAMPLE_RAW_PKG, change_byte_index


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Set up package reader to get tested"""
        super().setUp()

        self._mock_reader = MockDataReader()
        self._pkg_reader = PackageReader(self._mock_reader)

        self._pkg_reader.start()

    def tearDown(self):
        """Stop package reader"""
        super().tearDown()

        self._pkg_reader.stop()


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
        self.assertAlmostEqual(
            pkg.segment_float(),
            513.6,
            msg="Read correct float number from example package",
        )

    def test_index_checking(self):
        """Test checking of byte indices in raw packages"""
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
