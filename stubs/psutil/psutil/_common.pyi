"""Common objects shared by __init__.py and _ps*.py modules.

Note: this module is imported by setup.py, so it should not import
psutil or third-party modules.
"""

import enum
from _typeshed import StrOrBytesPath, SupportsWrite
from collections.abc import Callable
from socket import AF_INET6 as AF_INET6, AddressFamily, SocketKind
from typing import Any, Literal, NamedTuple, TypeVar, overload

POSIX: bool
WINDOWS: bool
LINUX: bool
MACOS: bool
OSX: bool
FREEBSD: bool
OPENBSD: bool
NETBSD: bool
BSD: bool
SUNOS: bool
AIX: bool

STATUS_RUNNING: Literal["running"]
STATUS_SLEEPING: Literal["sleeping"]
STATUS_DISK_SLEEP: Literal["disk-sleep"]
STATUS_STOPPED: Literal["stopped"]
STATUS_TRACING_STOP: Literal["tracing-stop"]
STATUS_ZOMBIE: Literal["zombie"]
STATUS_DEAD: Literal["dead"]
STATUS_WAKE_KILL: Literal["wake-kill"]
STATUS_WAKING: Literal["waking"]
STATUS_IDLE: Literal["idle"]
STATUS_LOCKED: Literal["locked"]
STATUS_WAITING: Literal["waiting"]
STATUS_SUSPENDED: Literal["suspended"]
STATUS_PARKED: Literal["parked"]

CONN_ESTABLISHED: str
CONN_SYN_SENT: str
CONN_SYN_RECV: str
CONN_FIN_WAIT1: str
CONN_FIN_WAIT2: str
CONN_TIME_WAIT: str
CONN_CLOSE: str
CONN_CLOSE_WAIT: str
CONN_LAST_ACK: str
CONN_LISTEN: str
CONN_CLOSING: str
CONN_NONE: str
NIC_DUPLEX_FULL: int
NIC_DUPLEX_HALF: int
NIC_DUPLEX_UNKNOWN: int

class NicDuplex(enum.IntEnum):
    NIC_DUPLEX_FULL = 2
    NIC_DUPLEX_HALF = 1
    NIC_DUPLEX_UNKNOWN = 0

POWER_TIME_UNKNOWN: int
POWER_TIME_UNLIMITED: int

class BatteryTime(enum.IntEnum):
    POWER_TIME_UNKNOWN = -1
    POWER_TIME_UNLIMITED = -2

ENCODING: str
ENCODING_ERRS: str

class sswap(NamedTuple):
    """sswap(total, used, free, percent, sin, sout)"""

    total: int
    used: int
    free: int
    percent: float
    sin: int
    sout: int

class sdiskusage(NamedTuple):
    """sdiskusage(total, used, free, percent)"""

    total: int
    used: int
    free: int
    percent: float

class sdiskio(NamedTuple):
    """sdiskio(read_count, write_count, read_bytes, write_bytes, read_time, write_time)"""

    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    read_time: int
    write_time: int

class sdiskpart(NamedTuple):
    """sdiskpart(device, mountpoint, fstype, opts)"""

    device: str
    mountpoint: str
    fstype: str
    opts: str

class snetio(NamedTuple):
    """snetio(bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)"""

    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int

class suser(NamedTuple):
    """suser(name, terminal, host, started, pid)"""

    name: str
    terminal: str | None
    host: str | None
    started: float
    pid: str

class sconn(NamedTuple):
    """sconn(fd, family, type, laddr, raddr, status, pid)"""

    fd: int
    family: AddressFamily
    type: SocketKind
    laddr: addr | tuple[()]
    raddr: addr | tuple[()]
    status: str
    pid: int | None

class snicaddr(NamedTuple):
    """snicaddr(family, address, netmask, broadcast, ptp)"""

    family: AddressFamily
    address: str
    netmask: str | None
    broadcast: str | None
    ptp: str | None

class snicstats(NamedTuple):
    """snicstats(isup, duplex, speed, mtu, flags)"""

    isup: bool
    duplex: int
    speed: int
    mtu: int
    flags: str

class scpustats(NamedTuple):
    """scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)"""

    ctx_switches: int
    interrupts: int
    soft_interrupts: int
    syscalls: int

class scpufreq(NamedTuple):
    """scpufreq(current, min, max)"""

    current: float
    min: float
    max: float

class shwtemp(NamedTuple):
    """shwtemp(label, current, high, critical)"""

    label: str
    current: float
    high: float | None
    critical: float | None

class sbattery(NamedTuple):
    """sbattery(percent, secsleft, power_plugged)"""

    percent: int
    secsleft: int
    power_plugged: bool

class sfan(NamedTuple):
    """sfan(label, current)"""

    label: str
    current: int

class pcputimes(NamedTuple):
    """pcputimes(user, system, children_user, children_system)"""

    user: float
    system: float
    children_user: float
    children_system: float

class popenfile(NamedTuple):
    """popenfile(path, fd)"""

    path: str
    fd: int

class pthread(NamedTuple):
    """pthread(id, user_time, system_time)"""

    id: int
    user_time: float
    system_time: float

class puids(NamedTuple):
    """puids(real, effective, saved)"""

    real: int
    effective: int
    saved: int

class pgids(NamedTuple):
    """pgids(real, effective, saved)"""

    real: int
    effective: int
    saved: int

class pio(NamedTuple):
    """pio(read_count, write_count, read_bytes, write_bytes)"""

    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int

class pionice(NamedTuple):
    """pionice(ioclass, value)"""

    ioclass: int
    value: int

class pctxsw(NamedTuple):
    """pctxsw(voluntary, involuntary)"""

    voluntary: int
    involuntary: int

class pconn(NamedTuple):
    """pconn(fd, family, type, laddr, raddr, status)"""

    fd: int
    family: AddressFamily
    type: SocketKind
    laddr: addr
    raddr: addr
    status: str

class addr(NamedTuple):
    """addr(ip, port)"""

    ip: str
    port: int

conn_tmap: dict[str, tuple[list[AddressFamily], list[SocketKind]]]

class Error(Exception):
    """Base exception class. All other psutil exceptions inherit
    from this one.
    """

    __module__: str
    msg: Any
    def __init__(self, msg: str = ...) -> None: ...

class NoSuchProcess(Error):
    """Exception raised when a process with a certain PID doesn't
    or no longer exists.
    """

    __module__: str
    pid: Any
    name: Any
    msg: Any
    def __init__(self, pid, name=None, msg=None) -> None: ...

class ZombieProcess(NoSuchProcess):
    """Exception raised when querying a zombie process. This is
    raised on macOS, BSD and Solaris only, and not always: depending
    on the query the OS may be able to succeed anyway.
    On Linux all zombie processes are querable (hence this is never
    raised). Windows doesn't have zombie processes.
    """

    __module__: str
    pid: Any
    ppid: Any
    name: Any
    msg: Any
    def __init__(self, pid, name=None, ppid=None, msg=None) -> None: ...

class AccessDenied(Error):
    """Exception raised when permission to perform an action is denied."""

    __module__: str
    pid: Any
    name: Any
    msg: Any
    def __init__(self, pid=None, name=None, msg=None) -> None: ...

class TimeoutExpired(Error):
    """Raised on Process.wait(timeout) if timeout expires and process
    is still alive.
    """

    __module__: str
    seconds: Any
    pid: Any
    name: Any
    def __init__(self, seconds, pid=None, name=None) -> None: ...

_Func = TypeVar("_Func", bound=Callable[..., Any])

def usage_percent(used, total, round_: int | None = None) -> float:
    """Calculate percentage usage of 'used' against 'total'."""

def memoize(fun: _Func) -> _Func:
    """A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>

    It supports:
     - functions
     - classes (acts as a @singleton)
     - staticmethods
     - classmethods

    It does NOT support:
     - methods
    """

def memoize_when_activated(fun: _Func) -> _Func:
    """A memoize decorator which is disabled by default. It can be
    activated and deactivated on request.
    For efficiency reasons it can be used only against class methods
    accepting no arguments.

    >>> class Foo:
    ...     @memoize
    ...     def foo()
    ...         print(1)
    ...
    >>> f = Foo()
    >>> # deactivated (default)
    >>> foo()
    1
    >>> foo()
    1
    >>>
    >>> # activated
    >>> foo.cache_activate(self)
    >>> foo()
    1
    >>> foo()
    >>> foo()
    >>>
    """

def isfile_strict(path: StrOrBytesPath) -> bool:
    """Same as os.path.isfile() but does not swallow EACCES / EPERM
    exceptions, see:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html.
    """

def path_exists_strict(path: StrOrBytesPath) -> bool:
    """Same as os.path.exists() but does not swallow EACCES / EPERM
    exceptions. See:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html.
    """

def supports_ipv6() -> bool:
    """Return True if IPv6 is supported on this platform."""

def parse_environ_block(data):
    """Parse a C environ block of environment variables into a dictionary."""

def sockfam_to_enum(num: int) -> AddressFamily:
    """Convert a numeric socket family value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """

def socktype_to_enum(num: int) -> SocketKind:
    """Convert a numeric socket type value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """

@overload
def conn_to_ntuple(fd: int, fam: int, type_: int, laddr, raddr, status: str, status_map, pid: int) -> sconn:
    """Convert a raw connection tuple to a proper ntuple."""

@overload
def conn_to_ntuple(fd: int, fam: int, type_: int, laddr, raddr, status: str, status_map, pid: None = None) -> pconn: ...
def deprecated_method(replacement: str) -> Callable[[_Func], _Func]:
    """A decorator which can be used to mark a method as deprecated
    'replcement' is the method name which will be called instead.
    """

class _WrapNumbers:
    """Watches numbers so that they don't overflow and wrap
    (reset to zero).
    """

    lock: Any
    cache: Any
    reminders: Any
    reminder_keys: Any
    def __init__(self) -> None: ...
    def run(self, input_dict, name):
        """Cache dict and sum numbers which overflow and wrap.
        Return an updated copy of `input_dict`.
        """

    def cache_clear(self, name=None) -> None:
        """Clear the internal cache, optionally only for function 'name'."""

    def cache_info(self):
        """Return internal cache dicts as a tuple of 3 elements."""

def wrap_numbers(input_dict, name: str):
    """Given an `input_dict` and a function `name`, adjust the numbers
    which "wrap" (restart from zero) across different calls by adding
    "old value" to "new value" and return an updated dict.
    """

def open_binary(fname): ...
def open_text(fname):
    """Open a file in text mode by using the proper FS encoding and
    en/decoding error handlers.
    """

def cat(fname, fallback=..., _open=...):
    """Read entire file content and return it as a string. File is
    opened in text mode. If specified, `fallback` is the value
    returned in case of error, either if the file does not exist or
    it can't be read().
    """

def bcat(fname, fallback=...):
    """Same as above but opens file in binary mode."""

def bytes2human(n: int, format: str = "%(value).1f%(symbol)s") -> str:
    """Used by various scripts. See: https://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/?in=user-4178764.

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'
    """

def get_procfs_path() -> str:
    """Return updated psutil.PROCFS_PATH constant."""

def term_supports_colors(file: SupportsWrite[str] = ...) -> bool: ...
def hilite(s: str, color: str | None = None, bold: bool = False) -> str:
    """Return an highlighted version of 'string'."""

def print_color(s: str, color: str | None = None, bold: bool = False, file: SupportsWrite[str] = ...) -> None:
    """Print a colorized version of string."""

def debug(msg) -> None:
    """If PSUTIL_DEBUG env var is set, print a debug message to stderr."""

__all__ = [
    # OS constants
    "FREEBSD",
    "BSD",
    "LINUX",
    "NETBSD",
    "OPENBSD",
    "MACOS",
    "OSX",
    "POSIX",
    "SUNOS",
    "WINDOWS",
    # connection constants
    "CONN_CLOSE",
    "CONN_CLOSE_WAIT",
    "CONN_CLOSING",
    "CONN_ESTABLISHED",
    "CONN_FIN_WAIT1",
    "CONN_FIN_WAIT2",
    "CONN_LAST_ACK",
    "CONN_LISTEN",
    "CONN_NONE",
    "CONN_SYN_RECV",
    "CONN_SYN_SENT",
    "CONN_TIME_WAIT",
    # net constants
    "NIC_DUPLEX_FULL",
    "NIC_DUPLEX_HALF",
    "NIC_DUPLEX_UNKNOWN",
    # process status constants
    "STATUS_DEAD",
    "STATUS_DISK_SLEEP",
    "STATUS_IDLE",
    "STATUS_LOCKED",
    "STATUS_RUNNING",
    "STATUS_SLEEPING",
    "STATUS_STOPPED",
    "STATUS_SUSPENDED",
    "STATUS_TRACING_STOP",
    "STATUS_WAITING",
    "STATUS_WAKE_KILL",
    "STATUS_WAKING",
    "STATUS_ZOMBIE",
    "STATUS_PARKED",
    # other constants
    "ENCODING",
    "ENCODING_ERRS",
    "AF_INET6",
    # named tuples
    "pconn",
    "pcputimes",
    "pctxsw",
    "pgids",
    "pio",
    "pionice",
    "popenfile",
    "pthread",
    "puids",
    "sconn",
    "scpustats",
    "sdiskio",
    "sdiskpart",
    "sdiskusage",
    "snetio",
    "snicaddr",
    "snicstats",
    "sswap",
    "suser",
    # utility functions
    "conn_tmap",
    "deprecated_method",
    "isfile_strict",
    "memoize",
    "parse_environ_block",
    "path_exists_strict",
    "usage_percent",
    "supports_ipv6",
    "sockfam_to_enum",
    "socktype_to_enum",
    "wrap_numbers",
    "open_text",
    "open_binary",
    "cat",
    "bcat",
    "bytes2human",
    "conn_to_ntuple",
    "debug",
    # shell utils
    "hilite",
    "term_supports_colors",
    "print_color",
]
