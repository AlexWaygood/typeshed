"""
XeLaTeX document tree Writer.

A variant of Docutils' standard 'latex2e' writer producing LaTeX output
suited for processing with the Unicode-aware TeX engines
LuaTeX and XeTeX.
"""

from typing import ClassVar, Final

from docutils import nodes
from docutils.utils import Reporter
from docutils.writers import latex2e

__docformat__: Final = "reStructuredText"

class Writer(latex2e.Writer):
    """A writer for Unicode-aware LaTeX variants (XeTeX, LuaTeX)"""

    default_template: ClassVar[str]
    default_preamble: ClassVar[str]
    config_section: ClassVar[str]
    config_section_dependencies: ClassVar[tuple[str, ...]]
    translator_class: type[XeLaTeXTranslator]

class Babel(latex2e.Babel):
    """Language specifics for XeTeX.

    Use `polyglossia` instead of `babel` and adapt settings.
    """

    language_code: str
    reporter: Reporter
    language: str
    warn_msg: str  # type: ignore[misc]
    quote_index: int
    quotes: tuple[str, ...]
    literal_double_quote: str
    key: str
    def __init__(self, language_code: str, reporter: Reporter) -> None: ...

class XeLaTeXTranslator(latex2e.LaTeXTranslator):
    """
    Generate code for LaTeX using Unicode fonts (XeLaTex or LuaLaTeX).

    See the docstring of docutils.writers._html_base.HTMLTranslator for
    notes on and examples of safe subclassing.
    """

    is_xetex: bool  # type: ignore[misc]
    def __init__(self, document: nodes.document) -> None: ...
