"""
pygments.formatters.latex
~~~~~~~~~~~~~~~~~~~~~~~~~

Formatter for LaTeX fancyvrb output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter
from pygments.lexer import Lexer

_T = TypeVar("_T", str, bytes)

class LatexFormatter(Formatter[_T]):
    """
    Format tokens as LaTeX code. This needs the `fancyvrb` and `color`
    standard packages.

    Without the `full` option, code is formatted as one ``Verbatim``
    environment, like this:

    .. sourcecode:: latex

        \\begin{Verbatim}[commandchars=\\\\\\{\\}]
        \\PY{k}{def }\\PY{n+nf}{foo}(\\PY{n}{bar}):
            \\PY{k}{pass}
        \\end{Verbatim}

    Wrapping can be disabled using the `nowrap` option.

    The special command used here (``\\PY``) and all the other macros it needs
    are output by the `get_style_defs` method.

    With the `full` option, a complete LaTeX document is output, including
    the command definitions in the preamble.

    The `get_style_defs()` method of a `LatexFormatter` returns a string
    containing ``\\def`` commands defining the macros needed inside the
    ``Verbatim`` environments.

    Additional options accepted:

    `nowrap`
        If set to ``True``, don't wrap the tokens at all, not even inside a
        ``\\begin{Verbatim}`` environment. This disables most other options
        (default: ``False``).

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `full`
        Tells the formatter to output a "full" document, i.e. a complete
        self-contained document (default: ``False``).

    `title`
        If `full` is true, the title that should be used to caption the
        document (default: ``''``).

    `docclass`
        If the `full` option is enabled, this is the document class to use
        (default: ``'article'``).

    `preamble`
        If the `full` option is enabled, this can be further preamble commands,
        e.g. ``\\usepackage`` (default: ``''``).

    `linenos`
        If set to ``True``, output line numbers (default: ``False``).

    `linenostart`
        The line number for the first line (default: ``1``).

    `linenostep`
        If set to a number n > 1, only every nth line number is printed.

    `verboptions`
        Additional options given to the Verbatim environment (see the *fancyvrb*
        docs for possible values) (default: ``''``).

    `commandprefix`
        The LaTeX commands used to produce colored output are constructed
        using this prefix and some letters (default: ``'PY'``).

        .. versionadded:: 0.7
        .. versionchanged:: 0.10
           The default is now ``'PY'`` instead of ``'C'``.

    `texcomments`
        If set to ``True``, enables LaTeX comment lines.  That is, LaTex markup
        in comment tokens is not escaped so that LaTeX can render it (default:
        ``False``).

        .. versionadded:: 1.2

    `mathescape`
        If set to ``True``, enables LaTeX math mode escape in comments. That
        is, ``'$...$'`` inside a comment will trigger math mode (default:
        ``False``).

        .. versionadded:: 1.2

    `escapeinside`
        If set to a string of length 2, enables escaping to LaTeX. Text
        delimited by these 2 characters is read as LaTeX code and
        typeset accordingly. It has no effect in string literals. It has
        no effect in comments if `texcomments` or `mathescape` is
        set. (default: ``''``).

        .. versionadded:: 2.0

    `envname`
        Allows you to pick an alternative environment name replacing Verbatim.
        The alternate environment still has to support Verbatim's option syntax.
        (default: ``'Verbatim'``).

        .. versionadded:: 2.0
    """

    name: str
    aliases: Any
    filenames: Any
    docclass: Any
    preamble: Any
    linenos: Any
    linenostart: Any
    linenostep: Any
    verboptions: Any
    nobackground: Any
    commandprefix: Any
    texcomments: Any
    mathescape: Any
    escapeinside: Any
    left: Any
    right: Any
    envname: Any
    def get_style_defs(self, arg: str = ""):
        """
        Return the command sequences needed to define the commands
        used to format text in the verbatim environment. ``arg`` is ignored.
        """

    def format_unencoded(self, tokensource, outfile) -> None: ...

class LatexEmbeddedLexer(Lexer):
    """
    This lexer takes one lexer as argument, the lexer for the language
    being formatted, and the left and right delimiters for escaped text.

    First everything is scanned using the language lexer to obtain
    strings and comments. All other consecutive tokens are merged and
    the resulting text is scanned for escaped segments, which are given
    the Token.Escape type. Finally text that is not escaped is scanned
    again with the language lexer.
    """

    left: Any
    right: Any
    lang: Any
    def __init__(self, left, right, lang, **options) -> None: ...
    def get_tokens_unprocessed(self, text): ...
