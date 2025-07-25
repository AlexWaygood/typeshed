"""
The block parser handles basic parsing of Markdown blocks.  It doesn't concern
itself with inline elements such as `**bold**` or `*italics*`, but rather just
catches blocks, lists, quotes, etc.

The `BlockParser` is made up of a bunch of `BlockProcessors`, each handling a
different type of block. Extensions may add/replace/remove `BlockProcessors`
as they need to alter how Markdown blocks are parsed.
"""

from collections.abc import Iterable
from typing import Any, TypeVar
from xml.etree.ElementTree import Element, ElementTree

from markdown import blockprocessors, util
from markdown.core import Markdown

_T = TypeVar("_T")

class State(list[_T]):
    """Track the current and nested state of the parser.

    This utility class is used to track the state of the `BlockParser` and
    support multiple levels if nesting. It's just a simple API wrapped around
    a list. Each time a state is set, that state is appended to the end of the
    list. Each time a state is reset, that state is removed from the end of
    the list.

    Therefore, each time a state is set for a nested block, that state must be
    reset when we back out of that level of nesting or the state could be
    corrupted.

    While all the methods of a list object are available, only the three
    defined below need be used.

    """

    def set(self, state: _T) -> None:
        """Set a new state."""

    def reset(self) -> None:
        """Step back one step in nested state."""

    def isstate(self, state: _T) -> bool:
        """Test that top (current) level is of given state."""

class BlockParser:
    """Parse Markdown blocks into an `ElementTree` object.

    A wrapper class that stitches the various `BlockProcessors` together,
    looping through them and creating an `ElementTree` object.

    """

    blockprocessors: util.Registry[blockprocessors.BlockProcessor]
    state: State[Any]  # TODO: possible to get rid of Any?
    md: Markdown
    def __init__(self, md: Markdown) -> None:
        """Initialize the block parser.

        Arguments:
            md: A Markdown instance.

        Attributes:
            BlockParser.md (Markdown): A Markdown instance.
            BlockParser.state (State): Tracks the nesting level of current location in document being parsed.
            BlockParser.blockprocessors (util.Registry): A collection of
                [`blockprocessors`][markdown.blockprocessors].

        """
    root: Element
    def parseDocument(self, lines: Iterable[str]) -> ElementTree:
        """Parse a Markdown document into an `ElementTree`.

        Given a list of lines, an `ElementTree` object (not just a parent
        `Element`) is created and the root element is passed to the parser
        as the parent. The `ElementTree` object is returned.

        This should only be called on an entire document, not pieces.

        Arguments:
            lines: A list of lines (strings).

        Returns:
            An element tree.
        """

    def parseChunk(self, parent: Element, text: str) -> None:
        """Parse a chunk of Markdown text and attach to given `etree` node.

        While the `text` argument is generally assumed to contain multiple
        blocks which will be split on blank lines, it could contain only one
        block. Generally, this method would be called by extensions when
        block parsing is required.

        The `parent` `etree` Element passed in is altered in place.
        Nothing is returned.

        Arguments:
            parent: The parent element.
            text: The text to parse.

        """

    def parseBlocks(self, parent: Element, blocks: list[str]) -> None:
        """Process blocks of Markdown text and attach to given `etree` node.

        Given a list of `blocks`, each `blockprocessor` is stepped through
        until there are no blocks left. While an extension could potentially
        call this method directly, it's generally expected to be used
        internally.

        This is a public method as an extension may need to add/alter
        additional `BlockProcessors` which call this method to recursively
        parse a nested block.

        Arguments:
            parent: The parent element.
            blocks: The blocks of text to parse.

        """
