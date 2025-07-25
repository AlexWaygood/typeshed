"""
This module is based on a rox module (LGPL):

http://cvs.sourceforge.net/viewcvs.py/rox/ROX-Lib2/python/rox/mime.py?rev=1.21&view=log

This module provides access to the shared MIME database.

types is a dictionary of all known MIME types, indexed by the type name, e.g.
types['application/x-python']

Applications can install information about MIME types by storing an
XML file as <MIME>/packages/<application>.xml and running the
update-mime-database command, which is provided by the freedesktop.org
shared mime database package.

See http://www.freedesktop.org/standards/shared-mime-info-spec/ for
information about the format of these files.

(based on version 0.13)
"""

import re
from _typeshed import StrOrBytesPath, SupportsLenAndGetItem, Unused
from collections import defaultdict
from collections.abc import Collection, Iterable
from io import BytesIO
from typing import Literal
from typing_extensions import Self, TypeAlias

FREE_NS: str
types: dict[str, MIMEtype]
exts: Unused | None  # This appears to be unused.
globs: GlobDB | None
literals: Unused | None  # This appears to be unused.
magic: MagicDB | None
PY3: Literal[True]

_MimeTypeWeightPair: TypeAlias = tuple[MIMEtype, int]

def lookup(media: str, subtype: str | None = None) -> MIMEtype:
    """Get the MIMEtype object for the given type.

    This remains for backwards compatibility; calling MIMEtype now does
    the same thing.

    The name can either be passed as one part ('text/plain'), or as two
    ('text', 'plain').
    """

class MIMEtype:
    """Class holding data about a MIME type.

    Calling the class will return a cached instance, so there is only one
    instance for each MIME type. The name can either be passed as one part
    ('text/plain'), or as two ('text', 'plain').
    """

    def __new__(cls, media: str, subtype: str | None = None) -> Self: ...
    def get_comment(self) -> str:
        """Returns comment for current language, loading it if needed."""

    def canonical(self) -> Self:
        """Returns the canonical MimeType object if this is an alias."""

    def inherits_from(self) -> set[MIMEtype]:
        """Returns a set of Mime types which this inherits from."""

    def __hash__(self) -> int: ...

class UnknownMagicRuleFormat(ValueError): ...

class DiscardMagicRules(Exception):
    """Raised when __NOMAGIC__ is found, and caught to discard previous rules."""

class MagicRule:
    also: MagicRule | MagicMatchAny | None
    start: int
    value: bytes
    mask: bytes | None
    word: int
    range: int
    def __init__(self, start: int, value: bytes, mask: bytes, word: int, range: int) -> None: ...
    rule_ending_re: re.Pattern[str]
    @classmethod
    def from_file(cls, f: BytesIO) -> tuple[int, MagicRule]:
        """Read a rule from the binary magics file. Returns a 2-tuple of
        the nesting depth and the MagicRule.
        """

    def maxlen(self) -> int: ...
    def match(self, buffer: SupportsLenAndGetItem[bytes]) -> bool: ...
    def match0(self, buffer: SupportsLenAndGetItem[bytes]) -> bool: ...

class MagicMatchAny:
    """Match any of a set of magic rules.

    This has a similar interface to MagicRule objects (i.e. its match() and
    maxlen() methods), to allow for duck typing.
    """

    rules: Collection[MagicRule]
    def __init__(self, rules: Iterable[MagicRule]) -> None: ...
    def match(self, buffer: SupportsLenAndGetItem[bytes]) -> bool: ...
    def maxlen(self) -> int: ...
    @classmethod
    def from_file(cls, f: BytesIO) -> MagicMatchAny | MagicRule | None:
        """Read a set of rules from the binary magic file."""

    @classmethod
    def from_rule_tree(cls, tree: list[MagicRule]) -> MagicMatchAny | MagicRule | None:
        """From a nested list of (rule, subrules) pairs, build a MagicMatchAny
        instance, recursing down the tree.

        Where there's only one top-level rule, this is returned directly,
        to simplify the nested structure. Returns None if no rules were read.
        """

class MagicDB:
    bytype: defaultdict[MIMEtype, list[tuple[int, MagicRule]]]
    def __init__(self) -> None: ...
    def merge_file(self, fname: StrOrBytesPath) -> None:
        """Read a magic binary file, and add its rules to this MagicDB."""
    alltypes: list[tuple[int, MIMEtype, MagicRule]]
    maxlen: int
    def finalise(self) -> None:
        """Prepare the MagicDB for matching.

        This should be called after all rules have been merged into it.
        """

    def match_data(
        self, data: bytes, max_pri: int = 100, min_pri: int = 0, possible: Iterable[MIMEtype] | None = None
    ) -> MIMEtype:
        """Do magic sniffing on some bytes.

        max_pri & min_pri can be used to specify the maximum & minimum priority
        rules to look for. possible can be a list of mimetypes to check, or None
        (the default) to check all mimetypes until one matches.

        Returns the MIMEtype found, or None if no entries match.
        """

    def match(
        self, path: StrOrBytesPath, max_pri: int = 100, min_pri: int = 0, possible: Iterable[MIMEtype] | None = None
    ) -> MIMEtype:
        """Read data from the file and do magic sniffing on it.

        max_pri & min_pri can be used to specify the maximum & minimum priority
        rules to look for. possible can be a list of mimetypes to check, or None
        (the default) to check all mimetypes until one matches.

        Returns the MIMEtype found, or None if no entries match. Raises IOError
        if the file can't be opened.
        """

class GlobDB:
    allglobs: defaultdict[MIMEtype, list[tuple[int, str, str]]]
    def __init__(self) -> None:
        """Prepare the GlobDB. It can't actually be used until .finalise() is
        called, but merge_file() can be used to add data before that.
        """

    def merge_file(self, path: StrOrBytesPath) -> None:
        """Loads name matching information from a globs2 file."""
    exts: defaultdict[str, list[MIMEtype | int]]  # Actually list[MIMEtype, int], but that's not valid.
    cased_exts: defaultdict[str, list[MIMEtype | int]]  # Actually list[MIMEtype, int], but that's not valid.
    globs: list[tuple[re.Pattern[str], MIMEtype, int]]
    literals: dict[str, _MimeTypeWeightPair]
    cased_literals: dict[str, _MimeTypeWeightPair]
    def finalise(self) -> None:
        """Prepare the GlobDB for matching.

        This should be called after all files have been merged into it.
        """

    def first_match(self, path: StrOrBytesPath) -> _MimeTypeWeightPair | None:
        """Return the first match found for a given path, or None if no match
        is found.
        """

    def all_matches(self, path: StrOrBytesPath) -> list[_MimeTypeWeightPair]:
        """Return a list of (MIMEtype, glob weight) pairs for the path."""

text: MIMEtype
octet_stream: MIMEtype
inode_block: MIMEtype
inode_char: MIMEtype
inode_dir: MIMEtype
inode_fifo: MIMEtype
inode_socket: MIMEtype
inode_symlink: MIMEtype
inode_door: MIMEtype
app_exe: MIMEtype

def update_cache() -> None: ...
def get_type_by_name(path: StrOrBytesPath) -> _MimeTypeWeightPair | None:
    """Returns type of file by its name, or None if not known"""

def get_type_by_contents(path: StrOrBytesPath, max_pri: int = 100, min_pri: int = 0) -> MIMEtype:
    """Returns type of file by its contents, or None if not known"""

def get_type_by_data(data: bytes, max_pri: int = 100, min_pri: int = 0) -> MIMEtype:
    """Returns type of the data, which should be bytes."""

def get_type(path: StrOrBytesPath, follow: bool = True, name_pri: int = 100) -> MIMEtype:
    """Returns type of file indicated by path.

    This function is *deprecated* - :func:`get_type2` is more accurate.

    :param path: pathname to check (need not exist)
    :param follow: when reading file, follow symbolic links
    :param name_pri: Priority to do name matches. 100=override magic

    This tries to use the contents of the file, and falls back to the name. It
    can also handle special filesystem objects like directories and sockets.
    """

def get_type2(path: StrOrBytesPath, follow: bool = True) -> MIMEtype:
    """Find the MIMEtype of a file using the XDG recommended checking order.

    This first checks the filename, then uses file contents if the name doesn't
    give an unambiguous MIMEtype. It can also handle special filesystem objects
    like directories and sockets.

    :param path: file path to examine (need not exist)
    :param follow: whether to follow symlinks

    :rtype: :class:`MIMEtype`

    .. versionadded:: 1.0
    """

def is_text_file(path: StrOrBytesPath) -> bool:
    """Guess whether a file contains text or binary data.

    Heuristic: binary if the first 32 bytes include ASCII control characters.
    This rule may change in future versions.

    .. versionadded:: 1.0
    """

def get_extensions(mimetype: MIMEtype) -> set[str]:
    """Retrieve the set of filename extensions matching a given MIMEtype.

    Extensions are returned without a leading dot, e.g. 'py'. If no extensions
    are registered for the MIMEtype, returns an empty set.

    The extensions are stored in a cache the first time this is called.

    .. versionadded:: 1.0
    """

def install_mime_info(application: str, package_file: StrOrBytesPath) -> None:
    """Copy 'package_file' as ``~/.local/share/mime/packages/<application>.xml.``
    If package_file is None, install ``<app_dir>/<application>.xml``.
    If already installed, does nothing. May overwrite an existing
    file with the same name (if the contents are different)
    """
