"""
Adds parsing of tables to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/tables)
for details.
"""

from re import Pattern
from typing import Any, ClassVar

from markdown import blockparser
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

PIPE_NONE: int
PIPE_LEFT: int
PIPE_RIGHT: int

class TableProcessor(BlockProcessor):
    """Process Tables."""

    RE_CODE_PIPES: ClassVar[Pattern[str]]
    RE_END_BORDER: ClassVar[Pattern[str]]
    border: bool
    separator: str
    def __init__(self, parser: blockparser.BlockParser, config: dict[str, Any]) -> None: ...

class TableExtension(Extension):
    """Add tables to Markdown."""

    def __init__(self, **kwargs) -> None: ...

def makeExtension(**kwargs) -> TableExtension: ...
