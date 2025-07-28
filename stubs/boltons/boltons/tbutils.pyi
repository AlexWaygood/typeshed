"""One of the oft-cited tenets of Python is that it is better to ask
forgiveness than permission. That is, there are many cases where it is
more inclusive and correct to handle exceptions than spend extra lines
and execution time checking for conditions. This philosophy makes good
exception handling features all the more important. Unfortunately
Python's :mod:`traceback` module is woefully behind the times.

The ``tbutils`` module provides two disparate but complementary featuresets:

  1. With :class:`ExceptionInfo` and :class:`TracebackInfo`, the
     ability to extract, construct, manipulate, format, and serialize
     exceptions, tracebacks, and callstacks.
  2. With :class:`ParsedException`, the ability to find and parse tracebacks
     from captured output such as logs and stdout.

There is also the :class:`ContextualTracebackInfo` variant of
:class:`TracebackInfo`, which includes much more information from each
frame of the callstack, including values of locals and neighboring
lines of code.
"""

from collections.abc import Iterable, Iterator, Mapping
from types import FrameType, TracebackType
from typing import Any, Generic, Literal, TypeVar
from typing_extensions import Self

class Callpoint:
    """The Callpoint is a lightweight object used to represent a single
    entry in the code of a call stack. It stores the code-related
    metadata of a given frame. Available attributes are the same as
    the parameters below.

    Args:
        func_name (str): the function name
        lineno (int): the line number
        module_name (str): the module name
        module_path (str): the filesystem path of the module
        lasti (int): the index of bytecode execution
        line (str): the single-line code content (if available)

    """

    func_name: str
    lineno: int
    module_name: str
    module_path: str
    lasti: int
    line: str
    def __init__(
        self, module_name: str, module_path: str, func_name: str, lineno: int, lasti: int, line: str | None = None
    ) -> None: ...
    def to_dict(self) -> dict[str, Any]:
        """Get a :class:`dict` copy of the Callpoint. Useful for serialization."""

    @classmethod
    def from_current(cls, level: int = 1) -> Self:
        """Creates a Callpoint from the location of the calling function."""

    @classmethod
    def from_frame(cls, frame: FrameType) -> Self:
        """Create a Callpoint object from data extracted from the given frame."""

    @classmethod
    def from_tb(cls, tb: TracebackType) -> Self:
        """Create a Callpoint from the traceback of the current
        exception. Main difference with :meth:`from_frame` is that
        ``lineno`` and ``lasti`` come from the traceback, which is to
        say the line that failed in the try block, not the line
        currently being executed (in the except block).
        """

    def tb_frame_str(self) -> str:
        """Render the Callpoint as it would appear in a standard printed
        Python traceback. Returns a string with filename, line number,
        function name, and the actual code line of the error on up to
        two lines.
        """

_CallpointT_co = TypeVar("_CallpointT_co", bound=Callpoint, covariant=True, default=Callpoint)

class TracebackInfo(Generic[_CallpointT_co]):
    """The TracebackInfo class provides a basic representation of a stack
    trace, be it from an exception being handled or just part of
    normal execution. It is basically a wrapper around a list of
    :class:`Callpoint` objects representing frames.

    Args:
        frames (list): A list of frame objects in the stack.

    .. note ::

      ``TracebackInfo`` can represent both exception tracebacks and
      non-exception tracebacks (aka stack traces). As a result, there
      is no ``TracebackInfo.from_current()``, as that would be
      ambiguous. Instead, call :meth:`TracebackInfo.from_frame`
      without the *frame* argument for a stack trace, or
      :meth:`TracebackInfo.from_traceback` without the *tb* argument
      for an exception traceback.
    """

    callpoint_type: type[_CallpointT_co]
    frames: list[_CallpointT_co]
    def __init__(self, frames: list[_CallpointT_co]) -> None: ...
    @classmethod
    def from_frame(cls, frame: FrameType | None = None, level: int = 1, limit: int | None = None) -> Self:
        """Create a new TracebackInfo *frame* by recurring up in the stack a
        max of *limit* times. If *frame* is unset, get the frame from
        :func:`sys._getframe` using *level*.

        Args:
            frame (types.FrameType): frame object from
                :func:`sys._getframe` or elsewhere. Defaults to result
                of :func:`sys.get_frame`.
            level (int): If *frame* is unset, the desired frame is
                this many levels up the stack from the invocation of
                this method. Default ``1`` (i.e., caller of this method).
            limit (int): max number of parent frames to extract
                (defaults to :data:`sys.tracebacklimit`)

        """

    @classmethod
    def from_traceback(cls, tb: TracebackType | None = None, limit: int | None = None) -> Self:
        """Create a new TracebackInfo from the traceback *tb* by recurring
        up in the stack a max of *limit* times. If *tb* is unset, get
        the traceback from the currently handled exception. If no
        exception is being handled, raise a :exc:`ValueError`.

        Args:

            frame (types.TracebackType): traceback object from
                :func:`sys.exc_info` or elsewhere. If absent or set to
                ``None``, defaults to ``sys.exc_info()[2]``, and
                raises a :exc:`ValueError` if no exception is
                currently being handled.
            limit (int): max number of parent frames to extract
                (defaults to :data:`sys.tracebacklimit`)

        """

    @classmethod
    def from_dict(cls, d: Mapping[Literal["frames"], list[_CallpointT_co]]) -> Self:
        """Complements :meth:`TracebackInfo.to_dict`."""

    def to_dict(self) -> dict[str, list[dict[str, _CallpointT_co]]]:
        """Returns a dict with a list of :class:`Callpoint` frames converted
        to dicts.
        """

    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_CallpointT_co]: ...
    def get_formatted(self) -> str:
        """Returns a string as formatted in the traditional Python
        built-in style observable when an exception is not caught. In
        other words, mimics :func:`traceback.format_tb` and
        :func:`traceback.format_stack`.
        """

_TracebackInfoT_co = TypeVar("_TracebackInfoT_co", bound=TracebackInfo, covariant=True, default=TracebackInfo)

class ExceptionInfo(Generic[_TracebackInfoT_co]):
    """An ExceptionInfo object ties together three main fields suitable
    for representing an instance of an exception: The exception type
    name, a string representation of the exception itself (the
    exception message), and information about the traceback (stored as
    a :class:`TracebackInfo` object).

    These fields line up with :func:`sys.exc_info`, but unlike the
    values returned by that function, ExceptionInfo does not hold any
    references to the real exception or traceback. This property makes
    it suitable for serialization or long-term retention, without
    worrying about formatting pitfalls, circular references, or leaking memory.

    Args:

        exc_type (str): The exception type name.
        exc_msg (str): String representation of the exception value.
        tb_info (TracebackInfo): Information about the stack trace of the
            exception.

    Like the :class:`TracebackInfo`, ExceptionInfo is most commonly
    instantiated from one of its classmethods: :meth:`from_exc_info`
    or :meth:`from_current`.
    """

    tb_info_type: type[_TracebackInfoT_co]
    exc_type: str
    exc_msg: str
    tb_info: _TracebackInfoT_co
    def __init__(self, exc_type: str, exc_msg: str, tb_info: _TracebackInfoT_co) -> None: ...
    @classmethod
    def from_exc_info(cls, exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType) -> Self:
        """Create an :class:`ExceptionInfo` object from the exception's type,
        value, and traceback, as returned by :func:`sys.exc_info`. See
        also :meth:`from_current`.
        """

    @classmethod
    def from_current(cls) -> Self:
        """Create an :class:`ExceptionInfo` object from the current exception
        being handled, by way of :func:`sys.exc_info`. Will raise an
        exception if no exception is currently being handled.
        """

    def to_dict(self) -> dict[str, str | dict[str, list[FrameType]]]:
        """Get a :class:`dict` representation of the ExceptionInfo, suitable
        for JSON serialization.
        """

    def get_formatted(self) -> str:
        """Returns a string formatted in the traditional Python
        built-in style observable when an exception is not caught. In
        other words, mimics :func:`traceback.format_exception`.
        """

    def get_formatted_exception_only(self) -> str: ...

class ContextualCallpoint(Callpoint):
    """The ContextualCallpoint is a :class:`Callpoint` subtype with the
    exact same API and storing two additional values:

      1. :func:`repr` outputs for local variables from the Callpoint's scope
      2. A number of lines before and after the Callpoint's line of code

    The ContextualCallpoint is used by the :class:`ContextualTracebackInfo`.
    """

    local_reprs: dict[Any, Any]
    pre_lines: list[str]
    post_lines: list[str]
    def __init__(self, *a, **kw) -> None: ...
    @classmethod
    def from_frame(cls, frame: FrameType) -> Self:
        """Identical to :meth:`Callpoint.from_frame`"""

    @classmethod
    def from_tb(cls, tb: TracebackType) -> Self:
        """Identical to :meth:`Callpoint.from_tb`"""

    def to_dict(self) -> dict[str, Any]:
        """
        Same principle as :meth:`Callpoint.to_dict`, but with the added
        contextual values. With ``ContextualCallpoint.to_dict()``,
        each frame will now be represented like::

          {'func_name': 'print_example',
           'lineno': 0,
           'module_name': 'example_module',
           'module_path': '/home/example/example_module.pyc',
           'lasti': 0,
           'line': 'print "example"',
           'locals': {'variable': '"value"'},
           'pre_lines': ['variable = "value"'],
           'post_lines': []}

        The locals dictionary and line lists are copies and can be mutated
        freely.
        """

class ContextualTracebackInfo(TracebackInfo[ContextualCallpoint]):
    """The ContextualTracebackInfo type is a :class:`TracebackInfo`
    subtype that is used by :class:`ContextualExceptionInfo` and uses
    the :class:`ContextualCallpoint` as its frame-representing
    primitive.
    """

    callpoint_type: type[ContextualCallpoint]

class ContextualExceptionInfo(ExceptionInfo[ContextualTracebackInfo]):
    """The ContextualTracebackInfo type is a :class:`TracebackInfo`
    subtype that uses the :class:`ContextualCallpoint` as its
    frame-representing primitive.

    It carries with it most of the exception information required to
    recreate the widely recognizable "500" page for debugging Django
    applications.
    """

    tb_info_type: type[ContextualTracebackInfo]

def print_exception(
    etype: type[BaseException] | None,
    value: BaseException | None,
    tb: TracebackType | None,
    limit: int | None = None,
    file: str | None = None,
) -> None:
    """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

    This differs from print_tb() in the following ways: (1) if
    traceback is not None, it prints a header "Traceback (most recent
    call last):"; (2) it prints the exception type and value after the
    stack trace; (3) if type is SyntaxError and value has the
    appropriate format, it prints the line where the syntax error
    occurred with a caret on the next line indicating the approximate
    position of the error.
    """

class ParsedException:
    """Stores a parsed traceback and exception as would be typically
    output by :func:`sys.excepthook` or
    :func:`traceback.print_exception`.

    .. note:

       Does not currently store SyntaxError details such as column.

    """

    exc_type: str
    exc_msg: str
    frames: list[FrameType]
    def __init__(self, exc_type_name: str, exc_msg: str, frames: Iterable[Mapping[str, Any]] | None = None) -> None: ...
    @property
    def source_file(self) -> str | None:
        """
        The file path of module containing the function that raised the
        exception, or None if not available.
        """

    def to_dict(self) -> dict[str, str | list[FrameType]]:
        """Get a copy as a JSON-serializable :class:`dict`."""

    def to_string(self) -> str:
        """Formats the exception and its traceback into the standard format,
        as returned by the traceback module.

        ``ParsedException.from_string(text).to_string()`` should yield
        ``text``.

        .. note::

           Note that this method does not output "anchors" (e.g.,
           ``~~~~~^^``), as were added in Python 3.13. See the built-in
           ``traceback`` module if these are necessary.
        """

    @classmethod
    def from_string(cls, tb_str: str) -> Self:
        """Parse a traceback and exception from the text *tb_str*. This text
        is expected to have been decoded, otherwise it will be
        interpreted as UTF-8.

        This method does not search a larger body of text for
        tracebacks. If the first line of the text passed does not
        match one of the known patterns, a :exc:`ValueError` will be
        raised. This method will ignore trailing text after the end of
        the first traceback.

        Args:
            tb_str (str): The traceback text (:class:`unicode` or UTF-8 bytes)
        """

ParsedTB = ParsedException

__all__ = [
    "ExceptionInfo",
    "TracebackInfo",
    "Callpoint",
    "ContextualExceptionInfo",
    "ContextualTracebackInfo",
    "ContextualCallpoint",
    "print_exception",
    "ParsedException",
]
