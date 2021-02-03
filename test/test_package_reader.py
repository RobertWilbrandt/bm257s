"""Unit tests for package reader module"""

import unittest


class TestPackageReader(unittest.TestCase):
    """Testcase for package reader unit tests
    """

    def test_success(self):
        """Test of successfull test
        """
        self.assertEqual("foo".upper(), "FOO")
