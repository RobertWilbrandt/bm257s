"""Read, organize and validate packages from data input"""
import enum
import threading


class Symbol(enum.Enum):
    """Enumeration of all LCD symbols
    """

    AUTO = enum.auto()
    DC = enum.auto()
    AC = enum.auto()
    REL = enum.auto()
    BEEP = enum.auto()
    BATTERY = enum.auto()
    LOZ = enum.auto()
    BMINUS = enum.auto()
    HOLD = enum.auto()
    DBM = enum.auto()
    MEGA = enum.auto()
    KILO = enum.auto()
    CREST = enum.auto()
    OHM = enum.auto()
    HZ = enum.auto()
    NANO = enum.auto()
    MAX = enum.auto()
    FARAD = enum.auto()
    MICRO = enum.auto()
    MILLI = enum.auto()
    MIN = enum.auto()
    VOLT = enum.auto()
    AMPERE = enum.auto()
    SCALE = enum.auto()


class Package:
    """Represents a single 15-byte serial package

    :param segments: List of tuples of 7-segment display segment occupancies
    :type segments: list
    :param dots: List of dot occupancies
    :type dots: list
    :param minus: Occupancy of minus sign
    :type minus: bool
    :param symbols: Set of symbols currently shown
    :type symbol: set
    """

    # pylint: disable=R0903
    # Remove this once usage becomes clearer

    def __init__(self, segments, dots, symbols):
        self.segments = segments
        self.dots = dots
        self.symbols = symbols


def parse_package(data):
    """Parses a package from raw multimeter data

    :param data: Raw multimeter data, aligned to 15-byte boundary
    :type data: bytes
    :raise RuntimeError: If package contains invalid data
    """

    # Check byte indices
    index_mask = ((1 << 5) - 1) << 4
    for (i, d_i) in enumerate(data):
        index_field = (d_i & index_mask) >> 4
        if index_field != i:
            raise RuntimeError(
                f"Raw data package contains invalid byte index at byte {i}",
                index_field,
            )

    segments = []
    dots = []
    symbols = []
    return Package(segments, dots, set(symbols))


class PackageReader:
    """Read, organize and validate packages from data input

    :param reader: Input reader used
    :type reader: Class with reader.read(len) method
    """

    PKG_LEN = 15
    PKG_START = 0b00000010  # Start of first package byte

    def __init__(self, reader):
        self._reader = reader

        self._read_thread = threading.Thread(target=self._run)
        self._read_thread_stop = threading.Event()

        self._last_pkg = None
        self._last_pkg_lock = threading.Lock()

    def start(self):
        """Start reading packages in a seperate thread

        Call this at most once until you call stop().
        """
        self._read_thread_stop.clear()
        self._read_thread.start()

    def stop(self):
        """Stop reading packages in seperate thread

        Only call this if you previously called start().
        """
        self._read_thread_stop.set()
        self._read_thread.join()

    def next_package(self):
        """Returns the last received package and removes it from storage

        :return: Last received packgae
        :rtype: Package
        """
        with self._last_pkg_lock:
            result = self._last_pkg
            self._last_pkg = None
            return result

    def _run(self):
        data = bytes()
        while not self._read_thread_stop.is_set():
            data = data + self._reader.read(self.PKG_LEN)

            for (i, byte) in enumerate(data):
                if byte == self.PKG_START:
                    data = data[i:]
                    break

            if len(data) >= self.PKG_LEN:
                pkg = parse_package(data[0 : self.PKG_LEN + 1])  # noqa: E203
                with self._last_pkg_lock:
                    self._last_pkg = pkg
