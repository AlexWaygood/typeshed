"""
Miscellaneous utilities for the documentation utilities.
"""

import optparse
from _typeshed import StrPath, SupportsWrite, Unused
from collections.abc import Callable, Iterable, Mapping
from re import Pattern
from typing import Any, Final, Literal, TypeVar
from typing_extensions import TypeAlias

from docutils import ApplicationError, DataError, nodes
from docutils.frontend import Values
from docutils.io import ErrorOutput, FileOutput
from docutils.nodes import document, unescape as unescape

_T = TypeVar("_T")
_Observer: TypeAlias = Callable[[nodes.system_message], object]
_SystemMessageLevel: TypeAlias = Literal[0, 1, 2, 3, 4]

__docformat__: Final = "reStructuredText"

class DependencyList:
    """
    List of dependencies, with file recording support.

    Note that the output file is not automatically closed.  You have
    to explicitly call the close() method.
    """

    list: list[str]
    file: FileOutput | None
    def __init__(self, output_file: str | None = None, dependencies: Iterable[str] = ()) -> None:
        """
        Initialize the dependency list, automatically setting the
        output file to `output_file` (see `set_output()`) and adding
        all supplied dependencies.

        If output_file is None, no file output is done when calling add().
        """

    def set_output(self, output_file: str | None) -> None:
        """
        Set the output file and clear the list of already added
        dependencies.

        `output_file` must be a string.  The specified file is
        immediately overwritten.

        If output_file is '-', the output will be written to stdout.
        """

    def add(self, *paths: str) -> None:
        """
        Append `path` to `self.list` unless it is already there.

        Also append to `self.file` unless it is already there
        or `self.file is `None`.
        """

    def close(self) -> None:
        """
        Close the output file.
        """

class SystemMessagePropagation(ApplicationError): ...

class Reporter:
    """
    Info/warning/error reporter and ``system_message`` element generator.

    Five levels of system messages are defined, along with corresponding
    methods: `debug()`, `info()`, `warning()`, `error()`, and `severe()`.

    There is typically one Reporter object per process.  A Reporter object is
    instantiated with thresholds for reporting (generating warnings) and
    halting processing (raising exceptions), a switch to turn debug output on
    or off, and an I/O stream for warnings.  These are stored as instance
    attributes.

    When a system message is generated, its level is compared to the stored
    thresholds, and a warning or error is generated as appropriate.  Debug
    messages are produced if the stored debug switch is on, independently of
    other thresholds.  Message output is sent to the stored warning stream if
    not set to ''.

    The Reporter class also employs a modified form of the "Observer" pattern
    [GoF95]_ to track system messages generated.  The `attach_observer` method
    should be called before parsing, with a bound method or function which
    accepts system messages.  The observer can be removed with
    `detach_observer`, and another added in its place.

    .. [GoF95] Gamma, Helm, Johnson, Vlissides. *Design Patterns: Elements of
       Reusable Object-Oriented Software*. Addison-Wesley, Reading, MA, USA,
       1995.
    """

    levels: list[str]

    DEBUG_LEVEL: Literal[0]
    INFO_LEVEL: Literal[1]
    WARNING_LEVEL: Literal[2]
    ERROR_LEVEL: Literal[3]
    SEVERE_LEVEL: Literal[4]

    stream: ErrorOutput
    encoding: str
    observers: list[_Observer]
    max_level: int
    def __init__(
        self,
        source: str,
        report_level: int,
        halt_level: int,
        stream: SupportsWrite[str] | SupportsWrite[bytes] | str | bool | None = None,
        debug: bool = False,
        encoding: str | None = None,
        error_handler: str = "backslashreplace",
    ) -> None:
        """
        :Parameters:
            - `source`: The path to or description of the source data.
            - `report_level`: The level at or above which warning output will
              be sent to `stream`.
            - `halt_level`: The level at or above which `SystemMessage`
              exceptions will be raised, halting execution.
            - `debug`: Show debug (level=0) system messages?
            - `stream`: Where warning output is sent.  Can be file-like (has a
              ``.write`` method), a string (file name, opened for writing),
              '' (empty string) or `False` (for discarding all stream messages)
              or `None` (implies `sys.stderr`; default).
            - `encoding`: The output encoding.
            - `error_handler`: The error handler for stderr output encoding.
        """
    source: str
    error_handler: str
    debug_flag: bool
    report_level: _SystemMessageLevel
    halt_level: int
    def set_conditions(
        self,
        category: Unused,
        report_level: int,
        halt_level: int,
        stream: SupportsWrite[str] | SupportsWrite[bytes] | None = None,
        debug: bool = False,
    ) -> None: ...
    def attach_observer(self, observer: _Observer) -> None:
        """
        The `observer` parameter is a function or bound method which takes one
        argument, a `nodes.system_message` instance.
        """

    def detach_observer(self, observer: _Observer) -> None: ...
    def notify_observers(self, message: nodes.system_message) -> None: ...
    def system_message(
        self,
        level: int,
        message: str | Exception,
        *children: nodes.Node,
        base_node: nodes.Node = ...,
        source: str = ...,
        **kwargs,
    ) -> nodes.system_message:
        """
        Return a system_message object.

        Raise an exception or generate a warning if appropriate.
        """

    def debug(
        self, message: str | Exception, *children: nodes.Node, base_node: nodes.Node = ..., source: str = ..., **kwargs
    ) -> nodes.system_message:
        """
        Level-0, "DEBUG": an internal reporting issue. Typically, there is no
        effect on the processing. Level-0 system messages are handled
        separately from the others.
        """

    def info(
        self, message: str | Exception, *children: nodes.Node, base_node: nodes.Node = ..., source: str = ..., **kwargs
    ) -> nodes.system_message:
        """
        Level-1, "INFO": a minor issue that can be ignored. Typically there is
        no effect on processing, and level-1 system messages are not reported.
        """

    def warning(
        self, message: str | Exception, *children: nodes.Node, base_node: nodes.Node = ..., source: str = ..., **kwargs
    ) -> nodes.system_message:
        """
        Level-2, "WARNING": an issue that should be addressed. If ignored,
        there may be unpredictable problems with the output.
        """

    def error(
        self, message: str | Exception, *children: nodes.Node, base_node: nodes.Node = ..., source: str = ..., **kwargs
    ) -> nodes.system_message:
        """
        Level-3, "ERROR": an error that should be addressed. If ignored, the
        output will contain errors.
        """

    def severe(
        self, message: str | Exception, *children: nodes.Node, base_node: nodes.Node = ..., source: str = ..., **kwargs
    ) -> nodes.system_message:
        """
        Level-4, "SEVERE": a severe error that must be addressed. If ignored,
        the output will contain severe errors. Typically level-4 system
        messages are turned into exceptions which halt processing.
        """

class SystemMessage(ApplicationError):
    level: _SystemMessageLevel
    def __init__(self, system_message: object, level: _SystemMessageLevel): ...

def new_reporter(source_path: str, settings: optparse.Values) -> Reporter:
    """
    Return a new Reporter object.

    :Parameters:
        `source` : string
            The path to or description of the source text of the document.
        `settings` : optparse.Values object
            Runtime settings.
    """

def new_document(source_path: str, settings: optparse.Values | None = None) -> document:
    """
    Return a new empty document object.

    :Parameters:
        `source_path` : string
            The path to or description of the source text of the document.
        `settings` : optparse.Values object
            Runtime settings.  If none are provided, a default core set will
            be used.  If you will use the document object with any Docutils
            components, you must provide their default settings as well.

            For example, if parsing rST, at least provide the rst-parser
            settings, obtainable as follows:

            Defaults for parser component::

                settings = docutils.frontend.get_default_settings(
                               docutils.parsers.rst.Parser)

            Defaults and configuration file customizations::

                settings = docutils.core.Publisher(
                    parser=docutils.parsers.rst.Parser).get_settings()

    """

class ExtensionOptionError(DataError): ...
class BadOptionError(ExtensionOptionError): ...
class BadOptionDataError(ExtensionOptionError): ...
class DuplicateOptionError(ExtensionOptionError): ...

def extract_extension_options(field_list: nodes.field_list, options_spec: Mapping[str, Callable[[str], Any]]) -> dict[str, Any]:
    """
    Return a dictionary mapping extension option names to converted values.

    :Parameters:
        - `field_list`: A flat field list without field arguments, where each
          field body consists of a single paragraph only.
        - `options_spec`: Dictionary mapping known option names to a
          conversion function such as `int` or `float`.

    :Exceptions:
        - `KeyError` for unknown option names.
        - `ValueError` for invalid option values (raised by the conversion
           function).
        - `TypeError` for invalid option value types (raised by conversion
           function).
        - `DuplicateOptionError` for duplicate options.
        - `BadOptionError` for invalid fields.
        - `BadOptionDataError` for invalid option data (missing name,
          missing data, bad quotes, etc.).
    """

def extract_options(field_list: nodes.field_list) -> list[tuple[str, str]]:
    """
    Return a list of option (name, value) pairs from field names & bodies.

    :Parameter:
        `field_list`: A flat field list, where each field name is a single
        word and each field body consists of a single paragraph only.

    :Exceptions:
        - `BadOptionError` for invalid fields.
        - `BadOptionDataError` for invalid option data (missing name,
          missing data, bad quotes, etc.).
    """

def assemble_option_dict(
    option_list: Iterable[tuple[str, str]], options_spec: Mapping[str, Callable[[str], Any]]
) -> dict[str, Any]:
    """
    Return a mapping of option names to values.

    :Parameters:
        - `option_list`: A list of (name, value) pairs (the output of
          `extract_options()`).
        - `options_spec`: Dictionary mapping known option names to a
          conversion function such as `int` or `float`.

    :Exceptions:
        - `KeyError` for unknown option names.
        - `DuplicateOptionError` for duplicate options.
        - `ValueError` for invalid option values (raised by conversion
           function).
        - `TypeError` for invalid option value types (raised by conversion
           function).
    """

class NameValueError(DataError): ...

def decode_path(path: str) -> str:
    """
    Ensure `path` is Unicode. Return `str` instance.

    Decode file/path string in a failsafe manner if not already done.
    """

def extract_name_value(line: str) -> list[tuple[str, str]]:
    """
    Return a list of (name, value) from a line of the form "name=value ...".

    :Exception:
        `NameValueError` for invalid input (missing name, missing data, bad
        quotes, etc.).
    """

def clean_rcs_keywords(paragraph: nodes.paragraph, keyword_substitutions: Iterable[tuple[Pattern[str], str]]) -> None: ...
def relative_path(source: StrPath | None, target: StrPath) -> str:
    """
    Build and return a path to `target`, relative to `source` (both files).

    The return value is a `str` suitable to be included in `source`
    as a reference to `target`.

    :Parameters:
        `source` : path-like object or None
            Path of a file in the start directory for the relative path
            (the file does not need to exist).
            The value ``None`` is replaced with "<cwd>/dummy_file".
        `target` : path-like object
            End point of the returned relative path.

    Differences to `os.path.relpath()`:

    * Inverse argument order.
    * `source` is assumed to be a FILE in the start directory (add a "dummy"
      file name to obtain the path relative from a directory)
      while `os.path.relpath()` expects a DIRECTORY as `start` argument.
    * Always use Posix path separator ("/") for the output.
    * Use `os.sep` for parsing the input
      (changing the value of `os.sep` is ignored by `os.relpath()`).
    * If there is no common prefix, return the absolute path to `target`.

    Differences to `pathlib.PurePath.relative_to(other)`:

    * pathlib offers an object oriented interface.
    * `source` expects path to a FILE while `other` expects a DIRECTORY.
    * `target` defaults to the cwd, no default value for `other`.
    * `relative_path()` always returns a path (relative or absolute),
      while `PurePath.relative_to()` raises a ValueError
      if `target` is not a subpath of `other` (no ".." inserted).
    """

def get_stylesheet_reference(settings: Values, relative_to: str | None = None) -> str:
    """
    Retrieve a stylesheet reference from the settings object.

    Deprecated. Use get_stylesheet_list() instead to
    enable specification of multiple stylesheets as a comma-separated
    list.
    """

def get_stylesheet_list(settings: Values) -> list[str]:
    """
    Retrieve list of stylesheet references from the settings object.
    """

def find_file_in_dirs(path: StrPath, dirs: Iterable[StrPath]) -> str:
    """
    Search for `path` in the list of directories `dirs`.

    Return the first expansion that matches an existing file.
    """

def get_trim_footnote_ref_space(settings: Values) -> bool:
    """
    Return whether or not to trim footnote space.

    If trim_footnote_reference_space is not None, return it.

    If trim_footnote_reference_space is None, return False unless the
    footnote reference style is 'superscript'.
    """

def get_source_line(node: nodes.Node) -> tuple[str, int]:
    """
    Return the "source" and "line" attributes from the `node` given or from
    its closest ancestor.
    """

def escape2null(text: str) -> str:
    """Return a string with escape-backslashes converted to nulls."""

def split_escaped_whitespace(text: str) -> list[str]:
    """
    Split `text` on escaped whitespace (null+space or null+newline).
    Return a list of strings.
    """

def strip_combining_chars(text: str) -> str: ...
def find_combining_chars(text: str) -> list[int]:
    """Return indices of all combining chars in  Unicode string `text`.

    >>> from docutils.utils import find_combining_chars
    >>> find_combining_chars('A t̆ab̆lĕ')
    [3, 6, 9]

    """

def column_indices(text: str) -> list[int]:
    """Indices of Unicode string `text` when skipping combining characters.

    >>> from docutils.utils import column_indices
    >>> column_indices('A t̆ab̆lĕ')
    [0, 1, 2, 4, 5, 7, 8]

    """

east_asian_widths: dict[str, int]

def column_width(text: str) -> int:
    """Return the column width of text.

    Correct ``len(text)`` for wide East Asian and combining Unicode chars.
    """

def uniq(L: list[_T]) -> list[_T]: ...
def normalize_language_tag(tag: str) -> list[str]:
    """Return a list of normalized combinations for a `BCP 47` language tag.

    Example:

    >>> from docutils.utils import normalize_language_tag
    >>> normalize_language_tag('de_AT-1901')
    ['de-at-1901', 'de-at', 'de-1901', 'de']
    >>> normalize_language_tag('de-CH-x_altquot')
    ['de-ch-x-altquot', 'de-ch', 'de-x-altquot', 'de']

    """

def xml_declaration(encoding: str | None = None) -> str:
    """Return an XML text declaration.

    Include an encoding declaration, if `encoding`
    is not 'unicode', '', or None.
    """

release_level_abbreviations: dict[str, str]

def version_identifier(version_info: tuple[int, int, int, str, int, bool] | None = None) -> str:
    """
    Return a version identifier string built from `version_info`, a
    `docutils.VersionInfo` namedtuple instance or compatible tuple. If
    `version_info` is not provided, by default return a version identifier
    string based on `docutils.__version_info__` (i.e. the current Docutils
    version).
    """
