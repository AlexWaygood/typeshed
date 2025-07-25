"""
gevent tunables.

This should be used as ``from gevent import config``. That variable
is an object of :class:`Config`.

.. versionadded:: 1.3a2

.. versionchanged:: 22.08.0
   Invoking this module like ``python -m gevent._config`` will
   print a help message about available configuration properties.
   This is handy to quickly look for environment variables.
"""

from collections.abc import Callable, Sequence
from typing import Any, Generic, NoReturn, Protocol, TypeVar, overload

from gevent._types import _Loop, _Resolver
from gevent.fileobject import _FileObjectType
from gevent.threadpool import ThreadPool

__all__ = ["config"]

_T = TypeVar("_T")

class _SettingDescriptor(Protocol[_T]):
    @overload
    def __get__(self, obj: None, owner: type[Config]) -> property: ...
    @overload
    def __get__(self, obj: Config, owner: type[Config]) -> _T: ...
    def __set__(self, obj: Config, value: str | _T) -> None: ...

class SettingType(type):
    def fmt_desc(cls, desc: str) -> str: ...

def validate_invalid(value: object) -> NoReturn: ...
def validate_bool(value: str | bool) -> bool:
    """
    This is a boolean value.

    In the environment variable, it may be given as ``1``, ``true``,
    ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
    ``no`` for `False`.
    """

def validate_anything(value: _T) -> _T: ...

convert_str_value_as_is = validate_anything

class Setting(Generic[_T], metaclass=SettingType):
    order: int  # all subclasses have this
    name: str
    environment_key: str
    value: _T
    default: _T
    document: bool
    desc: str
    validate: Callable[[Any], _T]
    def get(self) -> _T: ...
    def set(self, val: str | _T) -> None: ...

class Config:
    """
    Global configuration for gevent.

    There is one instance of this object at ``gevent.config``. If you
    are going to make changes in code, instead of using the documented
    environment variables, you need to make the changes before using
    any parts of gevent that might need those settings (unless otherwise
    documented). For example::

        >>> from gevent import config
        >>> config.fileobject = 'thread'

        >>> from gevent import fileobject
        >>> fileobject.FileObject.__name__
        'FileObjectThread'

    .. versionadded:: 1.3a2

    """

    settings: dict[str, Setting[Any]]
    def __init__(self) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: object) -> None: ...
    def set(self, name: str, value: object) -> None: ...
    def __dir__(self) -> list[str]: ...
    def print_help(self) -> None: ...

    # we manually add properties for all the settings in this module
    # SettingType inserts a property into Config for every subclass of Setting
    resolver: _SettingDescriptor[type[_Resolver]]
    threadpool: _SettingDescriptor[type[Threadpool]]
    threadpool_idle_task_timeout: _SettingDescriptor[float]
    loop: _SettingDescriptor[type[_Loop]]
    format_context: _SettingDescriptor[Callable[[Any], str]]
    libev_backend: _SettingDescriptor[str | None]
    fileobject: _SettingDescriptor[_FileObjectType]
    disable_watch_children: _SettingDescriptor[bool]
    track_greenlet_tree: _SettingDescriptor[bool]
    monitor_thread: _SettingDescriptor[bool]
    max_blocking_time: _SettingDescriptor[float]
    memory_monitor_period: _SettingDescriptor[float]
    max_memory_usage: _SettingDescriptor[int | None]
    resolver_nameservers: _SettingDescriptor[Sequence[str] | str | None]
    resolver_timeout: _SettingDescriptor[float | None]
    # these get parsed by gevent.resolver.cares.channel so the Setting does not
    # perform any conversion, but we know at least what types can be valid
    ares_flags: _SettingDescriptor[str | int | None]
    ares_timeout: _SettingDescriptor[str | float | None]
    ares_tries: _SettingDescriptor[str | int | None]
    ares_ndots: _SettingDescriptor[str | int | None]
    ares_udp_port: _SettingDescriptor[str | int | None]
    ares_tcp_port: _SettingDescriptor[str | int | None]
    ares_servers: _SettingDescriptor[Sequence[str] | str | None]
    print_blocking_reports: _SettingDescriptor[bool]

class ImportableSetting(Generic[_T]):
    default: str | Sequence[str]
    shortname_map: dict[str, str]
    def validate(self, value: str | _T) -> _T: ...
    def get_options(self) -> dict[str, _T]: ...

class BoolSettingMixin:
    @staticmethod
    def validate(value: str | bool) -> bool:
        """
        This is a boolean value.

        In the environment variable, it may be given as ``1``, ``true``,
        ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
        ``no`` for `False`.
        """

class IntSettingMixin:
    @staticmethod
    def validate(value: int) -> int: ...

class _PositiveValueMixin(Generic[_T]):
    @staticmethod
    def validate(value: _T) -> _T: ...

class FloatSettingMixin(_PositiveValueMixin[float]): ...
class ByteCountSettingMixin(_PositiveValueMixin[int]): ...

class Resolver(ImportableSetting[type[_Resolver]], Setting[type[_Resolver]]):
    """The callable that will be used to create
    :attr:`gevent.hub.Hub.resolver`.

    See :doc:`dns` for more information.

    This is an importable value. It can be given as a string naming an importable object, or a list of strings in preference order and the first successfully importable object will be used. (Separate values in the environment variable with commas.) It can also be given as the callable object itself (in code). Shorthand names for default objects are ['ares', 'thread', 'block', 'dnspython']

    The default value is `['thread', 'dnspython', 'ares', 'block']`

    The environment variable ``GEVENT_RESOLVER`` can be used to control this.
    """

    desc: str
    default: list[str]  # type: ignore[assignment]
    shortname_map: dict[str, str]

class Threadpool(ImportableSetting[type[ThreadPool]], Setting[type[ThreadPool]]):
    """The kind of threadpool we use.

    This is an importable value. It can be given as a string naming an importable object, or a list of strings in preference order and the first successfully importable object will be used. (Separate values in the environment variable with commas.) It can also be given as the callable object itself (in code).

    The default value is `gevent.threadpool.ThreadPool`

    The environment variable ``GEVENT_THREADPOOL`` can be used to control this.
    """

    desc: str
    default: str  # type: ignore[assignment]

class ThreadpoolIdleTaskTimeout(FloatSettingMixin, Setting[float]):
    """How long threads in the default threadpool (used for
    DNS by default) are allowed to be idle before exiting.

    Use -1 for no timeout.

    .. versionadded:: 22.08.0

    The default value is `5.0`

    The environment variable ``GEVENT_THREADPOOL_IDLE_TASK_TIMEOUT`` can be used to control this.
    """

    document: bool
    desc: str
    default: float

class Loop(ImportableSetting[type[_Loop]], Setting[type[_Loop]]):
    """The kind of the loop we use.

    On Windows, this defaults to libuv, while on
    other platforms it defaults to libev.

    This is an importable value. It can be given as a string naming an importable object, or a list of strings in preference order and the first successfully importable object will be used. (Separate values in the environment variable with commas.) It can also be given as the callable object itself (in code). Shorthand names for default objects are ['libev-cext', 'libev-cffi', 'libuv-cffi', 'libuv']

    The default value is `['libev-cext', 'libev-cffi', 'libuv-cffi']`

    The environment variable ``GEVENT_LOOP`` can be used to control this.
    """

    desc: str
    default: list[str]  # type: ignore[assignment]
    shortname_map: dict[str, str]

class FormatContext(ImportableSetting[Callable[[Any], str]], Setting[Callable[[Any], str]]):
    """

    This is an importable value. It can be given as a string naming an importable object, or a list of strings in preference order and the first successfully importable object will be used. (Separate values in the environment variable with commas.) It can also be given as the callable object itself (in code).

    The default value is `pprint.saferepr`

    The environment variable ``GEVENT_FORMAT_CONTEXT`` can be used to control this.
    """

    default: str  # type: ignore[assignment]

class LibevBackend(Setting[str | None]):
    """The backend for libev, such as 'select'

    The default value is `None`

    The environment variable ``GEVENT_BACKEND`` can be used to control this.
    """

    desc: str
    default: None

class FileObject(ImportableSetting[_FileObjectType], Setting[_FileObjectType]):
    """The kind of ``FileObject`` we will use.

    See :mod:`gevent.fileobject` for a detailed description.

    This is an importable value. It can be given as a string naming an importable object, or a list of strings in preference order and the first successfully importable object will be used. (Separate values in the environment variable with commas.) It can also be given as the callable object itself (in code). Shorthand names for default objects are ['thread', 'posix', 'block']

    The default value is `['posix', 'thread']`

    The environment variable ``GEVENT_FILE`` can be used to control this.
    """

    desc: str
    default: list[str]  # type: ignore[assignment]
    shortname_map: dict[str, str]

class WatchChildren(BoolSettingMixin, Setting[bool]):
    """Should we *not* watch children with the event loop watchers?

    This is an advanced setting.

    See :mod:`gevent.os` for a detailed description.

    This is a boolean value.

    In the environment variable, it may be given as ``1``, ``true``,
    ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
    ``no`` for `False`.

    The default value is `False`

    The environment variable ``GEVENT_NOWAITPID`` can be used to control this.
    """

    desc: str
    default: bool

class TrackGreenletTree(BoolSettingMixin, Setting[bool]):
    """Should `Greenlet` objects track their spawning tree?

    Setting this to a false value will make spawning `Greenlet`
    objects and using `spawn_raw` faster, but the
    ``spawning_greenlet``, ``spawn_tree_locals`` and ``spawning_stack``
    will not be captured. Setting this to a false value can also
    reduce memory usage because capturing the stack captures
    some information about Python frames.

    .. versionadded:: 1.3b1

    This is a boolean value.

    In the environment variable, it may be given as ``1``, ``true``,
    ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
    ``no`` for `False`.

    The default value is `True`

    The environment variable ``GEVENT_TRACK_GREENLET_TREE`` can be used to control this.
    """

    default: bool
    desc: str

class MonitorThread(BoolSettingMixin, Setting[bool]):
    """Should each hub start a native OS thread to monitor
    for problems?

    Such a thread will periodically check to see if the event loop
    is blocked for longer than `max_blocking_time`, producing output on
    the hub's exception stream (stderr by default) if it detects this condition.

    If this setting is true, then this thread will be created
    the first time the hub is switched to,
    or you can call :meth:`gevent.hub.Hub.start_periodic_monitoring_thread` at any
    time to create it (from the same thread that will run the hub). That function
    will return an instance of :class:`gevent.events.IPeriodicMonitorThread`
    to which you can add your own monitoring functions. That function
    also emits an event of :class:`gevent.events.PeriodicMonitorThreadStartedEvent`.

    .. seealso:: `max_blocking_time`

    .. versionadded:: 1.3b1

    This is a boolean value.

    In the environment variable, it may be given as ``1``, ``true``,
    ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
    ``no`` for `False`.

    The default value is `False`

    The environment variable ``GEVENT_MONITOR_THREAD_ENABLE`` can be used to control this.
    """

    default: bool
    desc: str

class MaxBlockingTime(FloatSettingMixin, Setting[float]):
    """If the `monitor_thread` is enabled, this is
    approximately how long (in seconds)
    the event loop will be allowed to block before a warning is issued.

    This function depends on using `greenlet.settrace`, so installing
    your own trace function after starting the monitoring thread will
    cause this feature to misbehave unless you call the function
    returned by `greenlet.settrace`. If you install a tracing function *before*
    the monitoring thread is started, it will still be called.

    .. note:: In the unlikely event of creating and using multiple different
        gevent hubs in the same native thread in a short period of time,
        especially without destroying the hubs, false positives may be reported.

    .. versionadded:: 1.3b1

    The default value is `0.1`

    The environment variable ``GEVENT_MAX_BLOCKING_TIME`` can be used to control this.
    """

    default: float
    desc: str

class PrintBlockingReports(BoolSettingMixin, Setting[bool]):
    """If `monitor_thread` is enabled, and gevent detects a hub blocked
    for more than `max_blocking_time`, should gevent print a detailed
    report about the block?

    The report is generated and notifications are broadcast whether
    or not the report is printed.

    .. versionadded:: 25.4.1

    This is a boolean value.

    In the environment variable, it may be given as ``1``, ``true``,
    ``on`` or ``yes`` for `True`, or ``0``, ``false``, ``off``, or
    ``no`` for `False`.

    The default value is `True`

    The environment variable ``GEVENT_MONITOR_PRINT_BLOCKING_REPORTS`` can be used to control this.
    """

    default: bool
    desc: str

class MonitorMemoryPeriod(FloatSettingMixin, Setting[float]):
    """If `monitor_thread` is enabled, this is approximately how long
    (in seconds) we will go between checking the processes memory usage.

    Checking the memory usage is relatively expensive on some operating
    systems, so this should not be too low. gevent will place a floor
    value on it.

    The default value is `5`

    The environment variable ``GEVENT_MONITOR_MEMORY_PERIOD`` can be used to control this.
    """

    default: int
    desc: str

class MonitorMemoryMaxUsage(ByteCountSettingMixin, Setting[int | None]):
    """If `monitor_thread` is enabled,
    then if memory usage exceeds this amount (in bytes), events will
    be emitted. See `gevent.events`. In the environment variable, you can use
    a suffix of 'kb', 'mb' or 'gb' to specify the value in kilobytes, megabytes
    or gigibytes.

    There is no default value for this setting. If you wish to
    cap memory usage, you must choose a value.

    The default value is `None`

    The environment variable ``GEVENT_MONITOR_MEMORY_MAX`` can be used to control this.
    """

    default: None
    desc: str

class AresSettingMixin:
    document: bool
    @property
    def kwarg_name(self) -> str: ...
    validate: Any  # we just want this to mixin without errors

class AresFlags(AresSettingMixin, Setting[str | int | None]):
    """

    The default value is `None`

    The environment variable ``GEVENTARES_FLAGS`` can be used to control this.
    """

    default: None

class AresTimeout(AresSettingMixin, Setting[str | float | None]):
    """.. deprecated:: 1.3a2
       Prefer the :attr:`resolver_timeout` setting. If both are set,
       the results are not defined.

    The default value is `None`

    The environment variable ``GEVENTARES_TIMEOUT`` can be used to control this.
    """

    document: bool
    default: None
    desc: str

class AresTries(AresSettingMixin, Setting[str | int | None]):
    """

    The default value is `None`

    The environment variable ``GEVENTARES_TRIES`` can be used to control this.
    """

    default: None

class AresNdots(AresSettingMixin, Setting[str | int | None]):
    """

    The default value is `None`

    The environment variable ``GEVENTARES_NDOTS`` can be used to control this.
    """

    default: None

class AresUDPPort(AresSettingMixin, Setting[str | int | None]):
    """

    The default value is `None`

    The environment variable ``GEVENTARES_UDP_PORT`` can be used to control this.
    """

    default: None

class AresTCPPort(AresSettingMixin, Setting[str | int | None]):
    """

    The default value is `None`

    The environment variable ``GEVENTARES_TCP_PORT`` can be used to control this.
    """

    default: None

class AresServers(AresSettingMixin, Setting[Sequence[str] | str | None]):
    """A list of strings giving the IP addresses of nameservers for the ares resolver.

    In the environment variable, these strings are separated by commas.

    .. deprecated:: 1.3a2
       Prefer the :attr:`resolver_nameservers` setting. If both are set,
       the results are not defined.

    The default value is `None`

    The environment variable ``GEVENTARES_SERVERS`` can be used to control this.
    """

    document: bool
    default: None
    desc: str

class ResolverNameservers(AresSettingMixin, Setting[Sequence[str] | str | None]):
    """A list of strings giving the IP addresses of nameservers for the (non-system) resolver.

    In the environment variable, these strings are separated by commas.

    .. rubric:: Resolver Behaviour

    * blocking

      Ignored

    * Threaded

      Ignored

    * dnspython

      If this setting is not given, the dnspython resolver will
      load nameservers to use from ``/etc/resolv.conf``
      or the Windows registry. This setting replaces any nameservers read
      from those means. Note that the file and registry are still read
      for other settings.

      .. caution:: dnspython does not validate the members of the list.
         An improper address (such as a hostname instead of IP) has
         undefined results, including hanging the process.

    * ares

      Similar to dnspython, but with more platform and compile-time
      options. ares validates that the members of the list are valid
      addresses.

    The default value is `None`

    The environment variable ``GEVENT_RESOLVER_NAMESERVERS`` can be used to control this.
    """

    document: bool
    default: None
    desc: str
    @property
    def kwarg_name(self) -> str: ...

class ResolverTimeout(FloatSettingMixin, AresSettingMixin, Setting[float | None]):
    """The total amount of time that the DNS resolver will spend making queries.

    Only the ares and dnspython resolvers support this.

    .. versionadded:: 1.3a2

    The default value is `None`

    The environment variable ``GEVENT_RESOLVER_TIMEOUT`` can be used to control this.
    """

    document: bool
    desc: str
    @property
    def kwarg_name(self) -> str: ...

config: Config = ...
