"""
This extension adds abbreviation handling to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/abbreviations)
for details.
"""

from re import Pattern
from typing import ClassVar
from typing_extensions import deprecated
from xml.etree.ElementTree import Element

from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor
from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor

class AbbrExtension(Extension):
    """Abbreviation Extension for Python-Markdown."""

    def reset(self) -> None:
        """Clear all previously defined abbreviations."""

    def reset_glossary(self) -> None:
        """Clear all abbreviations from the glossary."""

    def load_glossary(self, dictionary: dict[str, str]) -> None:
        """Adds `dictionary` to our glossary. Any abbreviations that already exist will be overwritten."""

class AbbrTreeprocessor(Treeprocessor):
    """Replace abbreviation text with `<abbr>` elements."""

    RE: Pattern[str] | None
    abbrs: dict[str, str]
    def __init__(self, md: Markdown | None = None, abbrs: dict[str, str] | None = None) -> None: ...
    def create_element(self, title: str, text: str, tail: str) -> Element:
        """Create an `abbr` element."""

    def iter_element(self, el: Element, parent: Element | None = None) -> None:
        """Recursively iterate over elements, run regex on text and wrap matches in `abbr` tags."""

# Techinically it is the same type as `AbbrPreprocessor` just not deprecated.
class AbbrBlockprocessor(BlockProcessor):
    """Parse text for abbreviation references."""

    RE: ClassVar[Pattern[str]]
    abbrs: dict[str, str]
    def __init__(self, parser: BlockParser, abbrs: dict[str, str]) -> None: ...

@deprecated("This class will be removed in the future; use `AbbrTreeprocessor` instead.")
class AbbrPreprocessor(AbbrBlockprocessor):
    """Parse text for abbreviation references."""

@deprecated("This class will be removed in the future; use `AbbrTreeprocessor` instead.")
class AbbrInlineProcessor(InlineProcessor):
    """Abbreviation inline pattern."""

    title: str
    def __init__(self, pattern: str, title: str) -> None: ...

def makeExtension(**kwargs) -> AbbrExtension: ...
