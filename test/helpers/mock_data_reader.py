"""Mock data reader for testing interactions with a package reader"""

import threading


class MockDataReader:
    """Mock data reader to test package reader interactions"""

    def __init__(self):
        self._next_data = b""
        self._next_data_lock = threading.Lock()

    def set_next_data(self, data):
        """Set the next data to get read from by the next read invocation

        :param data: Data to read from in the next read invocation
        :type data: bytes
        """
        with self._next_data_lock:
            self._next_data = data

    def all_data_used(self):
        """Test if all data set by set_next_data got read in read() invocations

        Can be called after a test to verify that all packages were read

        :return: Whether there is more dummy data left
        :rtype: bool
        """
        with self._next_data_lock:
            return len(self._next_data) == 0

    def read(self, size):
        """Read dummy data previously set by set_next_data

        :param size: Amount of data to read
        :type size: int

        :return: Chunk of dummy data set by set_next_data
        :rtype: bytes
        """
        with self._next_data_lock:
            real_size = min(size, len(self._next_data))
            result = self._next_data[0:real_size]
            self._next_data = self._next_data[real_size:]

            return result
