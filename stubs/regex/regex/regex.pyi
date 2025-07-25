"""Support for regular expressions (RE).

This module provides regular expression matching operations similar to those
found in Perl. It supports both 8-bit and Unicode strings; both the pattern and
the strings being processed can contain null bytes and characters outside the
US ASCII range.

Regular expressions can contain both special and ordinary characters. Most
ordinary characters, like "A", "a", or "0", are the simplest regular
expressions; they simply match themselves. You can concatenate ordinary
characters, so last matches the string 'last'.

There are a few differences between the old (legacy) behaviour and the new
(enhanced) behaviour, which are indicated by VERSION0 or VERSION1.

The special characters are:
    "."                 Matches any character except a newline.
    "^"                 Matches the start of the string.
    "$"                 Matches the end of the string or just before the
                        newline at the end of the string.
    "*"                 Matches 0 or more (greedy) repetitions of the preceding
                        RE. Greedy means that it will match as many repetitions
                        as possible.
    "+"                 Matches 1 or more (greedy) repetitions of the preceding
                        RE.
    "?"                 Matches 0 or 1 (greedy) of the preceding RE.
    *?,+?,??            Non-greedy versions of the previous three special
                        characters.
    *+,++,?+            Possessive versions of the previous three special
                        characters.
    {m,n}               Matches from m to n repetitions of the preceding RE.
    {m,n}?              Non-greedy version of the above.
    {m,n}+              Possessive version of the above.
    {...}               Fuzzy matching constraints.
    "\\\\"                Either escapes special characters or signals a special
                        sequence.
    [...]               Indicates a set of characters. A "^" as the first
                        character indicates a complementing set.
    "|"                 A|B, creates an RE that will match either A or B.
    (...)               Matches the RE inside the parentheses. The contents are
                        captured and can be retrieved or matched later in the
                        string.
    (?flags-flags)      VERSION1: Sets/clears the flags for the remainder of
                        the group or pattern; VERSION0: Sets the flags for the
                        entire pattern.
    (?:...)             Non-capturing version of regular parentheses.
    (?>...)             Atomic non-capturing version of regular parentheses.
    (?flags-flags:...)  Non-capturing version of regular parentheses with local
                        flags.
    (?P<name>...)       The substring matched by the group is accessible by
                        name.
    (?<name>...)        The substring matched by the group is accessible by
                        name.
    (?P=name)           Matches the text matched earlier by the group named
                        name.
    (?#...)             A comment; ignored.
    (?=...)             Matches if ... matches next, but doesn't consume the
                        string.
    (?!...)             Matches if ... doesn't match next.
    (?<=...)            Matches if preceded by ....
    (?<!...)            Matches if not preceded by ....
    (?(id)yes|no)       Matches yes pattern if group id matched, the (optional)
                        no pattern otherwise.
    (?(DEFINE)...)      If there's no group called "DEFINE", then ... will be
                        ignored, but any group definitions will be available.
    (?|...|...)         (?|A|B), creates an RE that will match either A or B,
                        but reuses capture group numbers across the
                        alternatives.
    (*FAIL)             Forces matching to fail, which means immediate
                        backtracking.
    (*F)                Abbreviation for (*FAIL).
    (*PRUNE)            Discards the current backtracking information. Its
                        effect doesn't extend outside an atomic group or a
                        lookaround.
    (*SKIP)             Similar to (*PRUNE), except that it also sets where in
                        the text the next attempt at matching the entire
                        pattern will start. Its effect doesn't extend outside
                        an atomic group or a lookaround.

The fuzzy matching constraints are: "i" to permit insertions, "d" to permit
deletions, "s" to permit substitutions, "e" to permit any of these. Limits are
optional with "<=" and "<". If any type of error is provided then any type not
provided is not permitted.

A cost equation may be provided.

Examples:
    (?:fuzzy){i<=2}
    (?:fuzzy){i<=1,s<=2,d<=1,1i+1s+1d<3}

VERSION1: Set operators are supported, and a set can include nested sets. The
set operators, in order of increasing precedence, are:
    ||  Set union ("x||y" means "x or y").
    ~~  (double tilde) Symmetric set difference ("x~~y" means "x or y, but not
        both").
    &&  Set intersection ("x&&y" means "x and y").
    --  (double dash) Set difference ("x--y" means "x but not y").

Implicit union, ie, simple juxtaposition like in [ab], has the highest
precedence.

VERSION0 and VERSION1:
The special sequences consist of "\\\\" and a character from the list below. If
the ordinary character is not on the list, then the resulting RE will match the
second character.
    \\number         Matches the contents of the group of the same number if
                    number is no more than 2 digits, otherwise the character
                    with the 3-digit octal code.
    \\a              Matches the bell character.
    \\A              Matches only at the start of the string.
    \\b              Matches the empty string, but only at the start or end of a
                    word.
    \\B              Matches the empty string, but not at the start or end of a
                    word.
    \\d              Matches any decimal digit; equivalent to the set [0-9] when
                    matching a bytestring or a Unicode string with the ASCII
                    flag, or the whole range of Unicode digits when matching a
                    Unicode string.
    \\D              Matches any non-digit character; equivalent to [^\\d].
    \\f              Matches the formfeed character.
    \\g<name>        Matches the text matched by the group named name.
    \\G              Matches the empty string, but only at the position where
                    the search started.
    \\h              Matches horizontal whitespace.
    \\K              Keeps only what follows for the entire match.
    \\L<name>        Named list. The list is provided as a keyword argument.
    \\m              Matches the empty string, but only at the start of a word.
    \\M              Matches the empty string, but only at the end of a word.
    \\n              Matches the newline character.
    \\N{name}        Matches the named character.
    \\p{name=value}  Matches the character if its property has the specified
                    value.
    \\P{name=value}  Matches the character if its property hasn't the specified
                    value.
    \\r              Matches the carriage-return character.
    \\s              Matches any whitespace character; equivalent to
                    [ \\t\\n\\r\\f\\v].
    \\S              Matches any non-whitespace character; equivalent to [^\\s].
    \\t              Matches the tab character.
    \\uXXXX          Matches the Unicode codepoint with 4-digit hex code XXXX.
    \\UXXXXXXXX      Matches the Unicode codepoint with 8-digit hex code
                    XXXXXXXX.
    \\v              Matches the vertical tab character.
    \\w              Matches any alphanumeric character; equivalent to
                    [a-zA-Z0-9_] when matching a bytestring or a Unicode string
                    with the ASCII flag, or the whole range of Unicode
                    alphanumeric characters (letters plus digits plus
                    underscore) when matching a Unicode string. With LOCALE, it
                    will match the set [0-9_] plus characters defined as
                    letters for the current locale.
    \\W              Matches the complement of \\w; equivalent to [^\\w].
    \\xXX            Matches the character with 2-digit hex code XX.
    \\X              Matches a grapheme.
    \\Z              Matches only at the end of the string.
    \\\\              Matches a literal backslash.

This module exports the following functions:
    match      Match a regular expression pattern at the beginning of a string.
    fullmatch  Match a regular expression pattern against all of a string.
    search     Search a string for the presence of a pattern.
    sub        Substitute occurrences of a pattern found in a string using a
               template string.
    subf       Substitute occurrences of a pattern found in a string using a
               format string.
    subn       Same as sub, but also return the number of substitutions made.
    subfn      Same as subf, but also return the number of substitutions made.
    split      Split a string by the occurrences of a pattern. VERSION1: will
               split at zero-width match; VERSION0: won't split at zero-width
               match.
    splititer  Return an iterator yielding the parts of a split string.
    findall    Find all occurrences of a pattern in a string.
    finditer   Return an iterator yielding a match object for each match.
    compile    Compile a pattern into a Pattern object.
    purge      Clear the regular expression cache.
    escape     Backslash all non-alphanumerics or special characters in a
               string.

Most of the functions support a concurrent parameter: if True, the GIL will be
released during matching, allowing other Python threads to run concurrently. If
the string changes during matching, the behaviour is undefined. This parameter
is not needed when working on the builtin (immutable) string classes.

Some of the functions in this module take flags as optional parameters. Most of
these flags can also be set within an RE:
    A   a   ASCII         Make \\w, \\W, \\b, \\B, \\d, and \\D match the
                          corresponding ASCII character categories. Default
                          when matching a bytestring.
    B   b   BESTMATCH     Find the best fuzzy match (default is first).
    D       DEBUG         Print the parsed pattern.
    E   e   ENHANCEMATCH  Attempt to improve the fit after finding the first
                          fuzzy match.
    F   f   FULLCASE      Use full case-folding when performing
                          case-insensitive matching in Unicode.
    I   i   IGNORECASE    Perform case-insensitive matching.
    L   L   LOCALE        Make \\w, \\W, \\b, \\B, \\d, and \\D dependent on the
                          current locale. (One byte per character only.)
    M   m   MULTILINE     "^" matches the beginning of lines (after a newline)
                          as well as the string. "$" matches the end of lines
                          (before a newline) as well as the end of the string.
    P   p   POSIX         Perform POSIX-standard matching (leftmost longest).
    R   r   REVERSE       Searches backwards.
    S   s   DOTALL        "." matches any character at all, including the
                          newline.
    U   u   UNICODE       Make \\w, \\W, \\b, \\B, \\d, and \\D dependent on the
                          Unicode locale. Default when matching a Unicode
                          string.
    V0  V0  VERSION0      Turn on the old legacy behaviour.
    V1  V1  VERSION1      Turn on the new enhanced behaviour. This flag
                          includes the FULLCASE flag.
    W   w   WORD          Make \\b and \\B work with default Unicode word breaks
                          and make ".", "^" and "$" work with Unicode line
                          breaks.
    X   x   VERBOSE       Ignore whitespace and comments for nicer looking REs.

This module also defines an exception 'error'.

"""

from _typeshed import ReadableBuffer, Unused
from collections.abc import Callable, Mapping
from types import GenericAlias
from typing import Any, AnyStr, Generic, Literal, TypeVar, final, overload
from typing_extensions import Self

from . import _regex
from ._regex_core import *

_T = TypeVar("_T")

__version__: str

def compile(
    pattern: AnyStr | Pattern[AnyStr],
    flags: int = 0,
    ignore_unused: bool = False,
    cache_pattern: bool | None = None,
    **kwargs: Any,
) -> Pattern[AnyStr]:
    """Compile a regular expression pattern, returning a pattern object."""

@overload
def search(
    pattern: str | Pattern[str],
    string: str,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[str] | None:
    """Search through string looking for a match to the pattern, returning a
    match object, or None if no match was found.
    """

@overload
def search(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[bytes] | None: ...
@overload
def match(
    pattern: str | Pattern[str],
    string: str,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[str] | None:
    """Try to apply the pattern at the start of the string, returning a match
    object, or None if no match was found.
    """

@overload
def match(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[bytes] | None: ...
@overload
def fullmatch(
    pattern: str | Pattern[str],
    string: str,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[str] | None:
    """Try to apply the pattern against all of the string, returning a match
    object, or None if no match was found.
    """

@overload
def fullmatch(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> Match[bytes] | None: ...
@overload
def split(
    pattern: str | Pattern[str],
    string: str,
    maxsplit: int = 0,
    flags: int = 0,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> list[str | Any]:
    """Split the source string by the occurrences of the pattern, returning a
    list containing the resulting substrings.  If capturing parentheses are used
    in pattern, then the text of all groups in the pattern are also returned as
    part of the resulting list.  If maxsplit is nonzero, at most maxsplit splits
    occur, and the remainder of the string is returned as the final element of
    the list.
    """

@overload
def split(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    maxsplit: int = 0,
    flags: int = 0,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> list[bytes | Any]: ...
@overload
def splititer(
    pattern: str | Pattern[str],
    string: str,
    maxsplit: int = 0,
    flags: int = 0,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> _regex.Splitter[str]:
    """Return an iterator yielding the parts of a split string."""

@overload
def splititer(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    maxsplit: int = 0,
    flags: int = 0,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> _regex.Splitter[bytes]: ...
@overload
def findall(
    pattern: str | Pattern[str],
    string: str,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    overlapped: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> list[Any]:
    """Return a list of all matches in the string. The matches may be overlapped
    if overlapped is True. If one or more groups are present in the pattern,
    return a list of groups; this will be a list of tuples if the pattern has
    more than one group. Empty matches are included in the result.
    """

@overload
def findall(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    overlapped: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> list[Any]: ...
@overload
def finditer(
    pattern: str | Pattern[str],
    string: str,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    overlapped: bool = False,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> _regex.Scanner[str]:
    """Return an iterator over all matches in the string. The matches may be
    overlapped if overlapped is True. For each match, the iterator returns a
    match object. Empty matches are included in the result.
    """

@overload
def finditer(
    pattern: bytes | Pattern[bytes],
    string: ReadableBuffer,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    overlapped: bool = False,
    partial: bool = False,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> _regex.Scanner[bytes]: ...
@overload
def sub(
    pattern: str | Pattern[str],
    repl: str | Callable[[Match[str]], str],
    string: str,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> str:
    """Return the string obtained by replacing the leftmost (or rightmost with a
    reverse pattern) non-overlapping occurrences of the pattern in string by the
    replacement repl. repl can be either a string or a callable; if a string,
    backslash escapes in it are processed; if a callable, it's passed the match
    object and must return a replacement string to be used.
    """

@overload
def sub(
    pattern: bytes | Pattern[bytes],
    repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> bytes: ...
@overload
def subf(
    pattern: str | Pattern[str],
    format: str | Callable[[Match[str]], str],
    string: str,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> str:
    """Return the string obtained by replacing the leftmost (or rightmost with a
    reverse pattern) non-overlapping occurrences of the pattern in string by the
    replacement format. format can be either a string or a callable; if a string,
    it's treated as a format string; if a callable, it's passed the match object
    and must return a replacement string to be used.
    """

@overload
def subf(
    pattern: bytes | Pattern[bytes],
    format: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> bytes: ...
@overload
def subn(
    pattern: str | Pattern[str],
    repl: str | Callable[[Match[str]], str],
    string: str,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> tuple[str, int]:
    """Return a 2-tuple containing (new_string, number). new_string is the string
    obtained by replacing the leftmost (or rightmost with a reverse pattern)
    non-overlapping occurrences of the pattern in the source string by the
    replacement repl. number is the number of substitutions that were made. repl
    can be either a string or a callable; if a string, backslash escapes in it
    are processed; if a callable, it's passed the match object and must return a
    replacement string to be used.
    """

@overload
def subn(
    pattern: bytes | Pattern[bytes],
    repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> tuple[bytes, int]: ...
@overload
def subfn(
    pattern: str | Pattern[str],
    format: str | Callable[[Match[str]], str],
    string: str,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> tuple[str, int]:
    """Return a 2-tuple containing (new_string, number). new_string is the string
    obtained by replacing the leftmost (or rightmost with a reverse pattern)
    non-overlapping occurrences of the pattern in the source string by the
    replacement format. number is the number of substitutions that were made. format
    can be either a string or a callable; if a string, it's treated as a format
    string; if a callable, it's passed the match object and must return a
    replacement string to be used.
    """

@overload
def subfn(
    pattern: bytes | Pattern[bytes],
    format: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
    string: ReadableBuffer,
    count: int = 0,
    flags: int = 0,
    pos: int | None = None,
    endpos: int | None = None,
    concurrent: bool | None = None,
    timeout: float | None = None,
    ignore_unused: bool = False,
    **kwargs: Any,
) -> tuple[bytes, int]: ...
def purge() -> None:
    """Clear the regular expression cache"""

@overload
def cache_all(value: bool = True) -> None:
    """Sets whether to cache all patterns, even those are compiled explicitly.
    Passing None has no effect, but returns the current setting.
    """

@overload
def cache_all(value: None) -> bool: ...
def escape(pattern: AnyStr, special_only: bool = True, literal_spaces: bool = False) -> AnyStr:
    """Escape a string for use as a literal in a pattern. If special_only is
    True, escape only special characters, else escape all non-alphanumeric
    characters. If literal_spaces is True, don't escape spaces.
    """

def template(pattern: AnyStr | Pattern[AnyStr], flags: int = 0) -> Pattern[AnyStr]:
    """Compile a template pattern, returning a pattern object."""

Regex = compile

@final
class Pattern(Generic[AnyStr]):
    """Compiled regex object"""

    @property
    def flags(self) -> int:
        """The regex matching flags."""

    @property
    def groupindex(self) -> Mapping[str, int]:
        """A dictionary mapping group names to group numbers."""

    @property
    def groups(self) -> int:
        """The number of capturing groups in the pattern."""

    @property
    def pattern(self) -> AnyStr:
        """The pattern string from which the regex object was compiled."""

    @property
    def named_lists(self) -> Mapping[str, frozenset[AnyStr]]:
        """The named lists used by the regex."""

    @overload
    def search(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[str] | None:
        """search(string, pos=None, endpos=None, concurrent=None, timeout=None) --> MatchObject or None.
        Search through string looking for a match, and return a corresponding
        match object instance.  Return None if no match is found.
        """

    @overload
    def search(
        self: Pattern[bytes],
        string: ReadableBuffer,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[bytes] | None: ...
    @overload
    def match(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[str] | None:
        """match(string, pos=None, endpos=None, concurrent=None, timeout=None) --> MatchObject or None.
        Match zero or more characters at the beginning of the string.
        """

    @overload
    def match(
        self: Pattern[bytes],
        string: ReadableBuffer,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[bytes] | None: ...
    @overload
    def fullmatch(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[str] | None:
        """fullmatch(string, pos=None, endpos=None, concurrent=None, timeout=None) --> MatchObject or None.
        Match zero or more characters against all of the string.
        """

    @overload
    def fullmatch(
        self: Pattern[bytes],
        string: ReadableBuffer,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> Match[bytes] | None: ...
    @overload
    def split(
        self: Pattern[str], string: str, maxsplit: int = 0, concurrent: bool | None = None, timeout: float | None = None
    ) -> list[str | Any]:
        """split(string, maxsplit=0, concurrent=None, timeout=None) --> list.
        Split string by the occurrences of pattern.
        """

    @overload
    def split(
        self: Pattern[bytes],
        string: ReadableBuffer,
        maxsplit: int = 0,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> list[bytes | Any]: ...
    @overload
    def splititer(
        self: Pattern[str], string: str, maxsplit: int = 0, concurrent: bool | None = None, timeout: float | None = None
    ) -> _regex.Splitter[str]:
        """splititer(string, maxsplit=0, concurrent=None, timeout=None) --> iterator.
        Return an iterator yielding the parts of a split string.
        """

    @overload
    def splititer(
        self: Pattern[bytes],
        string: ReadableBuffer,
        maxsplit: int = 0,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> _regex.Splitter[bytes]: ...
    @overload
    def findall(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> list[Any]:
        """findall(string, pos=None, endpos=None, overlapped=False, concurrent=None, timeout=None) --> list.
        Return a list of all matches of pattern in string.  The matches may be
        overlapped if overlapped is True.
        """

    @overload
    def findall(
        self: Pattern[bytes],
        string: ReadableBuffer,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> list[Any]: ...
    @overload
    def finditer(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> _regex.Scanner[str]:
        """finditer(string, pos=None, endpos=None, overlapped=False, concurrent=None, timeout=None) --> iterator.
        Return an iterator over all matches for the RE pattern in string.  The
        matches may be overlapped if overlapped is True.  For each match, the
        iterator returns a MatchObject.
        """

    @overload
    def finditer(
        self: Pattern[bytes],
        string: ReadableBuffer,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> _regex.Scanner[bytes]: ...
    @overload
    def sub(
        self: Pattern[str],
        repl: str | Callable[[Match[str]], str],
        string: str,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> str:
        """sub(repl, string, count=0, flags=0, pos=None, endpos=None, concurrent=None, timeout=None) --> newstring
        Return the string obtained by replacing the leftmost (or rightmost with a
        reverse pattern) non-overlapping occurrences of pattern in string by the
        replacement repl.
        """

    @overload
    def sub(
        self: Pattern[bytes],
        repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> bytes: ...
    @overload
    def subf(
        self: Pattern[str],
        format: str | Callable[[Match[str]], str],
        string: str,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> str:
        """subf(format, string, count=0, flags=0, pos=None, endpos=None, concurrent=None, timeout=None) --> newstring
        Return the string obtained by replacing the leftmost (or rightmost with a
        reverse pattern) non-overlapping occurrences of pattern in string by the
        replacement format.
        """

    @overload
    def subf(
        self: Pattern[bytes],
        format: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> bytes: ...
    @overload
    def subn(
        self: Pattern[str],
        repl: str | Callable[[Match[str]], str],
        string: str,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> tuple[str, int]:
        """subn(repl, string, count=0, flags=0, pos=None, endpos=None, concurrent=None, timeout=None) --> (newstring, number of subs)
        Return the tuple (new_string, number_of_subs_made) found by replacing the
        leftmost (or rightmost with a reverse pattern) non-overlapping occurrences
        of pattern with the replacement repl.
        """

    @overload
    def subn(
        self: Pattern[bytes],
        repl: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> tuple[bytes, int]: ...
    @overload
    def subfn(
        self: Pattern[str],
        format: str | Callable[[Match[str]], str],
        string: str,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> tuple[str, int]:
        """subfn(format, string, count=0, flags=0, pos=None, endpos=None, concurrent=None, timeout=None) --> (newstring, number of subs)
        Return the tuple (new_string, number_of_subs_made) found by replacing the
        leftmost (or rightmost with a reverse pattern) non-overlapping occurrences
        of pattern with the replacement format.
        """

    @overload
    def subfn(
        self: Pattern[bytes],
        format: ReadableBuffer | Callable[[Match[bytes]], ReadableBuffer],
        string: ReadableBuffer,
        count: int = 0,
        pos: int | None = None,
        endpos: int | None = None,
        concurrent: bool | None = None,
        timeout: float | None = None,
    ) -> tuple[bytes, int]: ...
    @overload
    def scanner(
        self: Pattern[str],
        string: str,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> _regex.Scanner[str]:
        """scanner(string, pos=None, endpos=None, overlapped=False, concurrent=None, timeout=None) --> scanner.
        Return an scanner for the RE pattern in string.  The matches may be overlapped
        if overlapped is True.
        """

    @overload
    def scanner(
        self: Pattern[bytes],
        string: bytes,
        pos: int | None = None,
        endpos: int | None = None,
        overlapped: bool = False,
        concurrent: bool | None = None,
        partial: bool = False,
        timeout: float | None = None,
    ) -> _regex.Scanner[bytes]: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: Unused, /) -> Self: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias:
        """See PEP 585"""

@final
class Match(Generic[AnyStr]):
    """Match object"""

    @property
    def pos(self) -> int:
        """The position at which the regex engine starting searching."""

    @property
    def endpos(self) -> int:
        """The final position beyond which the regex engine won't search."""

    @property
    def lastindex(self) -> int | None:
        """The group number of the last matched capturing group, or None."""

    @property
    def lastgroup(self) -> str | None:
        """The name of the last matched capturing group, or None."""

    @property
    def string(self) -> AnyStr:
        """The string that was searched, or None if it has been detached."""

    @property
    def re(self) -> Pattern[AnyStr]:
        """The regex object that produced this match object."""

    @property
    def partial(self) -> bool:
        """Whether it's a partial match."""

    @property
    def regs(self) -> tuple[tuple[int, int], ...]:
        """A tuple of the spans of the capturing groups."""

    @property
    def fuzzy_counts(self) -> tuple[int, int, int]:
        """A tuple of the number of substitutions, insertions and deletions."""

    @property
    def fuzzy_changes(self) -> tuple[list[int], list[int], list[int]]:
        """A tuple of the positions of the substitutions, insertions and deletions."""

    @overload
    def group(self, group: Literal[0] = 0, /) -> AnyStr:
        """group([group1, ...]) --> string or tuple of strings.
        Return one or more subgroups of the match.  If there is a single argument,
        the result is a single string, or None if the group did not contribute to
        the match; if there are multiple arguments, the result is a tuple with one
        item per argument; if there are no arguments, the whole match is returned.
        Group 0 is the whole match.
        """

    @overload
    def group(self, group: int | str = ..., /) -> AnyStr | Any: ...
    @overload
    def group(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[AnyStr | Any, ...]: ...
    @overload
    def groups(self, default: None = None) -> tuple[AnyStr | Any, ...]:
        """groups(default=None) --> tuple of strings.
        Return a tuple containing all the subgroups of the match.  The argument is
        the default for groups that did not participate in the match.
        """

    @overload
    def groups(self, default: _T) -> tuple[AnyStr | _T, ...]: ...
    @overload
    def groupdict(self, default: None = None) -> dict[str, AnyStr | Any]:
        """groupdict(default=None) --> dict.
        Return a dictionary containing all the named subgroups of the match, keyed
        by the subgroup name.  The argument is the value to be given for groups that
        did not participate in the match.
        """

    @overload
    def groupdict(self, default: _T) -> dict[str, AnyStr | _T]: ...
    @overload
    def span(self, group: int | str = ..., /) -> tuple[int, int]:
        """span([group1, ...]) --> 2-tuple of int or tuple of 2-tuple of ints.
        Return the span (a 2-tuple of the indices of the start and end) of one or
        more subgroups of the match.  If there is a single argument, the result is a
        span, or (-1, -1) if the group did not contribute to the match; if there are
        multiple arguments, the result is a tuple with one item per argument; if
        there are no arguments, the span of the whole match is returned.  Group 0 is
        the whole match.
        """

    @overload
    def span(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[tuple[int, int], ...]: ...
    @overload
    def spans(self, group: int | str = ..., /) -> list[tuple[int, int]]:
        """spans([group1, ...]) --> list of 2-tuple of ints or tuple of list of 2-tuple of ints.
        Return the spans (a 2-tuple of the indices of the start and end) of the
        captures of one or more subgroups of the match.  If there is a single
        argument, the result is a list of spans; if there are multiple arguments,
        the result is a tuple of lists with one item per argument; if there are no
        arguments, the spans of the captures of the whole match is returned.  Group
        0 is the whole match.
        """

    @overload
    def spans(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[list[tuple[int, int]], ...]: ...
    @overload
    def start(self, group: int | str = ..., /) -> int:
        """start([group1, ...]) --> int or tuple of ints.
        Return the index of the start of one or more subgroups of the match.  If
        there is a single argument, the result is an index, or -1 if the group did
        not contribute to the match; if there are multiple arguments, the result is
        a tuple with one item per argument; if there are no arguments, the index of
        the start of the whole match is returned.  Group 0 is the whole match.
        """

    @overload
    def start(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[int, ...]: ...
    @overload
    def starts(self, group: int | str = ..., /) -> list[int]:
        """starts([group1, ...]) --> list of ints or tuple of list of ints.
        Return the indices of the starts of the captures of one or more subgroups of
        the match.  If there is a single argument, the result is a list of indices;
        if there are multiple arguments, the result is a tuple of lists with one
        item per argument; if there are no arguments, the indices of the starts of
        the captures of the whole match is returned.  Group 0 is the whole match.
        """

    @overload
    def starts(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[list[int], ...]: ...
    @overload
    def end(self, group: int | str = ..., /) -> int:
        """end([group1, ...]) --> int or tuple of ints.
        Return the index of the end of one or more subgroups of the match.  If there
        is a single argument, the result is an index, or -1 if the group did not
        contribute to the match; if there are multiple arguments, the result is a
        tuple with one item per argument; if there are no arguments, the index of
        the end of the whole match is returned.  Group 0 is the whole match.
        """

    @overload
    def end(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[int, ...]: ...
    @overload
    def ends(self, group: int | str = ..., /) -> list[int]:
        """ends([group1, ...]) --> list of ints or tuple of list of ints.
        Return the indices of the ends of the captures of one or more subgroups of
        the match.  If there is a single argument, the result is a list of indices;
        if there are multiple arguments, the result is a tuple of lists with one
        item per argument; if there are no arguments, the indices of the ends of the
        captures of the whole match is returned.  Group 0 is the whole match.
        """

    @overload
    def ends(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[list[int], ...]: ...
    def expand(self, template: AnyStr, /) -> AnyStr:
        """expand(template) --> string.
        Return the string obtained by doing backslash substitution on the template,
        as done by the sub() method.
        """

    def expandf(self, format: AnyStr, /) -> AnyStr:
        """expandf(format) --> string.
        Return the string obtained by using the format, as done by the subf()
        method.
        """

    @overload
    def captures(self, group: int | str = ..., /) -> list[AnyStr]:
        """captures([group1, ...]) --> list of strings or tuple of list of strings.
        Return the captures of one or more subgroups of the match.  If there is a
        single argument, the result is a list of strings; if there are multiple
        arguments, the result is a tuple of lists with one item per argument; if
        there are no arguments, the captures of the whole match is returned.  Group
        0 is the whole match.
        """

    @overload
    def captures(self, group1: int | str, group2: int | str, /, *groups: int | str) -> tuple[list[AnyStr], ...]: ...
    def capturesdict(self) -> dict[str, list[AnyStr]]:
        """capturesdict() --> dict.
        Return a dictionary containing the captures of all the named subgroups of the
        match, keyed by the subgroup name.
        """

    def detach_string(self) -> None:
        """detach_string()
        Detaches the target string from the match object. The 'string' attribute
        will become None.
        """

    def allcaptures(self) -> tuple[list[AnyStr]]:
        """allcaptures() --> list of strings or tuple of list of strings.
        Return the captures of all the groups of the match and the whole match.
        """

    def allspans(self) -> tuple[list[tuple[int, int]]]:
        """allspans() --> list of 2-tuple of ints or tuple of list of 2-tuple of ints.
        Return the spans (a 2-tuple of the indices of the start and end) of all the
        captures of all the groups of the match and the whole match.
        """

    @overload
    def __getitem__(self, key: Literal[0], /) -> AnyStr: ...
    @overload
    def __getitem__(self, key: int | str, /) -> AnyStr | Any: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: Unused, /) -> Self: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias:
        """See PEP 585"""
