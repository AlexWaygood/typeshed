"""distutils.filelist

Provides the FileList class, used for poking about the filesystem
and building lists of files.
"""

from _typeshed import StrPath, Unused
from collections.abc import Iterable
from re import Pattern
from typing import Literal, overload

# class is entirely undocumented
class FileList:
    """A list of files built by on exploring the filesystem and filtered by
    applying various patterns to what we find there.

    Instance attributes:
      dir
        directory from which files will be taken -- only used if
        'allfiles' not supplied to constructor
      files
        list of filenames currently being built/filtered/manipulated
      allfiles
        complete list of files under consideration (ie. without any
        filtering applied)
    """

    allfiles: Iterable[str] | None
    files: list[str]
    def __init__(self, warn: Unused = None, debug_print: Unused = None) -> None: ...
    def set_allfiles(self, allfiles: Iterable[str]) -> None: ...
    def findall(self, dir: StrPath = ...) -> None: ...
    def debug_print(self, msg: object) -> None:
        """Print 'msg' to stdout if the global DEBUG (taken from the
        DISTUTILS_DEBUG environment variable) flag is true.
        """

    def append(self, item: str) -> None: ...
    def extend(self, items: Iterable[str]) -> None: ...
    def sort(self) -> None: ...
    def remove_duplicates(self) -> None: ...
    def process_template_line(self, line: str) -> None: ...
    @overload
    def include_pattern(
        self, pattern: str, anchor: bool = True, prefix: str | None = None, is_regex: Literal[False] = False
    ) -> bool:
        """Select strings (presumably filenames) from 'self.files' that
        match 'pattern', a Unix-style wildcard (glob) pattern.  Patterns
        are not quite the same as implemented by the 'fnmatch' module: '*'
        and '?'  match non-special characters, where "special" is platform-
        dependent: slash on Unix; colon, slash, and backslash on
        DOS/Windows; and colon on Mac OS.

        If 'anchor' is true (the default), then the pattern match is more
        stringent: "*.py" will match "foo.py" but not "foo/bar.py".  If
        'anchor' is false, both of these will match.

        If 'prefix' is supplied, then only filenames starting with 'prefix'
        (itself a pattern) and ending with 'pattern', with anything in between
        them, will match.  'anchor' is ignored in this case.

        If 'is_regex' is true, 'anchor' and 'prefix' are ignored, and
        'pattern' is assumed to be either a string containing a regex or a
        regex object -- no translation is done, the regex is just compiled
        and used as-is.

        Selected strings will be added to self.files.

        Return True if files are found, False otherwise.
        """

    @overload
    def include_pattern(
        self, pattern: str | Pattern[str], anchor: bool = True, prefix: str | None = None, *, is_regex: Literal[True]
    ) -> bool: ...
    @overload
    def include_pattern(self, pattern: str | Pattern[str], anchor: bool, prefix: str | None, is_regex: Literal[True]) -> bool: ...
    @overload
    def exclude_pattern(
        self, pattern: str, anchor: bool = True, prefix: str | None = None, is_regex: Literal[False] = False
    ) -> bool:
        """Remove strings (presumably filenames) from 'files' that match
        'pattern'.  Other parameters are the same as for
        'include_pattern()', above.
        The list 'self.files' is modified in place.
        Return True if files are found, False otherwise.
        """

    @overload
    def exclude_pattern(
        self, pattern: str | Pattern[str], anchor: bool = True, prefix: str | None = None, *, is_regex: Literal[True]
    ) -> bool: ...
    @overload
    def exclude_pattern(self, pattern: str | Pattern[str], anchor: bool, prefix: str | None, is_regex: Literal[True]) -> bool: ...
