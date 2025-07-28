"""
Adds footnote handling to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/footnotes)
for details.
"""

from collections import OrderedDict
from re import Pattern
from typing import ClassVar
from xml.etree.ElementTree import Element

from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor
from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor

FN_BACKLINK_TEXT: str
NBSP_PLACEHOLDER: str
RE_REF_ID: Pattern[str]

class FootnoteExtension(Extension):
    """Footnote Extension."""

    unique_prefix: int
    found_refs: dict[str, int]
    used_refs: set[str]
    def __init__(self, **kwargs) -> None:
        """Setup configs."""
    parser: BlockParser
    md: Markdown
    footnotes: OrderedDict[str, str]
    def reset(self) -> None:
        """Clear footnotes on reset, and prepare for distinct document."""

    def unique_ref(self, reference: str, found: bool = False) -> str:
        """Get a unique reference if there are duplicates."""

    def findFootnotesPlaceholder(self, root: Element) -> tuple[Element, Element, bool] | None:
        """Return ElementTree Element that contains Footnote placeholder."""

    def setFootnote(self, id: str, text: str) -> None:
        """Store a footnote for later retrieval."""

    def get_separator(self) -> str:
        """Get the footnote separator."""

    def makeFootnoteId(self, id: str) -> str:
        """Return footnote link id."""

    def makeFootnoteRefId(self, id: str, found: bool = False) -> str:
        """Return footnote back-link id."""

    def makeFootnotesDiv(self, root: Element) -> Element | None:
        """Return `div` of footnotes as `etree` Element."""

class FootnoteBlockProcessor(BlockProcessor):
    """Find all footnote references and store for later use."""

    RE: ClassVar[Pattern[str]]
    footnotes: FootnoteExtension
    def __init__(self, footnotes: FootnoteExtension) -> None: ...
    def detectTabbed(self, blocks: list[str]) -> list[str]:
        """Find indented text and remove indent before further processing.

        Returns:
            A list of blocks with indentation removed.
        """

    def detab(self, block: str) -> str:  # type: ignore[override]
        """Remove one level of indent from a block.

        Preserve lazily indented blocks by only removing indent from indented lines.
        """

class FootnoteInlineProcessor(InlineProcessor):
    """`InlineProcessor` for footnote markers in a document's body text."""

    footnotes: FootnoteExtension
    def __init__(self, pattern: str, footnotes: FootnoteExtension) -> None: ...

class FootnotePostTreeprocessor(Treeprocessor):
    """Amend footnote div with duplicates."""

    footnotes: FootnoteExtension
    def __init__(self, footnotes: FootnoteExtension) -> None: ...
    def add_duplicates(self, li: Element, duplicates: int) -> None:
        """Adjust current `li` and add the duplicates: `fnref2`, `fnref3`, etc."""

    def get_num_duplicates(self, li: Element) -> int:
        """Get the number of duplicate refs of the footnote."""

    def handle_duplicates(self, parent: Element) -> None:
        """Find duplicate footnotes and format and add the duplicates."""
    offset: int

class FootnoteTreeprocessor(Treeprocessor):
    """Build and append footnote div to end of document."""

    footnotes: FootnoteExtension
    def __init__(self, footnotes: FootnoteExtension) -> None: ...

class FootnotePostprocessor(Postprocessor):
    """Replace placeholders with html entities."""

    footnotes: FootnoteExtension
    def __init__(self, footnotes: FootnoteExtension) -> None: ...

def makeExtension(**kwargs) -> FootnoteExtension:
    """Return an instance of the `FootnoteExtension`"""
