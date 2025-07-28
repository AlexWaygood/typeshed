"""
Directives for document parts.
"""

from collections.abc import Sequence
from typing import Final

from docutils.parsers.rst import Directive

__docformat__: Final = "reStructuredText"

class Contents(Directive):
    """
    Table of contents.

    The table of contents is generated in two passes: initial parse and
    transform.  During the initial parse, a 'pending' element is generated
    which acts as a placeholder, storing the TOC title and any options
    internally.  At a later stage in the processing, the 'pending' element is
    replaced by a 'topic' element, a title and the table of contents proper.
    """

    backlinks_values: Sequence[str]
    def backlinks(arg): ...

class Sectnum(Directive):
    """Automatic section numbering."""

class Header(Directive):
    """Contents of document header."""

class Footer(Directive):
    """Contents of document footer."""
