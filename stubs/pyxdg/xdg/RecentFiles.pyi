"""
Implementation of the XDG Recent File Storage Specification
http://standards.freedesktop.org/recent-file-spec
"""

from _typeshed import Incomplete, StrOrBytesPath, StrPath
from collections.abc import Iterable

class RecentFiles:
    RecentFiles: list[RecentFile]
    filename: str
    def __init__(self) -> None: ...
    def parse(self, filename: StrPath | None = None) -> None:
        """Parse a list of recently used files.

        filename defaults to ``~/.recently-used``.
        """

    def write(self, filename: StrOrBytesPath | None = None) -> None:
        """Write the list of recently used files to disk.

        If the instance is already associated with a file, filename can be
        omitted to save it there again.
        """

    def getFiles(
        self, mimetypes: Iterable[str] | None = None, groups: Iterable[Incomplete] | None = None, limit: int = 0
    ) -> list[StrPath]:
        """Get a list of recently used files.

        The parameters can be used to filter by mime types, by group, or to
        limit the number of items returned. By default, the entire list is
        returned, except for items marked private.
        """

    def addFile(self, item: StrPath, mimetype: str, groups: Iterable[Incomplete] | None = None, private: bool = False) -> None:
        """Add a recently used file.

        item should be the URI of the file, typically starting with ``file:///``.
        """

    def deleteFile(self, item: RecentFile | StrPath) -> None:
        """Remove a recently used file, by URI, from the list."""

    def sort(self) -> None: ...

class RecentFile:
    URI: str
    MimeType: str
    Timestamp: str
    Private: bool
    Groups: list[Incomplete]
    def __init__(self) -> None: ...
    def __cmp__(self, other: RecentFile) -> int: ...
    def __lt__(self, other: RecentFile) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
