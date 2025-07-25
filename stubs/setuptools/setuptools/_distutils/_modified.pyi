"""Timestamp comparison of files and groups of files."""

from _typeshed import StrOrBytesPath
from collections.abc import Callable, Iterable
from typing import Literal, TypeVar

_SourcesT = TypeVar("_SourcesT", bound=StrOrBytesPath)
_TargetsT = TypeVar("_TargetsT", bound=StrOrBytesPath)

def newer(source: StrOrBytesPath, target: StrOrBytesPath) -> bool:
    """
    Is source modified more recently than target.

    Returns True if 'source' is modified more recently than
    'target' or if 'target' does not exist.

    Raises DistutilsFileError if 'source' does not exist.
    """

def newer_pairwise(
    sources: Iterable[_SourcesT], targets: Iterable[_TargetsT], newer: Callable[[_SourcesT, _TargetsT], bool] = ...
) -> tuple[list[_SourcesT], list[_TargetsT]]:
    """
    Filter filenames where sources are newer than targets.

    Walk two filename iterables in parallel, testing if each source is newer
    than its corresponding target.  Returns a pair of lists (sources,
    targets) where source is newer than target, according to the semantics
    of 'newer()'.
    """

def newer_group(
    sources: Iterable[StrOrBytesPath], target: StrOrBytesPath, missing: Literal["error", "ignore", "newer"] = "error"
) -> bool:
    """
    Is target out-of-date with respect to any file in sources.

    Return True if 'target' is out-of-date with respect to any file
    listed in 'sources'. In other words, if 'target' exists and is newer
    than every file in 'sources', return False; otherwise return True.
    ``missing`` controls how to handle a missing source file:

    - error (default): allow the ``stat()`` call to fail.
    - ignore: silently disregard any missing source files.
    - newer: treat missing source files as "target out of date". This
      mode is handy in "dry-run" mode: it will pretend to carry out
      commands that wouldn't work because inputs are missing, but
      that doesn't matter because dry-run won't run the commands.
    """

def newer_pairwise_group(
    sources: Iterable[_SourcesT], targets: Iterable[_TargetsT], *, newer: Callable[[_SourcesT, _TargetsT], bool] = ...
) -> tuple[list[_SourcesT], list[_TargetsT]]:
    """Create a new function with partial application of the given arguments
    and keywords.
    """
