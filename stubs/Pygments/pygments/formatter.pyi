"""
pygments.formatter
~~~~~~~~~~~~~~~~~~

Base formatter class.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, Generic, TypeVar, overload

_T = TypeVar("_T", str, bytes)

class Formatter(Generic[_T]):
    """
    Converts a token stream to text.

    Formatters should have attributes to help selecting them. These
    are similar to the corresponding :class:`~pygments.lexer.Lexer`
    attributes.

    .. autoattribute:: name
       :no-value:

    .. autoattribute:: aliases
       :no-value:

    .. autoattribute:: filenames
       :no-value:

    You can pass options as keyword arguments to the constructor.
    All formatters accept these basic options:

    ``style``
        The style to use, can be a string or a Style subclass
        (default: "default"). Not used by e.g. the
        TerminalFormatter.
    ``full``
        Tells the formatter to output a "full" document, i.e.
        a complete self-contained document. This doesn't have
        any effect for some formatters (default: false).
    ``title``
        If ``full`` is true, the title that should be used to
        caption the document (default: '').
    ``encoding``
        If given, must be an encoding name. This will be used to
        convert the Unicode token strings to byte strings in the
        output. If it is "" or None, Unicode strings will be written
        to the output file, which most file-like objects do not
        support (default: None).
    ``outencoding``
        Overrides ``encoding`` if given.

    """

    name: Any
    aliases: Any
    filenames: Any
    unicodeoutput: bool
    style: Any
    full: Any
    title: Any
    encoding: Any
    options: Any
    @overload
    def __init__(self: Formatter[str], *, encoding: None = None, outencoding: None = None, **options) -> None:
        """
        As with lexers, this constructor takes arbitrary optional arguments,
        and if you override it, you should first process your own options, then
        call the base class implementation.
        """

    @overload
    def __init__(self: Formatter[bytes], *, encoding: str, outencoding: None = None, **options) -> None: ...
    @overload
    def __init__(self: Formatter[bytes], *, encoding: None = None, outencoding: str, **options) -> None: ...
    def get_style_defs(self, arg: str = ""):
        """
        This method must return statements or declarations suitable to define
        the current style for subsequent highlighted text (e.g. CSS classes
        in the `HTMLFormatter`).

        The optional argument `arg` can be used to modify the generation and
        is formatter dependent (it is standardized because it can be given on
        the command line).

        This method is called by the ``-S`` :doc:`command-line option <cmdline>`,
        the `arg` is then given by the ``-a`` option.
        """

    def format(self, tokensource, outfile):
        """
        This method must format the tokens from the `tokensource` iterable and
        write the formatted version to the file object `outfile`.

        Formatter options can control how exactly the tokens are converted.
        """
