"""`PEP 3101`_ introduced the :meth:`str.format` method, and what
would later be called "new-style" string formatting. For the sake of
explicit correctness, it is probably best to refer to Python's dual
string formatting capabilities as *bracket-style* and
*percent-style*. There is overlap, but one does not replace the
other.

  * Bracket-style is more pluggable, slower, and uses a method.
  * Percent-style is simpler, faster, and uses an operator.

Bracket-style formatting brought with it a much more powerful toolbox,
but it was far from a full one. :meth:`str.format` uses `more powerful
syntax`_, but `the tools and idioms`_ for working with
that syntax are not well-developed nor well-advertised.

``formatutils`` adds several functions for working with bracket-style
format strings:

  * :class:`DeferredValue`: Defer fetching or calculating a value
    until format time.
  * :func:`get_format_args`: Parse the positional and keyword
    arguments out of a format string.
  * :func:`tokenize_format_str`: Tokenize a format string into
    literals and :class:`BaseFormatField` objects.
  * :func:`construct_format_field_str`: Assists in programmatic
    construction of format strings.
  * :func:`infer_positional_format_args`: Converts anonymous
    references in 2.7+ format strings to explicit positional arguments
    suitable for usage with Python 2.6.

.. _more powerful syntax: https://docs.python.org/2/library/string.html#format-string-syntax
.. _the tools and idioms: https://docs.python.org/2/library/string.html#string-formatting
.. _PEP 3101: https://www.python.org/dev/peps/pep-3101/
"""

from collections.abc import Callable
from typing import Generic, TypeVar

_T = TypeVar("_T")

def construct_format_field_str(fname: str | None, fspec: str | None, conv: str | None) -> str:
    """
    Constructs a format field string from the field name, spec, and
    conversion character (``fname``, ``fspec``, ``conv``). See Python
    String Formatting for more info.
    """

def infer_positional_format_args(fstr: str) -> str:
    """Takes format strings with anonymous positional arguments, (e.g.,
    "{}" and {:d}), and converts them into numbered ones for explicitness and
    compatibility with 2.6.

    Returns a string with the inferred positional arguments.
    """

def get_format_args(fstr: str) -> tuple[list[tuple[int, type]], list[tuple[str, type]]]:
    """
    Turn a format string into two lists of arguments referenced by the
    format string. One is positional arguments, and the other is named
    arguments. Each element of the list includes the name and the
    nominal type of the field.

    # >>> get_format_args("{noun} is {1:d} years old{punct}")
    # ([(1, <type 'int'>)], [('noun', <type 'str'>), ('punct', <type 'str'>)])

    # XXX: Py3k
    >>> get_format_args("{noun} is {1:d} years old{punct}") ==         ([(1, int)], [('noun', str), ('punct', str)])
    True
    """

def tokenize_format_str(fstr: str, resolve_pos: bool = True) -> list[str | BaseFormatField]:
    """Takes a format string, turns it into a list of alternating string
    literals and :class:`BaseFormatField` tokens. By default, also
    infers anonymous positional references into explicit, numbered
    positional references. To disable this behavior set *resolve_pos*
    to ``False``.
    """

class BaseFormatField:
    """A class representing a reference to an argument inside of a
    bracket-style format string. For instance, in ``"{greeting},
    world!"``, there is a field named "greeting".

    These fields can have many options applied to them. See the
    Python docs on `Format String Syntax`_ for the full details.

    .. _Format String Syntax: https://docs.python.org/2/library/string.html#string-formatting
    """

    def __init__(self, fname: str, fspec: str = "", conv: str | None = None) -> None: ...
    base_name: str
    fname: str
    subpath: str
    is_positional: bool
    def set_fname(self, fname: str) -> None:
        """Set the field name."""
    subfields: list[str]
    fspec: str
    type_char: str
    type_func: str
    def set_fspec(self, fspec) -> None:
        """Set the field spec."""
    conv: str | None
    conv_func: str | None
    def set_conv(self, conv: str | None) -> None:
        """There are only two built-in converters: ``s`` and ``r``. They are
        somewhat rare and appearlike ``"{ref!r}"``.
        """

    @property
    def fstr(self) -> str:
        """The current state of the field in string format."""

class DeferredValue(Generic[_T]):
    """:class:`DeferredValue` is a wrapper type, used to defer computing
    values which would otherwise be expensive to stringify and
    format. This is most valuable in areas like logging, where one
    would not want to waste time formatting a value for a log message
    which will subsequently be filtered because the message's log
    level was DEBUG and the logger was set to only emit CRITICAL
    messages.

    The :class:``DeferredValue`` is initialized with a callable that
    takes no arguments and returns the value, which can be of any
    type. By default DeferredValue only calls that callable once, and
    future references will get a cached value. This behavior can be
    disabled by setting *cache_value* to ``False``.

    Args:

        func (function): A callable that takes no arguments and
            computes the value being represented.
        cache_value (bool): Whether subsequent usages will call *func*
            again. Defaults to ``True``.

    >>> import sys
    >>> dv = DeferredValue(lambda: len(sys._current_frames()))
    >>> output = "works great in all {0} threads!".format(dv)

    PROTIP: To keep lines shorter, use: ``from formatutils import
    DeferredValue as DV``
    """

    func: Callable[[], _T]
    cache_value: bool
    def __init__(self, func: Callable[[], _T], cache_value: bool = True) -> None: ...
    def get_value(self) -> _T:
        """Computes, optionally caches, and returns the value of the
        *func*. If ``get_value()`` has been called before, a cached
        value may be returned depending on the *cache_value* option
        passed to the constructor.
        """

    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __unicode__(self) -> str: ...
    def __format__(self, fmt: str) -> str: ...

__all__ = [
    "DeferredValue",
    "get_format_args",
    "tokenize_format_str",
    "construct_format_field_str",
    "infer_positional_format_args",
    "BaseFormatField",
]
