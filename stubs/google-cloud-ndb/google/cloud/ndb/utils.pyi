"""Low-level utilities used internally by ``ndb``"""

import threading
from typing import Any

TRUTHY_STRINGS: Any

def asbool(value):
    """Convert an arbitrary value to a boolean.
    Usually, `value`, will be a string. If `value` is already a boolean, it's
    just returned as-is.

    Returns:
        bool: `value` if `value` is a bool, `False` if `value` is `None`,
            otherwise `True` if `value` converts to a lowercase string that is
            "truthy" or `False` if it does not.
    """

DEBUG: Any

def code_info(*args, **kwargs) -> None: ...
def decorator(*args, **kwargs) -> None: ...
def frame_info(*args, **kwargs) -> None: ...
def func_info(*args, **kwargs) -> None: ...
def gen_info(*args, **kwargs) -> None: ...
def get_stack(*args, **kwargs) -> None: ...
def logging_debug(log, message, *args, **kwargs) -> None:
    """Conditionally write to the debug log.

    In some Google App Engine environments, writing to the debug log is a
    significant performance hit. If the environment variable `NDB_DEBUG` is set
    to a "truthy" value, this function will call `log.debug(message, *args,
    **kwargs)`, otherwise this is a no-op.
    """

class keyword_only:
    """A decorator to get some of the functionality of keyword-only arguments
    from Python 3. It takes allowed keyword args and default values as
    parameters. Raises TypeError if a keyword argument not included in those
    parameters is passed in.
    """

    defaults: Any
    def __init__(self, **kwargs) -> None: ...
    def __call__(self, wrapped): ...

def positional(max_pos_args):
    """A decorator to declare that only the first N arguments may be
    positional. Note that for methods, n includes 'self'. This decorator
    retains TypeError functionality from previous version, but adds two
    attributes that can be used in combination with other decorators that
    depend on inspect.signature, only available in Python 3. Note that this
    decorator has to be closer to the function definition than other decorators
    that need to access `_positional_names` or `_positional_args`.
    """

threading_local = threading.local

def tweak_logging(*args, **kwargs) -> None: ...
def wrapping(*args, **kwargs) -> None:
    """Use functools.wraps instead"""
