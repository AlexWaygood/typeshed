"""
Low-level utilities.
"""

from _typeshed import SupportsWrite
from collections.abc import Callable
from types import TracebackType
from typing import Any, Generic, TypeVar
from typing_extensions import ParamSpec, Self

from gevent.hub import Hub
from greenlet import greenlet as greenlet_t

_T = TypeVar("_T")
_P = ParamSpec("_P")

class wrap_errors(Generic[_P, _T]):
    """
    Helper to make function return an exception, rather than raise it.

    Because every exception that is unhandled by greenlet will be logged,
    it is desirable to prevent non-error exceptions from leaving a greenlet.
    This can done with a simple ``try/except`` construct::

        def wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError) as ex:
                return ex

    This class provides a shortcut to write that in one line::

        wrapped_func = wrap_errors((TypeError, ValueError, AttributeError), func)

    It also preserves ``__str__`` and ``__repr__`` of the original function.
    """

    def __init__(self, errors: tuple[type[BaseException], ...], func: Callable[_P, _T]) -> None:
        """
        Calling this makes a new function from *func*, such that it catches *errors* (an
        :exc:`BaseException` subclass, or a tuple of :exc:`BaseException` subclasses) and
        return it as a value.
        """

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def __getattr__(self, name: str) -> Any: ...

def print_run_info(
    thread_stacks: bool = True, greenlet_stacks: bool = True, limit: int | None = ..., file: SupportsWrite[str] | None = None
) -> None:
    """
    Call `format_run_info` and print the results to *file*.

    If *file* is not given, `sys.stderr` will be used.

    .. versionadded:: 1.3b1
    """

def format_run_info(
    thread_stacks: bool = True, greenlet_stacks: bool = True, limit: int | None = ..., current_thread_ident: int | None = None
) -> None:
    """
    format_run_info(thread_stacks=True, greenlet_stacks=True, limit=None) -> [str]

    Request information about the running threads of the current process.

    This is a debugging utility. Its output has no guarantees other than being
    intended for human consumption.

    :keyword bool thread_stacks: If true, then include the stacks for
       running threads.
    :keyword bool greenlet_stacks: If true, then include the stacks for
       running greenlets. (Spawning stacks will always be printed.)
       Setting this to False can reduce the output volume considerably
       without reducing the overall information if *thread_stacks* is true
       and you can associate a greenlet to a thread (using ``thread_ident``
       printed values).
    :keyword int limit: If given, passed directly to `traceback.format_stack`.
       If not given, this defaults to the whole stack under CPython, and a
       smaller stack under PyPy.

    :return: A sequence of text lines detailing the stacks of running
            threads and greenlets. (One greenlet will duplicate one thread,
            the current thread and greenlet. If there are multiple running threads,
            the stack for the current greenlet may be incorrectly duplicated in multiple
            greenlets.)
            Extra information about
            :class:`gevent.Greenlet` object will also be returned.

    .. versionadded:: 1.3a1
    .. versionchanged:: 1.3a2
       Renamed from ``dump_stacks`` to reflect the fact that this
       prints additional information about greenlets, including their
       spawning stack, parent, locals, and any spawn tree locals.
    .. versionchanged:: 1.3b1
       Added the *thread_stacks*, *greenlet_stacks*, and *limit* params.
    """

class GreenletTree:
    """
    Represents a tree of greenlets.

    In gevent, the *parent* of a greenlet is usually the hub, so this
    tree is primarily arganized along the *spawning_greenlet* dimension.

    This object has a small str form showing this hierarchy. The `format`
    method can output more details. The exact output is unspecified but is
    intended to be human readable.

    Use the `forest` method to get the root greenlet trees for
    all threads, and the `current_tree` to get the root greenlet tree for
    the current thread.
    """

    greenlet: greenlet_t | None
    is_current_tree: bool
    child_trees: list[GreenletTree]
    DEFAULT_DETAILS: dict[str, Any]
    def __init__(self, greenlet: greenlet_t | None) -> None: ...
    def add_child(self, tree: GreenletTree) -> None: ...
    @property
    def root(self) -> bool: ...
    def __getattr__(self, name: str) -> Any: ...
    def format_lines(self, details: bool | dict[str, Any] = True) -> str:
        """
        Return a sequence of lines for the greenlet tree.

        :keyword bool details: If true (the default),
            then include more informative details in the output.
        """

    def format(self, details: bool | dict[str, Any] = True) -> str:
        """
        Like `format_lines` but returns a string.
        """

    @classmethod
    def forest(cls) -> list[GreenletTree]:
        """
        forest() -> sequence

        Return a sequence of `GreenletTree`, one for each running
        native thread.
        """

    @classmethod
    def current_tree(cls) -> GreenletTree:
        """
        current_tree() -> GreenletTree

        Returns the `GreenletTree` for the current thread.
        """

class assert_switches:
    """
    A context manager for ensuring a block of code switches greenlets.

    This performs a similar function as the :doc:`monitoring thread
    </monitoring>`, but the scope is limited to the body of the with
    statement. If the code within the body doesn't yield to the hub
    (and doesn't raise an exception), then upon exiting the
    context manager an :exc:`AssertionError` will be raised.

    This is useful in unit tests and for debugging purposes.

    :keyword float max_blocking_time: If given, the body is allowed
        to block for up to this many fractional seconds before
        an error is raised.
    :keyword bool hub_only: If True, then *max_blocking_time* only
        refers to the amount of time spent between switches into the
        hub. If False, then it refers to the maximum time between
        *any* switches. If *max_blocking_time* is not given, has no
        effect.

    Example::

        # This will always raise an exception: nothing switched
        with assert_switches():
            pass

        # This will never raise an exception; nothing switched,
        # but it happened very fast
        with assert_switches(max_blocking_time=1.0):
            pass

    .. versionadded:: 1.3

    .. versionchanged:: 1.4
        If an exception is raised, it now includes information about
        the duration of blocking and the parameters of this object.
    """

    hub: Hub | None
    tracer: object | None
    max_blocking_time: float | None
    hub_only: bool
    def __init__(self, max_blocking_time: float | None = None, hub_only: bool = False) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None: ...

__all__ = ["format_run_info", "print_run_info", "GreenletTree", "wrap_errors", "assert_switches"]
