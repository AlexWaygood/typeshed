"""
Pygments
~~~~~~~~

Pygments is a syntax highlighting package written in Python.

It is a generic syntax highlighter for general use in all kinds of software
such as forum systems, wikis or other applications that need to prettify
source code. Highlights are:

* a wide range of common languages and markup formats is supported
* special attention is paid to details, increasing quality by a fair amount
* support for new languages and formats are added easily
* a number of output formats, presently HTML, LaTeX, RTF, SVG, all image
  formats that PIL supports, and ANSI sequences
* it is usable as a command-line tool and as a library
* ... and it highlights even Brainfuck!

The `Pygments master branch`_ is installable with ``easy_install Pygments==dev``.

.. _Pygments master branch:
   https://github.com/pygments/pygments/archive/master.zip#egg=Pygments-dev

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import SupportsWrite
from collections.abc import Iterator
from typing import TypeVar, overload

from pygments.formatter import Formatter
from pygments.lexer import Lexer
from pygments.token import _TokenType

_T = TypeVar("_T", str, bytes)

__version__: str
__all__ = ["lex", "format", "highlight"]

def lex(code: str, lexer: Lexer) -> Iterator[tuple[_TokenType, str]]:
    """
    Lex `code` with the `lexer` (must be a `Lexer` instance)
    and return an iterable of tokens. Currently, this only calls
    `lexer.get_tokens()`.
    """

@overload
def format(tokens, formatter: Formatter[_T], outfile: SupportsWrite[_T]) -> None:
    """
    Format ``tokens`` (an iterable of tokens) with the formatter ``formatter``
    (a `Formatter` instance).

    If ``outfile`` is given and a valid file object (an object with a
    ``write`` method), the result will be written to it, otherwise it
    is returned as a string.
    """

@overload
def format(tokens, formatter: Formatter[_T], outfile: None = None) -> _T: ...
@overload
def highlight(code, lexer, formatter: Formatter[_T], outfile: SupportsWrite[_T]) -> None:
    """
    This is the most high-level highlighting function. It combines `lex` and
    `format` in one function.
    """

@overload
def highlight(code, lexer, formatter: Formatter[_T], outfile: None = None) -> _T: ...
