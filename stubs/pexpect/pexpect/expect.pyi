import re
from collections.abc import Iterable
from typing import AnyStr, Generic

from .spawnbase import SpawnBase, _CompiledRePattern, _CompiledStringPattern, _Searcher

class searcher_string(Generic[AnyStr]):
    """This is a plain string search helper for the spawn.expect_any() method.
    This helper class is for speed. For more powerful regex patterns
    see the helper class, searcher_re.

    Attributes:

        eof_index     - index of EOF, or -1
        timeout_index - index of TIMEOUT, or -1

    After a successful match by the search() method the following attributes
    are available:

        start - index into the buffer, first byte of match
        end   - index into the buffer, first byte after match
        match - the matching string itself

    """

    eof_index: int
    timeout_index: int
    longest_string: int
    def __init__(self, strings: Iterable[_CompiledStringPattern[AnyStr]]) -> None:
        """This creates an instance of searcher_string. This argument 'strings'
        may be a list; a sequence of strings; or the EOF or TIMEOUT types.
        """
    match: AnyStr
    start: int
    end: int
    def search(self, buffer: AnyStr, freshlen: int, searchwindowsize: int | None = None):
        """This searches 'buffer' for the first occurrence of one of the search
        strings.  'freshlen' must indicate the number of bytes at the end of
        'buffer' which have not been searched before. It helps to avoid
        searching the same, possibly big, buffer over and over again.

        See class spawn for the 'searchwindowsize' argument.

        If there is a match this returns the index of that string, and sets
        'start', 'end' and 'match'. Otherwise, this returns -1.
        """

class searcher_re(Generic[AnyStr]):
    """This is regular expression string search helper for the
    spawn.expect_any() method. This helper class is for powerful
    pattern matching. For speed, see the helper class, searcher_string.

    Attributes:

        eof_index     - index of EOF, or -1
        timeout_index - index of TIMEOUT, or -1

    After a successful match by the search() method the following attributes
    are available:

        start - index into the buffer, first byte of match
        end   - index into the buffer, first byte after match
        match - the re.match object returned by a successful re.search

    """

    eof_index: int
    timeout_index: int
    def __init__(self, patterns: Iterable[_CompiledRePattern[AnyStr]]) -> None:
        """This creates an instance that searches for 'patterns' Where
        'patterns' may be a list or other sequence of compiled regular
        expressions, or the EOF or TIMEOUT types.
        """
    match: re.Match[AnyStr]
    start: int
    end: int
    def search(self, buffer: AnyStr, freshlen: int, searchwindowsize: int | None = None):
        """This searches 'buffer' for the first occurrence of one of the regular
        expressions. 'freshlen' must indicate the number of bytes at the end of
        'buffer' which have not been searched before.

        See class spawn for the 'searchwindowsize' argument.

        If there is a match this returns the index of that string, and sets
        'start', 'end' and 'match'. Otherwise, returns -1.
        """

class Expecter(Generic[AnyStr]):
    spawn: SpawnBase[AnyStr]
    searcher: _Searcher[AnyStr]
    searchwindowsize: int | None
    lookback: _Searcher[AnyStr] | int | None
    def __init__(self, spawn: SpawnBase[AnyStr], searcher: _Searcher[AnyStr], searchwindowsize: int | None = -1) -> None: ...
    def do_search(self, window: AnyStr, freshlen: int) -> int: ...
    def existing_data(self) -> int: ...
    def new_data(self, data: AnyStr) -> int: ...
    def eof(self, err: object = None) -> int: ...
    def timeout(self, err: object = None) -> int: ...
    def errored(self) -> None: ...
    def expect_loop(self, timeout: float | None = -1) -> int:
        """Blocking expect"""
