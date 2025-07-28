"""

Additional support for Pygments formatter.

"""

from _typeshed import Incomplete
from typing import Any

# Formatter[str] from types-pygments
class _Formatter:
    name: Any
    aliases: Any
    filenames: Any
    unicodeoutput: bool
    style: Any
    full: Any
    title: Any
    encoding: Any
    options: Any
    def __init__(self, *, encoding: None = None, outencoding: None = None, **options) -> None: ...
    def get_style_defs(self, arg: str = ""): ...
    def format(self, tokensource, outfile): ...

class OdtPygmentsFormatter(_Formatter):
    rststyle_function: Incomplete
    escape_function: Incomplete
    def __init__(self, rststyle_function, escape_function) -> None: ...
    def rststyle(self, name, parameters=()): ...
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

class OdtPygmentsProgFormatter(OdtPygmentsFormatter):
    def format(self, tokensource, outfile) -> None: ...

class OdtPygmentsLaTeXFormatter(OdtPygmentsFormatter):
    def format(self, tokensource, outfile) -> None: ...
