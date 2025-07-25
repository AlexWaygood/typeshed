"""
Directives for references and targets.
"""

from typing import Final

from docutils.parsers.rst import Directive

__docformat__: Final = "reStructuredText"

class TargetNotes(Directive):
    """Target footnote generation."""
