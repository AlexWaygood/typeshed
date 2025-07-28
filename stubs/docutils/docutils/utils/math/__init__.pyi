"""
This is the Docutils (Python Documentation Utilities) "math" sub-package.

It contains various modules for conversion between different math formats
(LaTeX, MathML, HTML).

:math2html:    LaTeX math -> HTML conversion from eLyXer
:latex2mathml: LaTeX math -> presentational MathML
:unichar2tex:  Unicode character to LaTeX math translation table
:tex2unichar:  LaTeX math to Unicode character translation dictionaries
:mathalphabet2unichar:  LaTeX math alphabets to Unicode character translation
:tex2mathml_extern: Wrapper for 3rd party TeX -> MathML converters
"""

from typing import Literal

from docutils.nodes import Node

class MathError(ValueError):
    """Exception for math syntax and math conversion errors.

    The additional attribute `details` may hold a list of Docutils
    nodes suitable as children for a ``<system_message>``.
    """

    details: list[Node]
    def __init__(self, msg: object, details: list[Node] = []) -> None: ...

def toplevel_code(code: str) -> str:
    """Return string (LaTeX math) `code` with environments stripped out."""

def pick_math_environment(code: str, numbered: bool = False) -> Literal["align*", "equation*", "align", "equation"]:
    """Return the right math environment to display `code`.

    The test simply looks for line-breaks (``\\``) outside environments.
    Multi-line formulae are set with ``align``, one-liners with
    ``equation``.

    If `numbered` evaluates to ``False``, the "starred" versions are used
    to suppress numbering.
    """

def wrap_math_code(code: str, as_block: bool | None) -> str: ...
