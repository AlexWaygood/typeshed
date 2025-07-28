"""Discover and load entry points from installed packages."""

from collections.abc import Iterator, Sequence
from configparser import ConfigParser
from re import Pattern
from typing import Any
from typing_extensions import Self

entry_point_pattern: Pattern[str]
file_in_zip_pattern: Pattern[str]

class BadEntryPoint(Exception):
    """Raised when an entry point can't be parsed."""

    epstr: str
    def __init__(self, epstr: str) -> None: ...
    @staticmethod
    def err_to_warnings() -> Iterator[None]: ...

class NoSuchEntryPoint(Exception):
    """Raised by :func:`get_single` when no matching entry point is found."""

    group: str
    name: str
    def __init__(self, group: str, name: str) -> None: ...

class CaseSensitiveConfigParser(ConfigParser): ...

class EntryPoint:
    name: str
    module_name: str
    object_name: str
    extras: Sequence[str] | None
    distro: Distribution | None
    def __init__(
        self, name: str, module_name: str, object_name: str, extras: Sequence[str] | None = ..., distro: Distribution | None = ...
    ) -> None: ...
    def load(self) -> Any:
        """Load the object to which this entry point refers."""

    @classmethod
    def from_string(cls, epstr: str, name: str, distro: Distribution | None = ...) -> Self:
        """Parse an entry point from the syntax in entry_points.txt

        :param str epstr: The entry point string (not including 'name =')
        :param str name: The name of this entry point
        :param Distribution distro: The distribution in which the entry point was found
        :rtype: EntryPoint
        :raises BadEntryPoint: if *epstr* can't be parsed as an entry point.
        """

class Distribution:
    name: str
    version: str
    def __init__(self, name: str, version: str) -> None: ...
    @classmethod
    def from_name_version(cls, name: str) -> Self:
        """Parse a distribution from a "name-version" string

        :param str name: The name-version string (entrypoints-0.3)
        Returns an :class:`Distribution` object
        """

def iter_files_distros(
    path: Sequence[str] | None = ..., repeated_distro: str = ...
) -> Iterator[tuple[ConfigParser, Distribution | None]]: ...
def get_single(group: str, name: str, path: Sequence[str] | None = ...) -> EntryPoint:
    """Find a single entry point.

    Returns an :class:`EntryPoint` object, or raises :exc:`NoSuchEntryPoint`
    if no match is found.
    """

def get_group_named(group: str, path: Sequence[str] | None = ...) -> dict[str, EntryPoint]:
    """Find a group of entry points with unique names.

    Returns a dictionary of names to :class:`EntryPoint` objects.
    """

def get_group_all(group: str, path: Sequence[str] | None = ...) -> list[EntryPoint]:
    """Find all entry points in a group.

    Returns a list of :class:`EntryPoint` objects.
    """
