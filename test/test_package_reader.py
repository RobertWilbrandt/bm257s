"""Unit tests for package reader module"""

import unittest

from bm257s.package_reader import PackageReader, parse_package

from .helpers.mock_data_reader import MockDataReader
from .helpers.raw_package_helpers import (
    EXAMPLE_RAW_PKG,
    change_byte_index,
    check_example_pkg,
)


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests"""

    READER_TIMEOUT = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls._mock_reader = MockDataReader()
        cls._pkg_reader = PackageReader(cls._mock_reader)

    def setUp(self):
        """Set up package reader to get tested"""
        super().setUp()

        self.assertTrue(
            self._mock_reader.all_data_used(),
            msg="Mock data should be empty before test start",
        )

        self._pkg_reader.start()

    def tearDown(self):
        """Stop package reader"""
        super().tearDown()

        self._pkg_reader.stop()
        self.assertTrue(
            self._mock_reader.all_data_used(),
            msg="Mock data should be empty after test end",
        )

    def test_reader_restart(self):
        """Test restart behavior of package reader"""
        self._mock_reader.set_next_data(EXAMPLE_RAW_PKG)
        self.assertTrue(
            self._pkg_reader.wait_for_package(self.READER_TIMEOUT),
            msg="Reader should read package from input",
        )
        self.assertTrue(
            self._mock_reader.all_data_used(),
            "Reader should read all input data to get a package",
        )
        self.assertTrue(
            self._pkg_reader.is_running(), "Reader should normally be running"
        )

        # Stop reader
        self._pkg_reader.stop()
        self.assertFalse(
            self._pkg_reader.is_running(), "Reader should not be running after stop"
        )

        self._pkg_reader.start()
        self.assertTrue(
            self._pkg_reader.is_running(), "Reader should be running again after start"
        )

        # Should not keep any package lying around
        self.assertIsNone(
            self._pkg_reader.next_package(), msg="Restart should clear read packages"
        )

        # But should read new packages again
        self._mock_reader.set_next_data(EXAMPLE_RAW_PKG)
        self.assertTrue(
            self._pkg_reader.wait_for_package(self.READER_TIMEOUT),
            msg="Package reader reads new package after restart",
        )
        pkg = self._pkg_reader.next_package()
        self.assertIsNotNone(
            pkg, msg="Successfull waiting after reastart should yield a package"
        )
        check_example_pkg(self, pkg)

    def test_example_package(self):
        """Test parsing with 'spec'-provided example package"""
        self._mock_reader.set_next_data(EXAMPLE_RAW_PKG)
        self.assertTrue(
            self._pkg_reader.wait_for_package(self.READER_TIMEOUT),
            "Read package data from raw data reader",
        )
        pkg = self._pkg_reader.next_package()
        self.assertIsNotNone(pkg, "Package could get parsed fully")
        self.assertTrue(self._mock_reader.all_data_used)

        check_example_pkg(self, pkg)

    def test_misaligned_package(self):
        """Test alignment handling of package parser"""
        misaligned_data = {
            1: (EXAMPLE_RAW_PKG[14:15] + EXAMPLE_RAW_PKG),
            9: (EXAMPLE_RAW_PKG[9:15] + EXAMPLE_RAW_PKG),
            14: (EXAMPLE_RAW_PKG[1:15] + EXAMPLE_RAW_PKG),
        }

        for misalignment, data in misaligned_data.items():
            self.assertTrue(
                self._mock_reader.all_data_used,
                "Mock data should be empty before test start",
            )

            self._mock_reader.set_next_data(data)
            self.assertTrue(
                self._pkg_reader.wait_for_package(self.READER_TIMEOUT),
                f"Read package from raw data reader (misaligned by {misalignment})",
            )
            pkg = self._pkg_reader.next_package()
            self.assertIsNotNone(
                pkg, f"Package could not get parsed (misaligned by {misalignment})"
            )
            self.assertTrue(
                self._mock_reader.all_data_used,
                msg="Did not read all data from package (misaligned by "
                f"{misalignment})",
            )

            check_example_pkg(self, pkg)


class TestPackageParsing(unittest.TestCase):
    """Testcase for parsing of raw data packages"""

    def test_example_package(self):
        """Test parsing with 'spec'-provided example package"""
        # Example package should get parsed fine
        try:
            pkg = parse_package(EXAMPLE_RAW_PKG)
        except RuntimeError:
            self.fail("Falsely detected error in raw example package")

        check_example_pkg(self, pkg)

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
