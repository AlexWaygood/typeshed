from asyncio import ReadTransport
from collections.abc import Awaitable, Callable, Iterable
from re import Match, Pattern
from typing import IO, AnyStr, Generic, Literal, Protocol, TextIO, overload
from typing_extensions import TypeAlias

from ._async import PatternWaiter
from .exceptions import EOF, TIMEOUT
from .expect import searcher_re, searcher_string

PY3: bool
text_type: type

class _NullCoder:
    """Pass bytes through unchanged."""

    @staticmethod
    def encode(b: str, final: bool = False): ...
    @staticmethod
    def decode(b: str, final: bool = False): ...

class _Logfile(Protocol):
    def write(self, s, /) -> object: ...
    def flush(self) -> object: ...

_ErrorPattern: TypeAlias = type[EOF | TIMEOUT]
_InputStringPattern: TypeAlias = str | bytes | _ErrorPattern
_InputRePattern: TypeAlias = Pattern[str] | Pattern[bytes] | _InputStringPattern
_CompiledStringPattern: TypeAlias = AnyStr | _ErrorPattern
_CompiledRePattern: TypeAlias = Pattern[AnyStr] | _ErrorPattern
_Searcher: TypeAlias = searcher_string[AnyStr] | searcher_re[AnyStr]

class SpawnBase(Generic[AnyStr]):
    """A base class providing the backwards-compatible spawn API for Pexpect.

    This should not be instantiated directly: use :class:`pexpect.spawn` or
    :class:`pexpect.fdpexpect.fdspawn`.
    """

    encoding: str | None
    pid: int | None
    flag_eof: bool
    stdin: TextIO
    stdout: TextIO
    stderr: TextIO
    searcher: None
    ignorecase: bool
    before: AnyStr | None
    after: _CompiledStringPattern[AnyStr] | None
    match: AnyStr | Match[AnyStr] | _ErrorPattern | None
    match_index: int | None
    terminated: bool
    exitstatus: int | None
    signalstatus: int | None
    status: int | None
    child_fd: int
    timeout: float | None
    delimiter: type[EOF]
    logfile: _Logfile | None
    logfile_read: _Logfile | None
    logfile_send: _Logfile | None
    maxread: int
    searchwindowsize: int | None
    delaybeforesend: float | None
    delayafterclose: float
    delayafterterminate: float
    delayafterread: float
    softspace: bool
    name: str
    closed: bool
    codec_errors: str
    string_type: type[AnyStr]
    buffer_type: IO[AnyStr]
    crlf: AnyStr
    allowed_string_types: tuple[type, ...]
    linesep: AnyStr
    write_to_stdout: Callable[[AnyStr], int]
    async_pw_transport: tuple[PatternWaiter[AnyStr], ReadTransport] | None
    def __init__(
        self,
        timeout: float | None = 30,
        maxread: int = 2000,
        searchwindowsize: int | None = None,
        logfile: _Logfile | None = None,
        encoding: str | None = None,
        codec_errors: str = "strict",
    ) -> None: ...
    @property
    def buffer(self) -> AnyStr: ...
    @buffer.setter
    def buffer(self, value: AnyStr) -> None: ...
    def read_nonblocking(self, size: int = 1, timeout: float | None = None) -> AnyStr:
        """This reads data from the file descriptor.

        This is a simple implementation suitable for a regular file. Subclasses using ptys or pipes should override it.

        The timeout parameter is ignored.
        """

    def compile_pattern_list(self, patterns: _InputRePattern | list[_InputRePattern]) -> list[_CompiledRePattern[AnyStr]]:
        """This compiles a pattern-string or a list of pattern-strings.
        Patterns must be a StringType, EOF, TIMEOUT, SRE_Pattern, or a list of
        those. Patterns may also be None which results in an empty list (you
        might do this if waiting for an EOF or TIMEOUT condition without
        expecting any pattern).

        This is used by expect() when calling expect_list(). Thus expect() is
        nothing more than::

             cpl = self.compile_pattern_list(pl)
             return self.expect_list(cpl, timeout)

        If you are using expect() within a loop it may be more
        efficient to compile the patterns first and then call expect_list().
        This avoid calls in a loop to compile_pattern_list()::

             cpl = self.compile_pattern_list(my_pattern)
             while some_condition:
                ...
                i = self.expect_list(cpl, timeout)
                ...
        """

    @overload
    def expect(
        self,
        pattern: _InputRePattern | list[_InputRePattern],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        async_: Literal[False] = False,
    ) -> int:
        """This seeks through the stream until a pattern is matched. The
        pattern is overloaded and may take several types. The pattern can be a
        StringType, EOF, a compiled re, or a list of any of those types.
        Strings will be compiled to re types. This returns the index into the
        pattern list. If the pattern was not a list this returns index 0 on a
        successful match. This may raise exceptions for EOF or TIMEOUT. To
        avoid the EOF or TIMEOUT exceptions add EOF or TIMEOUT to the pattern
        list. That will cause expect to match an EOF or TIMEOUT condition
        instead of raising an exception.

        If you pass a list of patterns and more than one matches, the first
        match in the stream is chosen. If more than one pattern matches at that
        point, the leftmost in the pattern list is chosen. For example::

            # the input is 'foobar'
            index = p.expect(['bar', 'foo', 'foobar'])
            # returns 1('foo') even though 'foobar' is a "better" match

        Please note, however, that buffering can affect this behavior, since
        input arrives in unpredictable chunks. For example::

            # the input is 'foobar'
            index = p.expect(['foobar', 'foo'])
            # returns 0('foobar') if all input is available at once,
            # but returns 1('foo') if parts of the final 'bar' arrive late

        When a match is found for the given pattern, the class instance
        attribute *match* becomes an re.MatchObject result.  Should an EOF
        or TIMEOUT pattern match, then the match attribute will be an instance
        of that exception class.  The pairing before and after class
        instance attributes are views of the data preceding and following
        the matching pattern.  On general exception, class attribute
        *before* is all data received up to the exception, while *match* and
        *after* attributes are value None.

        When the keyword argument timeout is -1 (default), then TIMEOUT will
        raise after the default value specified by the class timeout
        attribute. When None, TIMEOUT will not be raised and may block
        indefinitely until match.

        When the keyword argument searchwindowsize is -1 (default), then the
        value specified by the class maxread attribute is used.

        A list entry may be EOF or TIMEOUT instead of a string. This will
        catch these exceptions and return the index of the list entry instead
        of raising the exception. The attribute 'after' will be set to the
        exception type. The attribute 'match' will be None. This allows you to
        write code like this::

                index = p.expect(['good', 'bad', pexpect.EOF, pexpect.TIMEOUT])
                if index == 0:
                    do_something()
                elif index == 1:
                    do_something_else()
                elif index == 2:
                    do_some_other_thing()
                elif index == 3:
                    do_something_completely_different()

        instead of code like this::

                try:
                    index = p.expect(['good', 'bad'])
                    if index == 0:
                        do_something()
                    elif index == 1:
                        do_something_else()
                except EOF:
                    do_some_other_thing()
                except TIMEOUT:
                    do_something_completely_different()

        These two forms are equivalent. It all depends on what you want. You
        can also just expect the EOF if you are waiting for all output of a
        child to finish. For example::

                p = pexpect.spawn('/bin/ls')
                p.expect(pexpect.EOF)
                print p.before

        If you are trying to optimize for speed then see expect_list().

        On Python 3.4, or Python 3.3 with asyncio installed, passing
        ``async_=True``  will make this return an :mod:`asyncio` coroutine,
        which you can yield from to get the same result that this method would
        normally give directly. So, inside a coroutine, you can replace this code::

            index = p.expect(patterns)

        With this non-blocking form::

            index = yield from p.expect(patterns, async_=True)
        """

    @overload
    def expect(
        self,
        pattern: _InputRePattern | list[_InputRePattern],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        *,
        async_: Literal[True],
    ) -> Awaitable[int]: ...
    @overload
    def expect_list(
        self,
        pattern_list: list[_CompiledRePattern[AnyStr]],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        async_: Literal[False] = False,
    ) -> int:
        """This takes a list of compiled regular expressions and returns the
        index into the pattern_list that matched the child output. The list may
        also contain EOF or TIMEOUT(which are not compiled regular
        expressions). This method is similar to the expect() method except that
        expect_list() does not recompile the pattern list on every call. This
        may help if you are trying to optimize for speed, otherwise just use
        the expect() method.  This is called by expect().


        Like :meth:`expect`, passing ``async_=True`` will make this return an
        asyncio coroutine.
        """

    @overload
    def expect_list(
        self,
        pattern_list: list[_CompiledRePattern[AnyStr]],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        *,
        async_: Literal[True],
    ) -> Awaitable[int]: ...
    @overload
    def expect_exact(
        self,
        pattern_list: _InputStringPattern | Iterable[_InputStringPattern],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        async_: Literal[False] = False,
    ) -> int:
        """This is similar to expect(), but uses plain string matching instead
        of compiled regular expressions in 'pattern_list'. The 'pattern_list'
        may be a string; a list or other sequence of strings; or TIMEOUT and
        EOF.

        This call might be faster than expect() for two reasons: string
        searching is faster than RE matching and it is possible to limit the
        search to just the end of the input buffer.

        This method is also useful when you don't want to have to worry about
        escaping regular expression characters that you want to match.

        Like :meth:`expect`, passing ``async_=True`` will make this return an
        asyncio coroutine.
        """

    @overload
    def expect_exact(
        self,
        pattern_list: _InputStringPattern | Iterable[_InputStringPattern],
        timeout: float | None = -1,
        searchwindowsize: int | None = -1,
        *,
        async_: Literal[True],
    ) -> Awaitable[int]: ...
    def expect_loop(self, searcher: _Searcher[AnyStr], timeout: float | None = -1, searchwindowsize: int | None = -1) -> int:
        """This is the common loop used inside expect. The 'searcher' should be
        an instance of searcher_re or searcher_string, which describes how and
        what to search for in the input.

        See expect() for other arguments, return value and exceptions.
        """

    def read(self, size: int = -1) -> AnyStr:
        """This reads at most "size" bytes from the file (less if the read hits
        EOF before obtaining size bytes). If the size argument is negative or
        omitted, read all data until EOF is reached. The bytes are returned as
        a string object. An empty string is returned when EOF is encountered
        immediately.
        """

    def readline(self, size: int = -1) -> AnyStr:
        """This reads and returns one entire line. The newline at the end of
        line is returned as part of the string, unless the file ends without a
        newline. An empty string is returned if EOF is encountered immediately.
        This looks for a newline as a CR/LF pair (\\r\\n) even on UNIX because
        this is what the pseudotty device returns. So contrary to what you may
        expect you will receive newlines as \\r\\n.

        If the size argument is 0 then an empty string is returned. In all
        other cases the size argument is ignored, which is not standard
        behavior for a file-like object.
        """

    def __iter__(self):
        """This is to support iterators over a file-like object."""

    def readlines(self, sizehint: int = -1) -> list[AnyStr]:
        """This reads until EOF using readline() and returns a list containing
        the lines thus read. The optional 'sizehint' argument is ignored.
        Remember, because this reads until EOF that means the child
        process should have closed its stdout. If you run this method on
        a child that is still running with its stdout open then this
        method will block until it timesout.
        """

    def fileno(self) -> int:
        """Expose file descriptor for a file-like interface"""

    def flush(self) -> None:
        """This does nothing. It is here to support the interface for a
        File-like object.
        """

    def isatty(self) -> bool:
        """Overridden in subclass using tty"""

    def __enter__(self): ...
    def __exit__(self, etype, evalue, tb) -> None: ...
