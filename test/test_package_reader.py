"""Unit tests for package reader module"""

import unittest

from bm257s.package_reader import parse_package

from .helpers.raw_package_helpers import EXAMPLE_RAW_PKG


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests
    """

    def test_success(self):
        """Test of successfull test
        """
        self.assertEqual("foo".upper(), "FOO")


class TestPackageParsing(unittest.TestCase):
    """Testcase for parsing of raw data packages
    """

    def test_example_package(self):
        """Test parsing with 'spec'-provided example package
        """
        _ = parse_package(EXAMPLE_RAW_PKG)
