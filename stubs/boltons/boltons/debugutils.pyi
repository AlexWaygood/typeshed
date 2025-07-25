"""
A small set of utilities useful for debugging misbehaving
applications. Currently this focuses on ways to use :mod:`pdb`, the
built-in Python debugger.
"""

from collections.abc import Callable
from typing import Any

def pdb_on_signal(signalnum: int | None = None) -> None:
    """Installs a signal handler for *signalnum*, which defaults to
    ``SIGINT``, or keyboard interrupt/ctrl-c. This signal handler
    launches a :mod:`pdb` breakpoint. Results vary in concurrent
    systems, but this technique can be useful for debugging infinite
    loops, or easily getting into deep call stacks.

    Args:
        signalnum (int): The signal number of the signal to handle
            with pdb. Defaults to :mod:`signal.SIGINT`, see
            :mod:`signal` for more information.
    """

def pdb_on_exception(limit: int = 100) -> None:
    """Installs a handler which, instead of exiting, attaches a
    post-mortem pdb console whenever an unhandled exception is
    encountered.

    Args:
        limit (int): the max number of stack frames to display when
            printing the traceback

    A similar effect can be achieved from the command-line using the
    following command::

      python -m pdb your_code.py

    But ``pdb_on_exception`` allows you to do this conditionally and within
    your application. To restore default behavior, just do::

      sys.excepthook = sys.__excepthook__
    """

def wrap_trace(
    obj, hook: Callable[..., Any] = ..., which: str | None = None, events: str | None = None, label: str | None = None
):
    """Monitor an object for interactions. Whenever code calls a method,
    gets an attribute, or sets an attribute, an event is called. By
    default the trace output is printed, but a custom tracing *hook*
    can be passed.

    Args:
       obj (object): New- or old-style object to be traced. Built-in
           objects like lists and dicts also supported.
       hook (callable): A function called once for every event. See
           below for details.
       which (str): One or more attribute names to trace, or a
           function accepting attribute name and value, and returning
           True/False.
       events (str): One or more kinds of events to call *hook*
           on. Expected values are ``['get', 'set', 'del', 'call',
           'raise', 'return']``. Defaults to all events.
       label (str): A name to associate with the traced object
           Defaults to hexadecimal memory address, similar to repr.

    The object returned is not the same object as the one passed
    in. It will not pass identity checks. However, it will pass
    :func:`isinstance` checks, as it is a new instance of a new
    subtype of the object passed.

    """

__all__ = ["pdb_on_signal", "pdb_on_exception", "wrap_trace"]
