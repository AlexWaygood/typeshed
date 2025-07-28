from _typeshed import StrPath, SupportsKeysAndGetItem
from collections.abc import Container, Iterable, Iterator, Mapping, MutableMapping, Sequence
from typing import Literal, TypeVar, overload
from typing_extensions import TypeAlias
from uuid import UUID

_T = TypeVar("_T")

_Token: TypeAlias = (
    tuple[Literal["EMPTY"], str, None]
    | tuple[Literal["COMMENT"], str, None]
    | tuple[Literal["SECTION"], str, tuple[str, ...]]
    | tuple[Literal["KV"], str, tuple[str, str, str]]
)

def get_app_dir(app_name: str, roaming: bool = ..., force_posix: bool = ...) -> str:
    """Returns the config folder for the application.  The default behavior
    is to return whatever is most appropriate for the operating system.

    To give you an idea, for an app called ``"Foo Bar"``, something like
    the following folders could be returned:

    Mac OS X:
      ``~/Library/Application Support/Foo Bar``
    Mac OS X (POSIX):
      ``~/.foo-bar``
    Unix:
      ``~/.config/foo-bar``
    Unix (POSIX):
      ``~/.foo-bar``
    Win XP (roaming):
      ``C:\\Documents and Settings\\<user>\\Local Settings\\Application Data\\Foo Bar``
    Win XP (not roaming):
      ``C:\\Documents and Settings\\<user>\\Application Data\\Foo Bar``
    Win 7 (roaming):
      ``C:\\Users\\<user>\\AppData\\Roaming\\Foo Bar``
    Win 7 (not roaming):
      ``C:\\Users\\<user>\\AppData\\Local\\Foo Bar``

    :param app_name: the application name.  This should be properly capitalized
                     and can contain whitespace.
    :param roaming: controls if the folder should be roaming or not on Windows.
                    Has no affect otherwise.
    :param force_posix: if this is set to `True` then on any POSIX system the
                        folder will be stored in the home folder with a leading
                        dot instead of the XDG config home or darwin's
                        application support folder.
    """

class Dialect:
    """This class allows customizing the dialect of the ini file.  The
    default configuration is a compromise between the general Windows
    format and what's common on Unix systems.

    Example dialect config::

        unix_dialect = Dialect(
            kv_sep=': ',
            quotes=("'",),
            comments=('#',),
        )

    :param ns_sep: the namespace separator.  This character is used to
                   create hierarchical structures in sections and also
                   placed between section and field.
    :param kv_sep: the separator to be placed between key and value.  For
                   parsing whitespace is automatically removed.
    :param quotes: a list of quote characters supported for strings.  The
                   leftmost one is automatically used for serialization,
                   the others are supported for deserialization.
    :param true: strings that should be considered boolean true.
    :param false: strings that should be considered boolean false.
    :param comments: comment start markers.
    :param allow_escaping: enables or disables backslash escapes.
    :param linesep: a specific line separator to use other than the
                    operating system's default.
    """

    def __init__(
        self,
        ns_sep: str = ...,
        kv_sep: str = ...,
        quotes: Sequence[str] = ...,
        true: Sequence[str] = ...,
        false: Sequence[str] = ...,
        comments: Container[str] = ...,
        allow_escaping: bool = ...,
        linesep: str | None = ...,
    ) -> None: ...
    @property
    def ns_sep(self) -> str: ...
    @property
    def kv_sep(self) -> str: ...
    @property
    def quotes(self) -> Sequence[str]: ...
    @property
    def true(self) -> Sequence[str]: ...
    @property
    def false(self) -> Sequence[str]: ...
    @property
    def comments(self) -> Container[str]: ...
    @property
    def allow_escaping(self) -> bool: ...
    @property
    def linesep(self) -> str | None: ...
    def get_actual_linesep(self) -> str: ...
    def get_strippable_lineseps(self) -> str: ...
    def kv_serialize(self, key: str, val: str | None) -> str | None: ...
    def escape(self, value: str, quote: str | None = ...) -> str: ...
    def unescape(self, value: str) -> str: ...
    def to_string(self, value: bool | float | str) -> str: ...
    def dict_from_iterable(self, iterable: Iterable[str]) -> MutableMapping[str, str]:
        """Builds a mapping of values out of an iterable of lines."""

    def tokenize(self, iterable: Iterable[str]) -> Iterator[_Token]:
        """Tokenizes an iterable of lines."""

    def update_tokens(
        self, old_tokens: Iterable[_Token], changes: SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]]
    ) -> list[_Token]:
        """Given the tokens returned from :meth:`tokenize` and a dictionary
        of new values (or `None` for values to be deleted) returns a new
        list of tokens that should be written back to a file.
        """

default_dialect: Dialect

class IniData(MutableMapping[str, str]):
    """This object behaves similar to a dictionary but it tracks
    modifications properly so that it can later write them back to an INI
    file with the help of the ini dialect, without destroying ordering or
    comments.

    This is rarely used directly, instead the :class:`IniFile` is normally
    used.

    This generally works similar to a dictionary and exposes the same
    basic API.
    """

    def __init__(self, mapping: Mapping[str, str] | None = ..., dialect: Dialect | None = ...) -> None: ...
    @property
    def dialect(self) -> Dialect: ...
    @property
    def is_dirty(self) -> bool:
        """This is true if the data was modified."""

    def get_updated_lines(self, line_iter: Iterable[_Token] | None = ...) -> list[_Token]:
        """Reconciles the updates in the ini data with the iterator of
        lines from the source file and returns a list of the new lines
        as they should be written into the file.
        """

    def discard(self) -> None:
        """Discards all local modifications in the ini data."""

    def rollover(self) -> None:
        """Rolls all local modifications to the primary data.  After this
        modifications are no longer tracked and `get_updated_lines` will
        not return them.
        """

    def to_dict(self) -> dict[str, str]:
        """Returns the current ini data as dictionary."""

    def __len__(self) -> int: ...
    @overload
    def get(self, name: str, default: None = None) -> str | None:
        """Return a value for a key or return a default if the key does
        not exist.
        """

    @overload
    def get(self, name: str, default: str) -> str: ...
    @overload
    def get(self, name: str, default: _T) -> str | _T: ...
    @overload
    def get_ascii(self, name: str) -> str | None:
        """This returns a value for a key for as long as the value fits
        into ASCII.  Otherwise (or if the key does not exist) the default
        is returned.  This is especially useful on Python 2 when working
        with some APIs that do not support unicode.
        """

    @overload
    def get_ascii(self, name: str, default: _T) -> str | _T: ...
    @overload
    def get_bool(self, name: str) -> bool:
        """Returns a value as boolean.  What constitutes as a valid boolean
        value depends on the dialect.
        """

    @overload
    def get_bool(self, name: str, default: _T) -> bool | _T: ...
    @overload
    def get_int(self, name: str) -> int | None:
        """Returns a value as integer."""

    @overload
    def get_int(self, name: str, default: _T = ...) -> int | _T: ...
    @overload
    def get_float(self, name: str) -> float | None:
        """Returns a value as float."""

    @overload
    def get_float(self, name: str, default: _T) -> float | _T: ...
    @overload
    def get_uuid(self, name: str) -> UUID | None:
        """Returns a value as uuid."""

    @overload
    def get_uuid(self, name: str, default: _T) -> UUID | _T: ...
    def itersections(self) -> Iterator[str]:
        """Iterates over the sections of the sections of the ini."""

    def sections(self) -> Iterator[str]:
        """Iterates over the sections of the sections of the ini."""

    def iteritems(self) -> Iterator[tuple[str, str]]: ...
    def iterkeys(self) -> Iterator[str]: ...
    def itervalues(self) -> Iterator[str]: ...
    # NB: keys, items, values currently return a generator, which is
    # incompatible with the views returned by Mappings
    def items(self) -> Iterator[tuple[str, str]]: ...  # type: ignore[override]
    def keys(self) -> Iterator[str]: ...  # type: ignore[override]
    def __iter__(self) -> Iterator[str]: ...
    def values(self) -> Iterator[str]: ...  # type: ignore[override]
    def section_as_dict(self, section: str) -> dict[str, str]: ...
    def __getitem__(self, name: str) -> str: ...
    def __setitem__(self, name: str, value: str) -> None: ...
    def __delitem__(self, name: str) -> None: ...

class IniFile(IniData):
    """This class implements simplified read and write access to INI files
    in a way that preserves the original files as good as possible.  Unlike
    a regular INI serializer it only overwrites the lines that were modified.

    Example usage::

        ifile = IniFile('myfile.ini')
        ifile['ui.username'] = 'john_doe'
        ifile.save()

    The ini file exposes unicode strings but utility methods are provided
    for common type conversion.  The default namespace separator is a dot
    (``.``).

    The format of the file can be configured by providing a custom
    :class:`Dialect` instance to the constructor.
    """

    def __init__(self, filename: StrPath, encoding: str | None = ..., dialect: Dialect | None = ...) -> None: ...
    @property
    def filename(self) -> str: ...
    @property
    def encoding(self) -> str | None: ...
    @property
    def is_new(self) -> bool: ...
    def save(self, create_folder: bool = ...) -> None:
        """Saves all modifications back to the file.  By default the folder
        in which the file is placed needs to exist.
        """

class AppIniFile(IniFile):
    """This works exactly the same as :class:`IniFile` but the ini files
    are placed by default in an application config directory.  This uses
    the function :func:`get_app_dir` internally to calculate the path
    to it.  Also by default the :meth:`~IniFile.save` method will create
    the folder if it did not exist yet.

    Example::

        from inifile import AppIniFile

        config = AppIniFile('My App', 'my_config.ini')
        config['ui.user_colors'] = True
        config['ui.colorscheme'] = 'tango'
        config.save()
    """

    def __init__(
        self,
        app_name: str,
        filename: StrPath,
        roaming: bool = ...,
        force_posix: bool = ...,
        encoding: str | None = ...,
        dialect: Dialect | None = ...,
    ) -> None: ...
