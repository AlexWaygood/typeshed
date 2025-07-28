"""
Tree processors manipulate the tree created by block processors. They can even create an entirely
new `ElementTree` object. This is an excellent place for creating summaries, adding collected
references, or last minute adjustments.

"""

from re import Pattern
from typing import ClassVar
from typing_extensions import TypeGuard
from xml.etree.ElementTree import Element

from markdown import util
from markdown.core import Markdown

def build_treeprocessors(md: Markdown, **kwargs) -> util.Registry[Treeprocessor]:
    """Build the default  `treeprocessors` for Markdown."""

def isString(s: object) -> TypeGuard[str]:
    """Return `True` if object is a string but not an  [`AtomicString`][markdown.util.AtomicString]."""

class Treeprocessor(util.Processor):
    """
    `Treeprocessor`s are run on the `ElementTree` object before serialization.

    Each `Treeprocessor` implements a `run` method that takes a pointer to an
    `Element` and modifies it as necessary.

    `Treeprocessors` must extend `markdown.Treeprocessor`.

    """

    def run(self, root: Element) -> Element | None:
        """
        Subclasses of `Treeprocessor` should implement a `run` method, which
        takes a root `Element`. This method can return another `Element`
        object, and the existing root `Element` will be replaced, or it can
        modify the current tree and return `None`.
        """

class InlineProcessor(Treeprocessor):
    """
    A `Treeprocessor` that traverses a tree, applying inline patterns.
    """

    inlinePatterns: util.Registry[InlineProcessor]
    ancestors: list[str]
    def __init__(self, md: Markdown) -> None: ...
    stashed_nodes: dict[str, Element | str]
    parent_map: dict[Element[str], Element[str]]
    def run(self, tree: Element, ancestors: list[str] | None = None) -> Element:
        """Apply inline patterns to a parsed Markdown tree.

        Iterate over `Element`, find elements with inline tag, apply inline
        patterns and append newly created Elements to tree.  To avoid further
        processing of string with inline patterns, instead of normal string,
        use subclass [`AtomicString`][markdown.util.AtomicString]:

            node.text = markdown.util.AtomicString("This will not be processed.")

        Arguments:
            tree: `Element` object, representing Markdown tree.
            ancestors: List of parent tag names that precede the tree node (if needed).

        Returns:
            An element tree object with applied inline patterns.

        """

class PrettifyTreeprocessor(Treeprocessor):
    """Add line breaks to the html document."""

class UnescapeTreeprocessor(Treeprocessor):
    """Restore escaped chars"""

    RE: ClassVar[Pattern[str]]
    def unescape(self, text: str) -> str: ...
