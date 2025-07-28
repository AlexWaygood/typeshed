"""
**polib** allows you to manipulate, create, modify gettext files (pot, po and
mo files).  You can load existing files, iterate through it's entries, add,
modify entries, comments or metadata, etc. or create new po files from scratch.

**polib** provides a simple and pythonic API via the :func:`~polib.pofile` and
:func:`~polib.mofile` convenience functions.
"""

from collections.abc import Callable
from pathlib import Path
from typing import IO, Any, Generic, Literal, SupportsIndex, TypeVar, overload

_TB = TypeVar("_TB", bound=_BaseEntry)
_TP = TypeVar("_TP", bound=POFile)
_TM = TypeVar("_TM", bound=MOFile)

default_encoding: str

# wrapwidth: int
# encoding: str
# check_for_duplicates: bool
@overload
def pofile(pofile: str | Path, *, klass: type[_TP], **kwargs: Any) -> _TP:
    """
    Convenience function that parses the po or pot file ``pofile`` and returns
    a :class:`~polib.POFile` instance.

    Arguments:

    ``pofile``
        string, full or relative path to the po/pot file or its content (data).

    ``wrapwidth``
        integer, the wrap width, only useful when the ``-w`` option was passed
        to xgettext (optional, default: ``78``).

    ``encoding``
        string, the encoding to use (e.g. "utf-8") (default: ``None``, the
        encoding will be auto-detected).

    ``check_for_duplicates``
        whether to check for duplicate entries when adding entries to the
        file (optional, default: ``False``).

    ``klass``
        class which is used to instantiate the return value (optional,
        default: ``None``, the return value with be a :class:`~polib.POFile`
        instance).
    """

@overload
def pofile(pofile: str | Path, **kwargs: Any) -> POFile: ...
@overload
def mofile(mofile: str, *, klass: type[_TM], **kwargs: Any) -> _TM:
    """
    Convenience function that parses the mo file ``mofile`` and returns a
    :class:`~polib.MOFile` instance.

    Arguments:

    ``mofile``
        string, full or relative path to the mo file or its content (string
        or bytes).

    ``wrapwidth``
        integer, the wrap width, only useful when the ``-w`` option was passed
        to xgettext to generate the po file that was used to format the mo file
        (optional, default: ``78``).

    ``encoding``
        string, the encoding to use (e.g. "utf-8") (default: ``None``, the
        encoding will be auto-detected).

    ``check_for_duplicates``
        whether to check for duplicate entries when adding entries to the
        file (optional, default: ``False``).

    ``klass``
        class which is used to instantiate the return value (optional,
        default: ``None``, the return value with be a :class:`~polib.POFile`
        instance).
    """

@overload
def mofile(mofile: str, **kwargs: Any) -> MOFile: ...
def detect_encoding(file: bytes | str, binary_mode: bool = ...) -> str:
    """
    Try to detect the encoding used by the ``file``. The ``file`` argument can
    be a PO or MO file path or a string containing the contents of the file.
    If the encoding cannot be detected, the function will return the value of
    ``default_encoding``.

    Arguments:

    ``file``
        string, full or relative path to the po/mo file or its content.

    ``binary_mode``
        boolean, set this to True if ``file`` is a mo file.
    """

def escape(st: str) -> str:
    """
    Escapes the characters ``\\\\``, ``\\t``, ``\\n``, ``\\r``, ``\\v``,
    ``\\b``, ``\\f`` and ``"`` in the given string ``st`` and returns it.
    """

def unescape(st: str) -> str:
    """
    Unescapes the characters ``\\\\``, ``\\t``, ``\\n``, ``\\r``, ``\\v``,
    ``\\b``, ``\\f`` and ``"`` in the given string ``st`` and returns it.
    """

class _BaseFile(list[_TB]):
    """
    Common base class for the :class:`~polib.POFile` and :class:`~polib.MOFile`
    classes. This class should **not** be instantiated directly.
    """

    fpath: str
    wrapwidth: int
    encoding: str
    check_for_duplicates: bool
    header: str
    metadata: dict[str, str]
    metadata_is_fuzzy: bool
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor, accepts the following keyword arguments:

        ``pofile``
            string, the path to the po or mo file, or its content as a string.

        ``wrapwidth``
            integer, the wrap width, only useful when the ``-w`` option was
            passed to xgettext (optional, default: ``78``).

        ``encoding``
            string, the encoding to use, defaults to ``default_encoding``
            global variable (optional).

        ``check_for_duplicates``
            whether to check for duplicate entries when adding entries to the
            file, (optional, default: ``False``).
        """

    def __unicode__(self) -> str:
        """
        Returns the unicode representation of the file.
        """

    def __contains__(self, entry: _TB) -> bool:  # type: ignore[override]  # AttributeError otherwise
        """
        Overridden ``list`` method to implement the membership test (in and
        not in).
        The method considers that an entry is in the file if it finds an entry
        that has the same msgid (the test is **case sensitive**) and the same
        msgctxt (or none for both entries).

        Argument:

        ``entry``
            an instance of :class:`~polib._BaseEntry`.
        """

    def __eq__(self, other: object) -> bool: ...
    def append(self, entry: _TB) -> None:
        """
        Overridden method to check for duplicates entries, if a user tries to
        add an entry that is already in the file, the method will raise a
        ``ValueError`` exception.

        Argument:

        ``entry``
            an instance of :class:`~polib._BaseEntry`.
        """

    def insert(self, index: SupportsIndex, entry: _TB) -> None:
        """
        Overridden method to check for duplicates entries, if a user tries to
        add an entry that is already in the file, the method will raise a
        ``ValueError`` exception.

        Arguments:

        ``index``
            index at which the entry should be inserted.

        ``entry``
            an instance of :class:`~polib._BaseEntry`.
        """

    def metadata_as_entry(self) -> POEntry:
        """
        Returns the file metadata as a :class:`~polib.POFile` instance.
        """

    def save(self, fpath: str | None = ..., repr_method: str = ..., newline: str | None = ...) -> None:
        """
        Saves the po file to ``fpath``.
        If it is an existing file and no ``fpath`` is provided, then the
        existing file is rewritten with the modified data.

        Keyword arguments:

        ``fpath``
            string, full or relative path to the file.

        ``repr_method``
            string, the method to use for output.

        ``newline``
            string, controls how universal newlines works
        """

    def find(
        self, st: str, by: str = ..., include_obsolete_entries: bool = ..., msgctxt: str | Literal[False] = ...
    ) -> _TB | None:
        """
        Find the entry which msgid (or property identified by the ``by``
        argument) matches the string ``st``.

        Keyword arguments:

        ``st``
            string, the string to search for.

        ``by``
            string, the property to use for comparison (default: ``msgid``).

        ``include_obsolete_entries``
            boolean, whether to also search in entries that are obsolete.

        ``msgctxt``
            string, allows specifying a specific message context for the
            search.
        """

    def ordered_metadata(self) -> list[tuple[str, str]]:
        """
        Convenience method that returns an ordered version of the metadata
        dictionary. The return value is list of tuples (metadata name,
        metadata_value).
        """

    def to_binary(self) -> bytes:
        """
        Return the binary representation of the file.
        """

class POFile(_BaseFile[POEntry]):
    """
    Po (or Pot) file reader/writer.
    This class inherits the :class:`~polib._BaseFile` class and, by extension,
    the python ``list`` type.
    """

    def __unicode__(self) -> str:
        """
        Returns the unicode representation of the po file.
        """

    def save_as_mofile(self, fpath: str) -> None:
        """
        Saves the binary representation of the file to given ``fpath``.

        Keyword argument:

        ``fpath``
            string, full or relative path to the mo file.
        """

    def percent_translated(self) -> int:
        """
        Convenience method that returns the percentage of translated
        messages.
        """

    def translated_entries(self) -> list[POEntry]:
        """
        Convenience method that returns the list of translated entries.
        """

    def untranslated_entries(self) -> list[POEntry]:
        """
        Convenience method that returns the list of untranslated entries.
        """

    def fuzzy_entries(self) -> list[POEntry]:
        """
        Convenience method that returns the list of fuzzy entries.
        """

    def obsolete_entries(self) -> list[POEntry]:
        """
        Convenience method that returns the list of obsolete entries.
        """

    def merge(self, refpot: POFile) -> None:
        """
        Convenience method that merges the current pofile with the pot file
        provided. It behaves exactly as the gettext msgmerge utility:

        * comments of this file will be preserved, but extracted comments and
          occurrences will be discarded;
        * any translations or comments in the file will be discarded, however,
          dot comments and file positions will be preserved;
        * the fuzzy flags are preserved.

        Keyword argument:

        ``refpot``
            object POFile, the reference catalog.
        """

class MOFile(_BaseFile[MOEntry]):
    """
    Mo file reader/writer.
    This class inherits the :class:`~polib._BaseFile` class and, by
    extension, the python ``list`` type.
    """

    MAGIC: int
    MAGIC_SWAPPED: int
    magic_number: int | None
    version: int
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor, accepts all keywords arguments accepted by
        :class:`~polib._BaseFile` class.
        """

    def save_as_pofile(self, fpath: str) -> None:
        """
        Saves the mofile as a pofile to ``fpath``.

        Keyword argument:

        ``fpath``
            string, full or relative path to the file.
        """

    def save(self, fpath: str | None = ...) -> None:  # type: ignore[override]  # binary file does not allow argument repr_method
        """
        Saves the mofile to ``fpath``.

        Keyword argument:

        ``fpath``
            string, full or relative path to the file.
        """

    def percent_translated(self) -> int:
        """
        Convenience method to keep the same interface with POFile instances.
        """

    def translated_entries(self) -> list[MOEntry]:
        """
        Convenience method to keep the same interface with POFile instances.
        """

    def untranslated_entries(self) -> list[MOEntry]:
        """
        Convenience method to keep the same interface with POFile instances.
        """

    def fuzzy_entries(self) -> list[MOEntry]:
        """
        Convenience method to keep the same interface with POFile instances.
        """

    def obsolete_entries(self) -> list[MOEntry]:
        """
        Convenience method to keep the same interface with POFile instances.
        """

class _BaseEntry:
    """
    Base class for :class:`~polib.POEntry` and :class:`~polib.MOEntry` classes.
    This class should **not** be instantiated directly.
    """

    msgid: str
    msgstr: str
    msgid_plural: str
    msgstr_plural: dict[int, str]
    msgctxt: str
    obsolete: bool
    encoding: str
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor, accepts the following keyword arguments:

        ``msgid``
            string, the entry msgid.

        ``msgstr``
            string, the entry msgstr.

        ``msgid_plural``
            string, the entry msgid_plural.

        ``msgstr_plural``
            dict, the entry msgstr_plural lines.

        ``msgctxt``
            string, the entry context (msgctxt).

        ``obsolete``
            bool, whether the entry is "obsolete" or not.

        ``encoding``
            string, the encoding to use, defaults to ``default_encoding``
            global variable (optional).
        """

    def __unicode__(self, wrapwidth: int = ...) -> str:
        """
        Returns the unicode representation of the entry.
        """

    def __eq__(self, other: object) -> bool: ...
    @property
    def msgid_with_context(self) -> str: ...

class POEntry(_BaseEntry):
    """
    Represents a po file entry.
    """

    comment: str
    tcomment: str
    occurrences: list[tuple[str, str]]
    flags: list[str]
    previous_msgctxt: str | None
    previous_msgid: str | None
    previous_msgid_plural: str | None
    linenum: int | None
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor, accepts the following keyword arguments:

        ``comment``
            string, the entry comment.

        ``tcomment``
            string, the entry translator comment.

        ``occurrences``
            list, the entry occurrences.

        ``flags``
            list, the entry flags.

        ``previous_msgctxt``
            string, the entry previous context.

        ``previous_msgid``
            string, the entry previous msgid.

        ``previous_msgid_plural``
            string, the entry previous msgid_plural.

        ``linenum``
            integer, the line number of the entry
        """

    def __unicode__(self, wrapwidth: int = ...) -> str:
        """
        Returns the unicode representation of the entry.
        """

    def __cmp__(self, other: POEntry) -> int:
        """
        Called by comparison operations if rich comparison is not defined.
        """

    def __gt__(self, other: POEntry) -> bool: ...
    def __lt__(self, other: POEntry) -> bool: ...
    def __ge__(self, other: POEntry) -> bool: ...
    def __le__(self, other: POEntry) -> bool: ...
    def __eq__(self, other: POEntry) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: POEntry) -> bool: ...  # type: ignore[override]
    def translated(self) -> bool:
        """
        Returns ``True`` if the entry has been translated or ``False``
        otherwise.
        """

    def merge(self, other: POEntry) -> None:
        """
        Merge the current entry with the given pot entry.
        """

    @property
    def fuzzy(self) -> bool: ...
    @property
    def msgid_with_context(self) -> str: ...
    def __hash__(self) -> int: ...

class MOEntry(_BaseEntry):
    """
    Represents a mo file entry.
    """

    comment: str
    tcomment: str
    occurrences: list[tuple[str, str]]
    flags: list[str]
    previous_msgctxt: str | None
    previous_msgid: str | None
    previous_msgid_plural: str | None
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructor, accepts the following keyword arguments,
        for consistency with :class:`~polib.POEntry`:

        ``comment``
        ``tcomment``
        ``occurrences``
        ``flags``
        ``previous_msgctxt``
        ``previous_msgid``
        ``previous_msgid_plural``

        Note: even though these keyword arguments are accepted,
        they hold no real meaning in the context of MO files
        and are simply ignored.
        """

    def __hash__(self) -> int: ...

class _POFileParser(Generic[_TP]):
    """
    A finite state machine to efficiently and correctly parse po
    file format.
    """

    fhandle: IO[str]
    instance: _TP
    transitions: dict[tuple[str, str], tuple[Callable[[], bool], str]]
    current_line: int
    current_entry: POEntry
    current_state: str
    current_token: str | None
    msgstr_index: int
    entry_obsolete: int
    def __init__(self, pofile: str, *args: Any, **kwargs: Any) -> None:
        """
        Constructor.

        Keyword arguments:

        ``pofile``
            string, path to the po file or its content

        ``encoding``
            string, the encoding to use, defaults to ``default_encoding``
            global variable (optional).

        ``check_for_duplicates``
            whether to check for duplicate entries when adding entries to the
            file (optional, default: ``False``).
        """

    def parse(self) -> _TP:
        """
        Run the state machine, parse the file line by line and call process()
        with the current matched symbol.
        """

    def add(self, symbol: str, states: list[str], next_state: str) -> None:
        """
        Add a transition to the state machine.

        Keywords arguments:

        ``symbol``
            string, the matched token (two chars symbol).

        ``states``
            list, a list of states (two chars symbols).

        ``next_state``
            the next state the fsm will have after the action.
        """

    def process(self, symbol: str) -> None:
        """
        Process the transition corresponding to the current state and the
        symbol provided.

        Keywords arguments:

        ``symbol``
            string, the matched token (two chars symbol).

        ``linenum``
            integer, the current line number of the parsed file.
        """

    def handle_he(self) -> bool:
        """Handle a header comment."""

    def handle_tc(self) -> bool:
        """Handle a translator comment."""

    def handle_gc(self) -> bool:
        """Handle a generated comment."""

    def handle_oc(self) -> bool:
        """Handle a file:num occurrence."""

    def handle_fl(self) -> bool:
        """Handle a flags line."""

    def handle_pp(self) -> bool:
        """Handle a previous msgid_plural line."""

    def handle_pm(self) -> bool:
        """Handle a previous msgid line."""

    def handle_pc(self) -> bool:
        """Handle a previous msgctxt line."""

    def handle_ct(self) -> bool:
        """Handle a msgctxt."""

    def handle_mi(self) -> bool:
        """Handle a msgid."""

    def handle_mp(self) -> bool:
        """Handle a msgid plural."""

    def handle_ms(self) -> bool:
        """Handle a msgstr."""

    def handle_mx(self) -> bool:
        """Handle a msgstr plural."""

    def handle_mc(self) -> bool:
        """Handle a msgid or msgstr continuation line."""

class _MOFileParser(Generic[_TM]):
    """
    A class to parse binary mo files.
    """

    fhandle: IO[bytes]
    instance: _TM
    def __init__(self, mofile: str, *args: Any, **kwargs: Any) -> None:
        """
        Constructor.

        Keyword arguments:

        ``mofile``
            string, path to the mo file or its content

        ``encoding``
            string, the encoding to use, defaults to ``default_encoding``
            global variable (optional).

        ``check_for_duplicates``
            whether to check for duplicate entries when adding entries to the
            file (optional, default: ``False``).
        """

    def __del__(self) -> None:
        """
        Make sure the file is closed, this prevents warnings on unclosed file
        when running tests with python >= 3.2.
        """

    def parse(self) -> _TM:
        """
        Build the instance with the file handle provided in the
        constructor.
        """

__all__ = [
    "pofile",
    "POFile",
    "POEntry",
    "mofile",
    "MOFile",
    "MOEntry",
    "default_encoding",
    "escape",
    "unescape",
    "detect_encoding",
]
