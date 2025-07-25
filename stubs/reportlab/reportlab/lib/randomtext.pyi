"""Like Lorem Ipsum, but more fun and extensible.

This module exposes a function randomText() which generates paragraphs.
These can be used when testing out document templates and stylesheets.
A number of 'themes' are provided - please contribute more!
We need some real Greek text too.

There are currently six themes provided:
    STARTUP (words suitable for a business plan - or not as the case may be),
    COMPUTERS (names of programming languages and operating systems etc),
    BLAH (variations on the word 'blah'),
    BUZZWORD (buzzword bingo),
    STARTREK (Star Trek),
    PRINTING (print-related terms)
    PYTHON (snippets and quotes from Monty Python)
    CHOMSKY (random lingusitic nonsense)

EXAMPLE USAGE:
    from reportlab.lib import randomtext
    print randomtext.randomText(randomtext.PYTHON, 10)

    This prints a random number of random sentences (up to a limit
    of ten) using the theme 'PYTHON'.

"""

from collections.abc import Sequence
from typing import Final

__version__: Final[str]
STARTUP: Final[Sequence[str]]
COMPUTERS: Final[Sequence[str]]
BLAH: Final[Sequence[str]]
BUZZWORD: Final[Sequence[str]]
STARTREK: Final[Sequence[str]]
PRINTING: Final[Sequence[str]]
PYTHON: Final[Sequence[str]]
leadins: Final[Sequence[str]]
subjects: Final[Sequence[str]]
verbs: Final[Sequence[str]]
objects: Final[Sequence[str]]

def format_wisdom(text: str, line_length: int = 72) -> str: ...
def chomsky(times: int = 1) -> str: ...
def randomText(theme: str | Sequence[str] = ..., sentences: int = 5) -> str: ...
