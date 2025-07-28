"""So much practical programming involves string manipulation, which
Python readily accommodates. Still, there are dozens of basic and
common capabilities missing from the standard library, several of them
provided by ``strutils``.
"""

from _typeshed import ReadableBuffer
from collections.abc import Callable, Generator, Iterable, Sized
from html.parser import HTMLParser
from re import Pattern
from typing import Literal, overload

def camel2under(camel_string: str) -> str:
    """Converts a camelcased string to underscores. Useful for turning a
    class name into a function name.

    >>> camel2under('BasicParseTest')
    'basic_parse_test'
    """

def under2camel(under_string: str) -> str:
    """Converts an underscored string to camelcased. Useful for turning a
    function name into a class name.

    >>> under2camel('complex_tokenizer')
    'ComplexTokenizer'
    """

@overload
def slugify(text: str, delim: str = "_", lower: bool = True, *, ascii: Literal[True]) -> bytes:
    """
    A basic function that turns text full of scary characters
    (i.e., punctuation and whitespace), into a relatively safe
    lowercased string separated only by the delimiter specified
    by *delim*, which defaults to ``_``.

    The *ascii* convenience flag will :func:`asciify` the slug if
    you require ascii-only slugs.

    >>> slugify('First post! Hi!!!!~1    ')
    'first_post_hi_1'

    >>> slugify("Kurt Gödel's pretty cool.", ascii=True) ==         b'kurt_goedel_s_pretty_cool'
    True

    """

@overload
def slugify(text: str, delim: str, lower: bool, ascii: Literal[True]) -> bytes: ...
@overload
def slugify(text: str, delim: str = "_", lower: bool = True, ascii: Literal[False] = False) -> str: ...
def split_punct_ws(text: str) -> list[str]:
    """While :meth:`str.split` will split on whitespace,
    :func:`split_punct_ws` will split on punctuation and
    whitespace. This used internally by :func:`slugify`, above.

    >>> split_punct_ws('First post! Hi!!!!~1    ')
    ['First', 'post', 'Hi', '1']
    """

def unit_len(sized_iterable: Sized, unit_noun: str = "item") -> str:
    """Returns a plain-English description of an iterable's
    :func:`len()`, conditionally pluralized with :func:`cardinalize`,
    detailed below.

    >>> print(unit_len(range(10), 'number'))
    10 numbers
    >>> print(unit_len('aeiou', 'vowel'))
    5 vowels
    >>> print(unit_len([], 'worry'))
    No worries
    """

def ordinalize(number: int | str, ext_only: bool = False) -> str:
    """Turns *number* into its cardinal form, i.e., 1st, 2nd,
    3rd, 4th, etc. If the last character isn't a digit, it returns the
    string value unchanged.

    Args:
        number (int or str): Number to be cardinalized.
        ext_only (bool): Whether to return only the suffix. Default ``False``.

    >>> print(ordinalize(1))
    1st
    >>> print(ordinalize(3694839230))
    3694839230th
    >>> print(ordinalize('hi'))
    hi
    >>> print(ordinalize(1515))
    1515th
    """

def cardinalize(unit_noun: str, count: int) -> str:
    """Conditionally pluralizes a singular word *unit_noun* if
    *count* is not one, preserving case when possible.

    >>> vowels = 'aeiou'
    >>> print(len(vowels), cardinalize('vowel', len(vowels)))
    5 vowels
    >>> print(3, cardinalize('Wish', 3))
    3 Wishes
    """

def singularize(word: str) -> str:
    """Semi-intelligently converts an English plural *word* to its
    singular form, preserving case pattern.

    >>> singularize('chances')
    'chance'
    >>> singularize('Activities')
    'Activity'
    >>> singularize('Glasses')
    'Glass'
    >>> singularize('FEET')
    'FOOT'

    """

def pluralize(word: str) -> str:
    """Semi-intelligently converts an English *word* from singular form to
    plural, preserving case pattern.

    >>> pluralize('friend')
    'friends'
    >>> pluralize('enemy')
    'enemies'
    >>> pluralize('Sheep')
    'Sheep'
    """

def find_hashtags(string: str) -> list[str]:
    """Finds and returns all hashtags in a string, with the hashmark
    removed. Supports full-width hashmarks for Asian languages and
    does not false-positive on URL anchors.

    >>> find_hashtags('#atag http://asite/#ananchor')
    ['atag']

    ``find_hashtags`` also works with unicode hashtags.
    """

def a10n(string: str) -> str:
    """That thing where "internationalization" becomes "i18n", what's it
    called? Abbreviation? Oh wait, no: ``a10n``. (It's actually a form
    of `numeronym`_.)

    >>> a10n('abbreviation')
    'a10n'
    >>> a10n('internationalization')
    'i18n'
    >>> a10n('')
    ''

    .. _numeronym: http://en.wikipedia.org/wiki/Numeronym
    """

def strip_ansi(text: str) -> str:
    """Strips ANSI escape codes from *text*. Useful for the occasional
    time when a log or redirected output accidentally captures console
    color codes and the like.

    >>> strip_ansi('\x1b[0m\x1b[1;36mart\x1b[46;34m')
    'art'

    Supports str, bytes and bytearray content as input. Returns the
    same type as the input.

    There's a lot of ANSI art available for testing on `sixteencolors.net`_.
    This function does not interpret or render ANSI art, but you can do so with
    `ansi2img`_ or `escapes.js`_.

    .. _sixteencolors.net: http://sixteencolors.net
    .. _ansi2img: http://www.bedroomlan.org/projects/ansi2img
    .. _escapes.js: https://github.com/atdt/escapes.js
    """

def asciify(text: str | bytes | bytearray, ignore: bool = False) -> bytes:
    """Converts a unicode or bytestring, *text*, into a bytestring with
    just ascii characters. Performs basic deaccenting for all you
    Europhiles out there.

    Also, a gentle reminder that this is a **utility**, primarily meant
    for slugification. Whenever possible, make your application work
    **with** unicode, not against it.

    Args:
        text (str): The string to be asciified.
        ignore (bool): Configures final encoding to ignore remaining
            unasciified string instead of replacing it.

    >>> asciify('Beyoncé') == b'Beyonce'
    True
    """

def is_ascii(text: str) -> bool:
    """Check if a string or bytestring, *text*, is composed of ascii
    characters only. Raises :exc:`ValueError` if argument is not text.

    Args:
        text (str): The string to be checked.

    >>> is_ascii('Beyoncé')
    False
    >>> is_ascii('Beyonce')
    True
    """

class DeaccenterDict(dict[int, int]):
    """A small caching dictionary for deaccenting."""

    def __missing__(self, key: int) -> int: ...

def bytes2human(nbytes: int, ndigits: int = 0) -> str:
    """Turns an integer value of *nbytes* into a human readable format. Set
    *ndigits* to control how many digits after the decimal point
    should be shown (default ``0``).

    >>> bytes2human(128991)
    '126K'
    >>> bytes2human(100001221)
    '95M'
    >>> bytes2human(0, 2)
    '0.00B'
    """

class HTMLTextExtractor(HTMLParser):
    strict: bool
    convert_charrefs: bool
    result: list[str]
    def __init__(self) -> None: ...
    def handle_data(self, d: str) -> None: ...
    def handle_charref(self, number: str) -> None: ...
    def handle_entityref(self, name: str) -> None: ...
    def get_text(self) -> str: ...

def html2text(html: str) -> str:
    """Strips tags from HTML text, returning markup-free text. Also, does
    a best effort replacement of entities like "&nbsp;"

    >>> r = html2text(u'<a href="#">Test &amp;<em>(Δ&#x03b7;&#956;&#x03CE;)</em></a>')
    >>> r == u'Test &(Δημώ)'
    True
    """

def gunzip_bytes(bytestring: ReadableBuffer) -> bytes:
    """The :mod:`gzip` module is great if you have a file or file-like
    object, but what if you just have bytes. StringIO is one
    possibility, but it's often faster, easier, and simpler to just
    use this one-liner. Use this tried-and-true utility function to
    decompress gzip from bytes.

    >>> gunzip_bytes(_EMPTY_GZIP_BYTES) == b''
    True
    >>> gunzip_bytes(_NON_EMPTY_GZIP_BYTES).rstrip() == b'bytesahoy!'
    True
    """

def gzip_bytes(bytestring: ReadableBuffer, level: int = 6) -> int:
    """Turn some bytes into some compressed bytes.

    >>> len(gzip_bytes(b'a' * 10000))
    46

    Args:
        bytestring (bytes): Bytes to be compressed
        level (int): An integer, 1-9, controlling the
          speed/compression. 1 is fastest, least compressed, 9 is
          slowest, but most compressed.

    Note that all levels of gzip are pretty fast these days, though
    it's not really a competitor in compression, at any level.
    """

def iter_splitlines(text: str) -> Generator[str, None, None]:
    """Like :meth:`str.splitlines`, but returns an iterator of lines
    instead of a list. Also similar to :meth:`file.next`, as that also
    lazily reads and yields lines from a file.

    This function works with a variety of line endings, but as always,
    be careful when mixing line endings within a file.

    >>> list(iter_splitlines('\\nhi\\nbye\\n'))
    ['', 'hi', 'bye', '']
    >>> list(iter_splitlines('\\r\\nhi\\rbye\\r\\n'))
    ['', 'hi', 'bye', '']
    >>> list(iter_splitlines(''))
    []
    """

def indent(text: str, margin: str, newline: str = "\n", key: Callable[[str], bool] = ...) -> str:
    """The missing counterpart to the built-in :func:`textwrap.dedent`.

    Args:
        text (str): The text to indent.
        margin (str): The string to prepend to each line.
        newline (str): The newline used to rejoin the lines (default: ``\\n``)
        key (callable): Called on each line to determine whether to
          indent it. Default: :class:`bool`, to ensure that empty lines do
          not get whitespace added.
    """

def is_uuid(obj, version: int = 4) -> bool:
    """Check the argument is either a valid UUID object or string.

    Args:
        obj (object): The test target. Strings and UUID objects supported.
        version (int): The target UUID version, set to 0 to skip version check.

    >>> is_uuid('e682ccca-5a4c-4ef2-9711-73f9ad1e15ea')
    True
    >>> is_uuid('0221f0d9-d4b9-11e5-a478-10ddb1c2feb9')
    False
    >>> is_uuid('0221f0d9-d4b9-11e5-a478-10ddb1c2feb9', version=1)
    True
    """

def escape_shell_args(args: Iterable[str], sep: str = " ", style: Literal["cmd", "sh"] | None = None) -> str:
    """Returns an escaped version of each string in *args*, according to
    *style*.

    Args:
        args (list): A list of arguments to escape and join together
        sep (str): The separator used to join the escaped arguments.
        style (str): The style of escaping to use. Can be one of
          ``cmd`` or ``sh``, geared toward Windows and Linux/BSD/etc.,
          respectively. If *style* is ``None``, then it is picked
          according to the system platform.

    See :func:`args2cmd` and :func:`args2sh` for details and example
    output for each style.
    """

def args2sh(args: Iterable[str], sep: str = " ") -> str:
    """Return a shell-escaped string version of *args*, separated by
    *sep*, based on the rules of sh, bash, and other shells in the
    Linux/BSD/MacOS ecosystem.

    >>> print(args2sh(['aa', '[bb]', "cc'cc", 'dd"dd']))
    aa '[bb]' 'cc'"'"'cc' 'dd"dd'

    As you can see, arguments with no special characters are not
    escaped, arguments with special characters are quoted with single
    quotes, and single quotes themselves are quoted with double
    quotes. Double quotes are handled like any other special
    character.

    Based on code from the :mod:`pipes`/:mod:`shlex` modules. Also
    note that :mod:`shlex` and :mod:`argparse` have functions to split
    and parse strings escaped in this manner.
    """

def args2cmd(args: Iterable[str], sep: str = " ") -> str:
    """Return a shell-escaped string version of *args*, separated by
    *sep*, using the same rules as the Microsoft C runtime.

    >>> print(args2cmd(['aa', '[bb]', "cc'cc", 'dd"dd']))
    aa [bb] cc'cc dd\\"dd

    As you can see, escaping is through backslashing and not quoting,
    and double quotes are the only special character. See the comment
    in the code for more details. Based on internal code from the
    :mod:`subprocess` module.

    """

def parse_int_list(range_string: str, delim: str = ",", range_delim: str = "-") -> list[int]:
    """Returns a sorted list of positive integers based on
    *range_string*. Reverse of :func:`format_int_list`.

    Args:
        range_string (str): String of comma separated positive
            integers or ranges (e.g. '1,2,4-6,8'). Typical of a custom
            page range string used in printer dialogs.
        delim (char): Defaults to ','. Separates integers and
            contiguous ranges of integers.
        range_delim (char): Defaults to '-'. Indicates a contiguous
            range of integers.

    >>> parse_int_list('1,3,5-8,10-11,15')
    [1, 3, 5, 6, 7, 8, 10, 11, 15]

    """

def format_int_list(int_list: list[int], delim: str = ",", range_delim: str = "-", delim_space: bool = False) -> str:
    """Returns a sorted range string from a list of positive integers
    (*int_list*). Contiguous ranges of integers are collapsed to min
    and max values. Reverse of :func:`parse_int_list`.

    Args:
        int_list (list): List of positive integers to be converted
           into a range string (e.g. [1,2,4,5,6,8]).
        delim (char): Defaults to ','. Separates integers and
           contiguous ranges of integers.
        range_delim (char): Defaults to '-'. Indicates a contiguous
           range of integers.
        delim_space (bool): Defaults to ``False``. If ``True``, adds a
           space after all *delim* characters.

    >>> format_int_list([1,3,5,6,7,8,10,11,15])
    '1,3,5-8,10-11,15'

    """

def complement_int_list(
    range_string: str, range_start: int = 0, range_end: int | None = None, delim: str = ",", range_delim: str = "-"
) -> str:
    """Returns range string that is the complement of the one provided as
    *range_string* parameter.

    These range strings are of the kind produce by :func:`format_int_list`, and
    parseable by :func:`parse_int_list`.

    Args:
        range_string (str): String of comma separated positive integers or
           ranges (e.g. '1,2,4-6,8'). Typical of a custom page range string
           used in printer dialogs.
        range_start (int): A positive integer from which to start the resulting
           range. Value is inclusive. Defaults to ``0``.
        range_end (int): A positive integer from which the produced range is
           stopped. Value is exclusive. Defaults to the maximum value found in
           the provided ``range_string``.
        delim (char): Defaults to ','. Separates integers and contiguous ranges
           of integers.
        range_delim (char): Defaults to '-'. Indicates a contiguous range of
           integers.

    >>> complement_int_list('1,3,5-8,10-11,15')
    '0,2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_start=0)
    '0,2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_start=1)
    '2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_start=2)
    '2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_start=3)
    '4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=15)
    '0,2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=14)
    '0,2,4,9,12-13'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=13)
    '0,2,4,9,12'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=20)
    '0,2,4,9,12-14,16-19'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=0)
    ''

    >>> complement_int_list('1,3,5-8,10-11,15', range_start=-1)
    '0,2,4,9,12-14'

    >>> complement_int_list('1,3,5-8,10-11,15', range_end=-1)
    ''

    >>> complement_int_list('1,3,5-8', range_start=1, range_end=1)
    ''

    >>> complement_int_list('1,3,5-8', range_start=2, range_end=2)
    ''

    >>> complement_int_list('1,3,5-8', range_start=2, range_end=3)
    '2'

    >>> complement_int_list('1,3,5-8', range_start=-10, range_end=-5)
    ''

    >>> complement_int_list('1,3,5-8', range_start=20, range_end=10)
    ''

    >>> complement_int_list('')
    ''
    """

def int_ranges_from_int_list(range_string: str, delim: str = ",", range_delim: str = "-") -> tuple[int, int]:
    """Transform a string of ranges (*range_string*) into a tuple of tuples.

    Args:
        range_string (str): String of comma separated positive integers or
           ranges (e.g. '1,2,4-6,8'). Typical of a custom page range string
           used in printer dialogs.
        delim (char): Defaults to ','. Separates integers and contiguous ranges
           of integers.
        range_delim (char): Defaults to '-'. Indicates a contiguous range of
           integers.

    >>> int_ranges_from_int_list('1,3,5-8,10-11,15')
    ((1, 1), (3, 3), (5, 8), (10, 11), (15, 15))

    >>> int_ranges_from_int_list('1')
    ((1, 1),)

    >>> int_ranges_from_int_list('')
    ()
    """

class MultiReplace:
    """
    MultiReplace is a tool for doing multiple find/replace actions in one pass.

    Given a mapping of values to be replaced it allows for all of the matching
    values to be replaced in a single pass which can save a lot of performance
    on very large strings. In addition to simple replace, it also allows for
    replacing based on regular expressions.

    Keyword Arguments:

    :type regex: bool
    :param regex: Treat search keys as regular expressions [Default: False]
    :type flags: int
    :param flags: flags to pass to the regex engine during compile

    Dictionary Usage::

        from boltons import strutils
        s = strutils.MultiReplace({
            'foo': 'zoo',
            'cat': 'hat',
            'bat': 'kraken'
        })
        new = s.sub('The foo bar cat ate a bat')
        new == 'The zoo bar hat ate a kraken'

    Iterable Usage::

        from boltons import strutils
        s = strutils.MultiReplace([
            ('foo', 'zoo'),
            ('cat', 'hat'),
            ('bat', 'kraken)'
        ])
        new = s.sub('The foo bar cat ate a bat')
        new == 'The zoo bar hat ate a kraken'


    The constructor can be passed a dictionary or other mapping as well as
    an iterable of tuples. If given an iterable, the substitution will be run
    in the order the replacement values are specified in the iterable. This is
    also true if it is given an OrderedDict. If given a dictionary then the
    order will be non-deterministic::

        >>> 'foo bar baz'.replace('foo', 'baz').replace('baz', 'bar')
        'bar bar bar'
        >>> m = MultiReplace({'foo': 'baz', 'baz': 'bar'})
        >>> m.sub('foo bar baz')
        'baz bar bar'

    This is because the order of replacement can matter if you're inserting
    something that might be replaced by a later substitution. Pay attention and
    if you need to rely on order then consider using a list of tuples instead
    of a dictionary.
    """

    group_map: dict[str, str]
    combined_pattern: Pattern[str]
    def __init__(self, sub_map: dict[str, str], **kwargs) -> None:
        """Compile any regular expressions that have been passed."""

    def sub(self, text: str) -> str:
        """
        Run substitutions on the input text.

        Given an input string, run all substitutions given in the
        constructor.
        """

def multi_replace(text: str, sub_map: dict[str, str], **kwargs) -> str:
    """
    Shortcut function to invoke MultiReplace in a single call.

    Example Usage::

        from boltons.strutils import multi_replace
        new = multi_replace(
            'The foo bar cat ate a bat',
            {'foo': 'zoo', 'cat': 'hat', 'bat': 'kraken'}
        )
        new == 'The zoo bar hat ate a kraken'
    """

def unwrap_text(text: str, ending: str | None = "\n\n") -> str:
    """
    Unwrap text, the natural complement to :func:`textwrap.wrap`.

    >>> text = "Short \\n lines  \\nwrapped\\nsmall.\\n\\nAnother\\nparagraph."
    >>> unwrap_text(text)
    'Short lines wrapped small.\\n\\nAnother paragraph.'

    Args:
       text: A string to unwrap.
       ending (str): The string to join all unwrapped paragraphs
          by. Pass ``None`` to get the list. Defaults to '\\n\\n' for
          compatibility with Markdown and RST.

    """

def removeprefix(text: str, prefix: str) -> str:
    """
    Remove `prefix` from start of `text` if present.

    Backport of `str.removeprefix` for Python versions less than 3.9.

    Args:
        text: A string to remove the prefix from.
        prefix: The string to remove from the beginning of `text`.
    """

__all__ = [
    "camel2under",
    "under2camel",
    "slugify",
    "split_punct_ws",
    "unit_len",
    "ordinalize",
    "cardinalize",
    "pluralize",
    "singularize",
    "asciify",
    "is_ascii",
    "is_uuid",
    "html2text",
    "strip_ansi",
    "bytes2human",
    "find_hashtags",
    "a10n",
    "gzip_bytes",
    "gunzip_bytes",
    "iter_splitlines",
    "indent",
    "escape_shell_args",
    "args2cmd",
    "args2sh",
    "parse_int_list",
    "format_int_list",
    "complement_int_list",
    "int_ranges_from_int_list",
    "MultiReplace",
    "multi_replace",
    "unwrap_text",
    "removeprefix",
]
