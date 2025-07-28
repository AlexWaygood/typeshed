import sys
from collections.abc import Callable
from contextvars import Context
from types import FrameType, TracebackType
from typing import Any, Literal, Protocol, overload
from typing_extensions import TypeAlias

_TraceEvent: TypeAlias = Literal["switch", "throw"]
_TraceCallback: TypeAlias = Callable[[_TraceEvent, tuple[greenlet, greenlet]], object]

CLOCKS_PER_SEC: int
GREENLET_USE_CONTEXT_VARS: bool
GREENLET_USE_GC: bool
GREENLET_USE_STANDARD_THREADING: bool
GREENLET_USE_TRACING: bool
# this is a PyCapsule, it may be used to pass the gevent C-API to another C-extension
# there isn't a runtime type for this, since it's only an opaque wrapper around void*
# but it's probably still better than pretending it doesn't exist, so people that need
# to pass this around, can still pass it around without having to ignore type errors...
_C_API: object

class _ParentDescriptor(Protocol):
    def __get__(self, obj: greenlet, owner: type[greenlet] | None = None) -> greenlet | None: ...
    def __set__(self, obj: greenlet, value: greenlet) -> None: ...

class GreenletExit(BaseException): ...
class error(Exception): ...

class greenlet:
    """greenlet(run=None, parent=None) -> greenlet

    Creates a new greenlet object (without running it).

     - *run* -- The callable to invoke.
     - *parent* -- The parent greenlet. The default is the current greenlet.
    """

    @property
    def dead(self) -> bool: ...
    @property
    def gr_context(self) -> Context | None: ...
    @gr_context.setter
    def gr_context(self, value: Context | None) -> None: ...
    @property
    def gr_frame(self) -> FrameType | None: ...
    # the parent attribute is a bit special, since it can't be set to `None` manually, but
    # it can be `None` for the master greenlet which will always be around, regardless of
    # how many greenlets have been spawned explicitly. Since there can only be one such
    # greenlet per thread, there is no way to create another one manually.
    parent: _ParentDescriptor
    @property
    def run(self) -> Callable[..., Any]: ...
    @run.setter
    def run(self, value: Callable[..., Any]) -> None: ...
    def __init__(self, run: Callable[..., Any] | None = None, parent: greenlet | None = None) -> None: ...
    def switch(self, *args: Any, **kwargs: Any) -> Any:
        """switch(*args, **kwargs)

        Switch execution to this greenlet.

        If this greenlet has never been run, then this greenlet
        will be switched to using the body of ``self.run(*args, **kwargs)``.

        If the greenlet is active (has been run, but was switch()'ed
        out before leaving its run function), then this greenlet will
        be resumed and the return value to its switch call will be
        None if no arguments are given, the given argument if one
        argument is given, or the args tuple and keyword args dict if
        multiple arguments are given.

        If the greenlet is dead, or is the current greenlet then this
        function will simply return the arguments using the same rules as
        above.
        """

    @overload
    def throw(
        self, typ: type[BaseException] = ..., val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> Any:
        """Switches execution to this greenlet, but immediately raises the
        given exception in this greenlet.  If no argument is provided, the exception
        defaults to `greenlet.GreenletExit`.  The normal exception
        propagation rules apply, as described for `switch`.  Note that calling this
        method is almost equivalent to the following::

            def raiser():
                raise typ, val, tb
            g_raiser = greenlet(raiser, parent=g)
            g_raiser.switch()

        except that this trick does not work for the
        `greenlet.GreenletExit` exception, which would not propagate
        from ``g_raiser`` to ``g``.
        """

    @overload
    def throw(self, typ: BaseException = ..., val: None = None, tb: TracebackType | None = None, /) -> Any: ...
    def __bool__(self) -> bool:
        """True if self else False"""
    # aliases for some module attributes/methods
    GreenletExit: type[GreenletExit]
    error: type[error]
    @staticmethod
    def getcurrent() -> greenlet:
        """getcurrent() -> greenlet

        Returns the current greenlet (i.e. the one which called this function).
        """

    @staticmethod
    def gettrace() -> _TraceCallback | None:
        """gettrace() -> object

        Returns the currently set tracing function, or None.
        """

    @staticmethod
    def settrace(callback: _TraceCallback | None, /) -> _TraceCallback | None:
        """settrace(callback) -> object

        Sets a new tracing function and returns the previous one.
        """

class UnswitchableGreenlet(greenlet):  # undocumented
    """Undocumented internal class"""

    force_switch_error: bool
    force_slp_switch_error: bool

def enable_optional_cleanup(enabled: bool, /) -> None:
    """mod_enable_optional_cleanup(bool) -> None

    Enable or disable optional cleanup operations.
    See ``get_clocks_used_doing_optional_cleanup()`` for details.
    """

def get_clocks_used_doing_optional_cleanup() -> int:
    """get_clocks_used_doing_optional_cleanup() -> Integer

    Get the number of clock ticks the program has used doing optional greenlet cleanup.
    Beginning in greenlet 2.0, greenlet tries to find and dispose of greenlets
    that leaked after a thread exited. This requires invoking Python's garbage collector,
    which may have a performance cost proportional to the number of live objects.
    This function returns the amount of processor time
    greenlet has used to do this. In programs that run with very large amounts of live
    objects, this metric can be used to decide whether the cost of doing this cleanup
    is worth the memory leak being corrected. If not, you can disable the cleanup
    using ``enable_optional_cleanup(False)``.
    The units are arbitrary and can only be compared to themselves (similarly to ``time.clock()``);
    for example, to see how it scales with your heap. You can attempt to convert them into seconds
    by dividing by the value of CLOCKS_PER_SEC.If cleanup has been disabled, returns None.
    This is an implementation specific, provisional API. It may be changed or removed
    in the future.
    .. versionadded:: 2.0
    """

def get_pending_cleanup_count() -> int:
    """get_pending_cleanup_count() -> Integer

    Get the number of greenlet cleanup operations pending. Testing only.
    """

def get_total_main_greenlets() -> int:
    """get_total_main_greenlets() -> Integer

    Quickly return the number of main greenlets that exist. Testing only.
    """

if sys.version_info < (3, 13):
    def get_tstate_trash_delete_nesting() -> int: ...

def getcurrent() -> greenlet:
    """getcurrent() -> greenlet

    Returns the current greenlet (i.e. the one which called this function).
    """

def gettrace() -> _TraceCallback | None:
    """gettrace() -> object

    Returns the currently set tracing function, or None.
    """

def set_thread_local(key: object, value: object, /) -> None:
    """set_thread_local(key, value) -> None

    Set a value in the current thread-local dictionary. Debugging only.
    """

def settrace(callback: _TraceCallback | None, /) -> _TraceCallback | None:
    """settrace(callback) -> object

    Sets a new tracing function and returns the previous one.
    """
