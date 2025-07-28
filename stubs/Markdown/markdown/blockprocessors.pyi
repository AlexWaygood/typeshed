"""
A block processor parses blocks of text and adds new elements to the ElementTree. Blocks of text,
separated from other text by blank lines, may have a different syntax and produce a differently
structured tree than other Markdown. Block processors excel at handling code formatting, equation
layouts, tables, etc.
"""

from logging import Logger
from re import Match, Pattern
from typing import Any, ClassVar
from xml.etree.ElementTree import Element

from markdown.blockparser import BlockParser
from markdown.core import Markdown

logger: Logger

def build_block_parser(md: Markdown, **kwargs: Any) -> BlockParser:
    """Build the default block parser used by Markdown."""

class BlockProcessor:
    """Base class for block processors.

    Each subclass will provide the methods below to work with the source and
    tree. Each processor will need to define it's own `test` and `run`
    methods. The `test` method should return True or False, to indicate
    whether the current block should be processed by this processor. If the
    test passes, the parser will call the processors `run` method.

    Attributes:
        BlockProcessor.parser (BlockParser): The `BlockParser` instance this is attached to.
        BlockProcessor.tab_length (int): The tab length set on the `Markdown` instance.

    """

    parser: BlockParser
    tab_length: int
    def __init__(self, parser: BlockParser) -> None: ...
    def lastChild(self, parent: Element) -> Element | None:
        """Return the last child of an `etree` element."""

    def detab(self, text: str, length: int | None = None) -> tuple[str, str]:
        """Remove a tab from the front of each line of the given text."""

    def looseDetab(self, text: str, level: int = 1) -> str:
        """Remove a tab from front of lines but allowing dedented lines."""

    def test(self, parent: Element, block: str) -> bool:
        """Test for block type. Must be overridden by subclasses.

        As the parser loops through processors, it will call the `test`
        method on each to determine if the given block of text is of that
        type. This method must return a boolean `True` or `False`. The
        actual method of testing is left to the needs of that particular
        block type. It could be as simple as `block.startswith(some_string)`
        or a complex regular expression. As the block type may be different
        depending on the parent of the block (i.e. inside a list), the parent
        `etree` element is also provided and may be used as part of the test.

        Keyword arguments:
            parent: An `etree` element which will be the parent of the block.
            block: A block of text from the source which has been split at blank lines.
        """

    def run(self, parent: Element, blocks: list[str]) -> bool | None:
        """Run processor. Must be overridden by subclasses.

        When the parser determines the appropriate type of a block, the parser
        will call the corresponding processor's `run` method. This method
        should parse the individual lines of the block and append them to
        the `etree`.

        Note that both the `parent` and `etree` keywords are pointers
        to instances of the objects which should be edited in place. Each
        processor must make changes to the existing objects as there is no
        mechanism to return new/different objects to replace them.

        This means that this method should be adding `SubElements` or adding text
        to the parent, and should remove (`pop`) or add (`insert`) items to
        the list of blocks.

        If `False` is returned, this will have the same effect as returning `False`
        from the `test` method.

        Keyword arguments:
            parent: An `etree` element which is the parent of the current block.
            blocks: A list of all remaining blocks of the document.
        """

class ListIndentProcessor(BlockProcessor):
    """Process children of list items.

    Example

        * a list item
            process this part

            or this part

    """

    ITEM_TYPES: list[str]
    LIST_TYPES: list[str]
    INDENT_RE: Pattern[str]
    def __init__(self, parser: BlockParser) -> None: ...  # Note: This was done because the args are sent as-is.
    def create_item(self, parent: Element, block: str) -> None:
        """Create a new `li` and parse the block with it as the parent."""

    def get_level(self, parent: Element, block: str) -> tuple[int, Element]:
        """Get level of indentation based on list level."""

class CodeBlockProcessor(BlockProcessor):
    """Process code blocks."""

class BlockQuoteProcessor(BlockProcessor):
    """Process blockquotes."""

    RE: Pattern[str]
    def clean(self, line: str) -> str:
        """Remove `>` from beginning of a line."""

class OListProcessor(BlockProcessor):
    """Process ordered list blocks."""

    TAG: ClassVar[str]
    STARTSWITH: ClassVar[str]
    LAZY_OL: ClassVar[bool]
    SIBLING_TAGS: ClassVar[list[str]]
    RE: Pattern[str]
    CHILD_RE: Pattern[str]
    INDENT_RE: Pattern[str]
    def __init__(self, parser: BlockParser) -> None: ...
    def get_items(self, block: str) -> list[str]:
        """Break a block into list items."""

class UListProcessor(OListProcessor):
    """Process unordered list blocks."""

    def __init__(self, parser: BlockParser) -> None: ...

class HashHeaderProcessor(BlockProcessor):
    """Process Hash Headers."""

    RE: ClassVar[Pattern[str]]

class SetextHeaderProcessor(BlockProcessor):
    """Process Setext-style Headers."""

    RE: ClassVar[Pattern[str]]

class HRProcessor(BlockProcessor):
    """Process Horizontal Rules."""

    RE: ClassVar[str]
    SEARCH_RE: ClassVar[Pattern[str]]
    match: Match[str]

class EmptyBlockProcessor(BlockProcessor):
    """Process blocks that are empty or start with an empty line."""

class ReferenceProcessor(BlockProcessor):
    """Process link references."""

    RE: ClassVar[Pattern[str]]

class ParagraphProcessor(BlockProcessor):
    """Process Paragraph blocks."""
