"""Wrappers for TeX->MathML conversion by external tools

This module is provisional:
the API is not settled and may change with any minor Docutils version.
"""

from typing import Final

document_template: Final[str]

def blahtexml(math_code: str, as_block: bool = False) -> str:
    """Convert LaTeX math code to MathML with blahtexml__.

    __ http://gva.noekeon.org/blahtexml/
    """

def latexml(math_code: str, as_block: bool = False) -> str:
    """Convert LaTeX math code to MathML with LaTeXML__.

    Comprehensive macro support but **very** slow.

    __ http://dlmf.nist.gov/LaTeXML/
    """

def pandoc(math_code: str, as_block: bool = False) -> str:
    """Convert LaTeX math code to MathML with pandoc__.

    __ https://pandoc.org/
    """

def ttm(math_code: str, as_block: bool = False) -> str:
    """Convert LaTeX math code to MathML with TtM__.

    Aged, limited, but fast.

    __ http://silas.psfc.mit.edu/tth/mml/
    """
