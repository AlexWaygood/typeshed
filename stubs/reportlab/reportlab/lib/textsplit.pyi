"""Helpers for text wrapping, hyphenation, Asian text splitting and kinsoku shori.

How to split a 'big word' depends on the language and the writing system.  This module
works on a Unicode string.  It ought to grow by allowing ore algoriths to be plugged
in based on possible knowledge of the language and desirable 'niceness' of the algorithm.

"""

from _typeshed import Incomplete
from collections.abc import Sequence
from typing import Final

__version__: Final[str]
CANNOT_START_LINE: Final[Sequence[str]]
ALL_CANNOT_START: Final[str]
CANNOT_END_LINE: Final[Sequence[str]]
ALL_CANNOT_END: Final[str]

def is_multi_byte(ch):
    """Is this an Asian character?"""

def getCharWidths(word, fontName, fontSize):
    """Returns a list of glyph widths.

    >>> getCharWidths('Hello', 'Courier', 10)
    [6.0, 6.0, 6.0, 6.0, 6.0]
    >>> from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    >>> from reportlab.pdfbase.pdfmetrics import registerFont
    >>> registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    >>> getCharWidths(u'東京', 'HeiseiMin-W3', 10)   #most kanji are 100 ems
    [10.0, 10.0]
    """

def wordSplit(word, maxWidths, fontName, fontSize, encoding: str = "utf8"):
    """Attempts to break a word which lacks spaces into two parts, the first of which
    fits in the remaining space.  It is allowed to add hyphens or whatever it wishes.

    This is intended as a wrapper for some language- and user-choice-specific splitting
    algorithms.  It should only be called after line breaking on spaces, which covers western
    languages and is highly optimised already.  It works on the 'last unsplit word'.

    Presumably with further study one could write a Unicode splitting algorithm for text
    fragments whick was much faster.

    Courier characters should be 6 points wide.
    >>> wordSplit('HelloWorld', 30, 'Courier', 10)
    [[0.0, 'Hello'], [0.0, 'World']]
    >>> wordSplit('HelloWorld', 31, 'Courier', 10)
    [[1.0, 'Hello'], [1.0, 'World']]
    """

def dumbSplit(word, widths, maxWidths):
    """This function attempts to fit as many characters as possible into the available
    space, cutting "like a knife" between characters.  This would do for Chinese.
    It returns a list of (text, extraSpace) items where text is a Unicode string,
    and extraSpace is the points of unused space available on the line.  This is a
    structure which is fairly easy to display, and supports 'backtracking' approaches
    after the fact.

    Test cases assume each character is ten points wide...

    >>> dumbSplit(u'Hello', [10]*5, 60)
    [[10, u'Hello']]
    >>> dumbSplit(u'Hello', [10]*5, 50)
    [[0, u'Hello']]
    >>> dumbSplit(u'Hello', [10]*5, 40)
    [[0, u'Hell'], [30, u'o']]
    """

def kinsokuShoriSplit(word, widths, availWidth) -> None:
    """Split according to Japanese rules according to CJKV (Lunde).

    Essentially look for "nice splits" so that we don't end a line
    with an open bracket, or start one with a full stop, or stuff like
    that.  There is no attempt to try to split compound words into
    constituent kanji.  It currently uses wrap-down: packs as much
    on a line as possible, then backtracks if needed

    This returns a number of words each of which should just about fit
    on a line.  If you give it a whole paragraph at once, it will
    do all the splits.

    It's possible we might slightly step over the width limit
    if we do hanging punctuation marks in future (e.g. dangle a Japanese
    full stop in the right margin rather than using a whole character
    box.

    """

rx: Incomplete

def cjkwrap(text, width, encoding: str = "utf8"): ...
