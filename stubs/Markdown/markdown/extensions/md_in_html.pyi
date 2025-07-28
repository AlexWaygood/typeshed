"""
Parse Markdown syntax within raw HTML.
Based on the implementation in [PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

See the [documentation](https://Python-Markdown.github.io/extensions/raw_html)
for details.
"""

from collections.abc import Iterable, Mapping
from typing import Literal
from xml.etree.ElementTree import Element, TreeBuilder

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.htmlparser import HTMLExtractor
from markdown.postprocessors import RawHtmlPostprocessor
from markdown.preprocessors import Preprocessor

class HTMLExtractorExtra(HTMLExtractor):
    """
    Override `HTMLExtractor` and create `etree` `Elements` for any elements which should have content parsed as
    Markdown.
    """

    block_level_tags: set[str]
    span_tags: set[str]
    raw_tags: set[str]
    block_tags: set[str]
    span_and_blocks_tags: set[str]
    mdstack: list[str]
    treebuilder: TreeBuilder
    mdstate: list[Literal["block", "span", "off"] | None]
    mdstarted: list[bool]
    def get_element(self) -> Element:
        """Return element from `treebuilder` and reset `treebuilder` for later use."""

    def get_state(self, tag: str, attrs: Mapping[str, str]) -> Literal["block", "span", "off"] | None:
        """Return state from tag and `markdown` attribute. One of 'block', 'span', or 'off'."""

    def handle_starttag(self, tag: str, attrs: Iterable[tuple[str, str | None]]) -> None: ...
    def handle_endtag(self, tag: str) -> None: ...
    def handle_startendtag(self, tag: str, attrs: Iterable[tuple[str, str | None]]) -> None: ...
    def handle_data(self, data: str) -> None: ...
    def handle_empty_tag(self, data: str, is_block: bool) -> None: ...
    def parse_pi(self, i: int) -> int: ...
    def parse_html_declaration(self, i: int) -> int: ...

class HtmlBlockPreprocessor(Preprocessor):
    """Remove html blocks from the text and store them for later retrieval."""

class MarkdownInHtmlProcessor(BlockProcessor):
    """Process Markdown Inside HTML Blocks which have been stored in the `HtmlStash`."""

    def parse_element_content(self, element: Element) -> None:
        """
        Recursively parse the text content of an `etree` Element as Markdown.

        Any block level elements generated from the Markdown will be inserted as children of the element in place
        of the text content. All `markdown` attributes are removed. For any elements in which Markdown parsing has
        been disabled, the text content of it and its children are wrapped in an `AtomicString`.
        """

class MarkdownInHTMLPostprocessor(RawHtmlPostprocessor):
    def stash_to_string(self, text: str | Element) -> str:
        """Override default to handle any `etree` elements still in the stash."""

class MarkdownInHtmlExtension(Extension):
    """Add Markdown parsing in HTML to Markdown class."""

def makeExtension(**kwargs) -> MarkdownInHtmlExtension: ...
