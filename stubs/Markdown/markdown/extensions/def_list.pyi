"""
Adds parsing of Definition Lists to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/definition_lists)
for details.
"""

from re import Pattern

from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
from markdown.extensions import Extension

class DefListProcessor(BlockProcessor):
    """Process Definition Lists."""

    RE: Pattern[str]
    NO_INDENT_RE: Pattern[str]

class DefListIndentProcessor(ListIndentProcessor):
    """Process indented children of definition list items."""

class DefListExtension(Extension):
    """Add definition lists to Markdown."""

def makeExtension(**kwargs) -> DefListExtension: ...
