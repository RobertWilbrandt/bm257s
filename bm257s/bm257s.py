"""Serial interface library for brymen bm257s multimeters"""
import serial


def decode_lcd(data):
    """Decodes the serial data sent from the multimeter

    :param data: 15 byte data package from multimeter
    :type data: list

    :return: Decoded LCD state
    :rtype: dict
    """
    return None


class BM257sSerialInterface:
    """Serial interface used to communicate with brymen bm257s multimeters

    :param port: Device name to use
    :type port: str
    """

    def __init__(self, port="/dev/ttyUSB0"):
        self._serial = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
        )

    def read_lcd(self):
        """Reads the current state of the LCD

        :return: Decoded LCD state
        :rtype: dict
        """
        msg = self._serial.read(15)
        print(msg)

    def close(self):
        """Closes the used serial port
        """
        self._serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
