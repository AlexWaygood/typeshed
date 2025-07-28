"""
Adds rST-style admonitions to Python-Markdown.
Inspired by [rST][] feature with the same name.

[rST]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions

See the [documentation](https://Python-Markdown.github.io/extensions/admonition)
for details.
"""

from re import Match, Pattern
from typing import ClassVar
from xml.etree.ElementTree import Element

from markdown import blockparser
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension

class AdmonitionExtension(Extension):
    """Admonition extension for Python-Markdown."""

class AdmonitionProcessor(BlockProcessor):
    CLASSNAME: str
    CLASSNAME_TITLE: str
    RE: ClassVar[Pattern[str]]
    RE_SPACES: ClassVar[Pattern[str]]
    current_sibling: Element | None
    content_indent: int
    def __init__(self, parser: blockparser.BlockParser) -> None:
        """Initialization."""

    def parse_content(self, parent: Element, block: str) -> tuple[Element | None, str, str]:
        """Get sibling admonition.

        Retrieve the appropriate sibling element. This can get tricky when
        dealing with lists.

        """

    def get_class_and_title(self, match: Match[str]) -> tuple[str, str | None]: ...

def makeExtension(**kwargs) -> AdmonitionExtension: ...
