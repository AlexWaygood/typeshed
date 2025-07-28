from collections.abc import Callable
from types import TracebackType
from typing import TypeVar
from typing_extensions import ParamSpec, Self

_AC = TypeVar("_AC", bound=Callable[..., object])
_R = TypeVar("_R")
_P = ParamSpec("_P")

class Python:
    """
    Start and connect to a separate Python subprocess.

    This is the lowest level of public API provided by this module. The advantage of using this class directly is
    that it allows multiple functions to be evaluated in a single subprocess, making it faster than multiple calls to
    :func:`call`.

    The ``strict_mode`` argument controls behavior when the child process fails to shut down; if strict mode is enabled,
    an error is raised, otherwise only warning is logged. If the value of ``strict_mode`` is ``None``, the value of
    ``PyInstaller.compat.strict_collect_mode`` is used (which in turn is controlled by the
    ``PYINSTALLER_STRICT_COLLECT_MODE`` environment variable.

    Examples:
        To call some predefined functions ``x = foo()``, ``y = bar("numpy")`` and ``z = bazz(some_flag=True)`` all using
        the same isolated subprocess use::

            with isolated.Python() as child:
                x = child.call(foo)
                y = child.call(bar, "numpy")
                z = child.call(bazz, some_flag=True)

    """

    def __init__(self, strict_mode: bool | None = None) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def call(self, function: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
        """
        Call a function in the child Python. Retrieve its return value. Usage of this method is identical to that
        of the :func:`call` function.
        """

def call(function: Callable[_P, _R], *args: _P.args, **kwargs: _P.kwargs) -> _R:
    """
    Call a function with arguments in a separate child Python. Retrieve its return value.

    Args:
        function:
            The function to send and invoke.
        *args:
        **kwargs:
            Positional and keyword arguments to send to the function. These must be simple builtin types - not custom
            classes.
    Returns:
        The return value of the function. Again, these must be basic types serialisable by :func:`marshal.dumps`.
    Raises:
        RuntimeError:
            Any exception which happens inside an isolated process is caught and reraised in the parent process.

    To use, define a function which returns the information you're looking for. Any imports it requires must happen in
    the body of the function. For example, to safely check the output of ``matplotlib.get_data_path()`` use::

        # Define a function to be ran in isolation.
        def get_matplotlib_data_path():
            import matplotlib
            return matplotlib.get_data_path()

        # Call it with isolated.call().
        get_matplotlib_data_path = isolated.call(matplotlib_data_path)

    For single use functions taking no arguments like the above you can abuse the decorator syntax slightly to define
    and execute a function in one go. ::

        >>> @isolated.call
        ... def matplotlib_data_dir():
        ...     import matplotlib
        ...     return matplotlib.get_data_path()
        >>> matplotlib_data_dir
        '/home/brenainn/.pyenv/versions/3.9.6/lib/python3.9/site-packages/matplotlib/mpl-data'

    Functions may take positional and keyword arguments and return most generic Python data types. ::

        >>> def echo_parameters(*args, **kwargs):
        ...     return args, kwargs
        >>> isolated.call(echo_parameters, 1, 2, 3)
        (1, 2, 3), {}
        >>> isolated.call(echo_parameters, foo=["bar"])
        (), {'foo': ['bar']}

    Notes:
        To make a function behave differently if it's isolated, check for the ``__isolated__`` global. ::

            if globals().get("__isolated__", False):
                # We're inside a child process.
                ...
            else:
                # This is the master process.
                ...

    """

def decorate(function: _AC) -> _AC:
    """
    Decorate a function so that it is always called in an isolated subprocess.

    Examples:

        To use, write a function then prepend ``@isolated.decorate``. ::

            @isolated.decorate
            def add_1(x):
                '''Add 1 to ``x``, displaying the current process ID.'''
                import os
                print(f"Process {os.getpid()}: Adding 1 to {x}.")
                return x + 1

        The resultant ``add_1()`` function can now be called as you would a
        normal function and it'll automatically use a subprocess.

            >>> add_1(4)
            Process 4920: Adding 1 to 4.
            5
            >>> add_1(13.2)
            Process 4928: Adding 1 to 13.2.
            14.2

    """
