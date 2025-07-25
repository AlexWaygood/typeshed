"""macOS platform implementation."""

from _typeshed import Incomplete
from typing import Any, NamedTuple

from psutil._common import (
    AccessDenied as AccessDenied,
    NoSuchProcess as NoSuchProcess,
    ZombieProcess as ZombieProcess,
    conn_tmap as conn_tmap,
    conn_to_ntuple as conn_to_ntuple,
    isfile_strict as isfile_strict,
    parse_environ_block as parse_environ_block,
    usage_percent as usage_percent,
)

__extra__all__: Any
PAGESIZE: Any
AF_LINK: Any
TCP_STATUSES: Any
PROC_STATUSES: Any
kinfo_proc_map: Any
pidtaskinfo_map: Any

class scputimes(NamedTuple):
    """scputimes(user, nice, system, idle)"""

    user: float
    nice: float
    system: float
    idle: float

class svmem(NamedTuple):
    """svmem(total, available, percent, used, free, active, inactive, wired)"""

    total: int
    available: int
    percent: float
    used: int
    free: int
    active: int
    inactive: int
    wired: int

class pmem(NamedTuple):
    """pmem(rss, vms, pfaults, pageins)"""

    rss: Any
    vms: Any
    pfaults: Any
    pageins: Any

class pfullmem(NamedTuple):
    """pfullmem(rss, vms, pfaults, pageins, uss)"""

    rss: Incomplete
    vms: Incomplete
    pfaults: Incomplete
    pageins: Incomplete
    uss: Incomplete

def virtual_memory() -> svmem:
    """System virtual memory as a namedtuple."""

def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""

def cpu_times():
    """Return system CPU times as a namedtuple."""

def per_cpu_times():
    """Return system CPU times as a named tuple."""

def cpu_count_logical():
    """Return the number of logical CPUs in the system."""

def cpu_count_cores() -> int | None:
    """Return the number of CPU cores in the system."""

def cpu_stats(): ...
def cpu_freq():
    """Return CPU frequency.
    On macOS per-cpu frequency is not supported.
    Also, the returned frequency never changes, see:
    https://arstechnica.com/civis/viewtopic.php?f=19&t=465002.
    """

disk_usage: Any
disk_io_counters: Any

def disk_partitions(all: bool = ...):
    """Return mounted disk partitions as a list of namedtuples."""

def sensors_battery():
    """Return battery information."""

net_io_counters: Any
net_if_addrs: Any

def net_connections(kind: str = ...):
    """System-wide network connections."""

def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""

def boot_time():
    """The system boot time expressed in seconds since the epoch."""

def users():
    """Return currently connected users as a list of namedtuples."""

def pids(): ...

pid_exists: Any

def is_zombie(pid): ...
def wrap_exceptions(fun):
    """Decorator which translates bare OSError exceptions into
    NoSuchProcess and AccessDenied.
    """

class Process:
    """Wrapper class around underlying C implementation."""

    pid: Any
    def __init__(self, pid) -> None: ...
    def oneshot_enter(self) -> None: ...
    def oneshot_exit(self) -> None: ...
    def name(self): ...
    def exe(self): ...
    def cmdline(self): ...
    def environ(self): ...
    def ppid(self): ...
    def cwd(self): ...
    def uids(self): ...
    def gids(self): ...
    def terminal(self): ...
    def memory_info(self): ...
    def memory_full_info(self): ...
    def cpu_times(self): ...
    def create_time(self): ...
    def num_ctx_switches(self): ...
    def num_threads(self): ...
    def open_files(self): ...
    def net_connections(self, kind: str = ...): ...
    def num_fds(self): ...
    def wait(self, timeout: Incomplete | None = ...): ...
    def nice_get(self): ...
    def nice_set(self, value): ...
    def status(self): ...
    def threads(self): ...
