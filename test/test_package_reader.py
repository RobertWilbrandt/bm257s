"""Unit tests for package reader module"""

import unittest

from bm257s.package_reader import PackageReader, parse_package

from .helpers.mock_data_reader import MockDataReader
from .helpers.raw_package_helpers import (
    EXAMPLE_RAW_PKG,
    EXAMPLE_RAW_PKG_STRING,
    EXAMPLE_RAW_PKG_SYMBOLS,
    EXAMPLE_RAW_PKG_VALUE,
    change_byte_index,
)


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests"""

    READER_TIMEOUT = 0.1

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

    def test_example_package(self):
        """Test parsing with 'spec'-provided example package"""
        self.assertTrue(
            self._mock_reader.all_data_used,
            "Mock data should be empty before test start",
        )

        self._mock_reader.set_next_data(EXAMPLE_RAW_PKG)
        self.assertTrue(
            self._pkg_reader.wait_for_package(self.READER_TIMEOUT),
            "Read package data from raw data reader",
        )
        pkg = self._pkg_reader.next_package()
        self.assertIsNotNone(pkg, "Package could get parsed fully")
        self.assertTrue(self._mock_reader.all_data_used)

        self.assertEqual(
            pkg.symbols,
            EXAMPLE_RAW_PKG_SYMBOLS,
            msg="Read correct symbols from example package",
        )
        self.assertEqual(
            pkg.segment_string(),
            EXAMPLE_RAW_PKG_STRING,
            msg="Read correct string from example package",
        )


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
            EXAMPLE_RAW_PKG_SYMBOLS,
            "Read correct symbols from example package",
        )
        self.assertEqual(
            pkg.segment_string(),
            EXAMPLE_RAW_PKG_STRING,
            "Read correct segment string from example package",
        )
        self.assertAlmostEqual(
            pkg.segment_float(),
            EXAMPLE_RAW_PKG_VALUE,
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
