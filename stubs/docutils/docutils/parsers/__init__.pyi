"""
This package contains Docutils parser modules.
"""

from typing import ClassVar, Final

from docutils import Component
from docutils.nodes import _Document

__docformat__: Final = "reStructuredText"

class Parser(Component):
    component_type: ClassVar[str]
    config_section: ClassVar[str]
    inputstring: str  # defined after call to setup_parse()
    document: _Document  # defined after call to setup_parse()
    def parse(self, inputstring: str, document: _Document) -> None:
        """Override to parse `inputstring` into document tree `document`."""

    def setup_parse(self, inputstring: str, document: _Document) -> None:
        """Initial parse setup.  Call at start of `self.parse()`."""

    def finish_parse(self) -> None:
        """Finalize parse details.  Call at end of `self.parse()`."""

_parser_aliases: dict[str, str]

def get_parser_class(parser_name: str) -> type[Parser]:
    """Return the Parser class from the `parser_name` module."""
