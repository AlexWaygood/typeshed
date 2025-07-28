"""
Add table of contents support to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/toc)
for details.
"""

from collections.abc import Iterator, MutableSet
from re import Pattern
from typing import Any, TypedDict
from typing_extensions import deprecated
from xml.etree.ElementTree import Element

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

IDCOUNT_RE: Pattern[str]

class _FlatTocToken(TypedDict):
    level: int
    id: str
    name: str

class _TocToken(_FlatTocToken):
    children: list[_TocToken]

def slugify(value: str, separator: str, unicode: bool = False) -> str:
    """Slugify a string, to make it URL friendly."""

def slugify_unicode(value: str, separator: str) -> str:
    """Slugify a string, to make it URL friendly while preserving Unicode characters."""

def unique(id: str, ids: MutableSet[str]) -> str:
    """Ensure id is unique in set of ids. Append '_1', '_2'... if not"""

@deprecated("Use `render_inner_html` and `striptags` instead.")
def get_name(el: Element) -> str:
    """Get title name."""

@deprecated("Use `run_postprocessors`, `render_inner_html` and/or `striptags` instead.")
def stashedHTML2text(text: str, md: Markdown, strip_entities: bool = True) -> str:
    """Extract raw HTML from stash, reduce to plain text and swap with placeholder."""

def unescape(text: str) -> str:
    """Unescape Markdown backslash escaped text."""

def strip_tags(text: str) -> str:
    """Strip HTML tags and return plain text. Note: HTML entities are unaffected."""

def escape_cdata(text: str) -> str:
    """Escape character data."""

def run_postprocessors(text: str, md: Markdown) -> str:
    """Run postprocessors from Markdown instance on text."""

def render_inner_html(el: Element, md: Markdown) -> str:
    """Fully render inner html of an `etree` element as a string."""

def remove_fnrefs(root: Element) -> Element:
    """Remove footnote references from a copy of the element, if any are present."""

def nest_toc_tokens(toc_list: list[_FlatTocToken]) -> list[_TocToken]:
    """Given an unsorted list with errors and skips, return a nested one.

        [{'level': 1}, {'level': 2}]
        =>
        [{'level': 1, 'children': [{'level': 2, 'children': []}]}]

    A wrong list is also converted:

        [{'level': 2}, {'level': 1}]
        =>
        [{'level': 2, 'children': []}, {'level': 1, 'children': []}]
    """

class TocTreeprocessor(Treeprocessor):
    """Step through document and build TOC."""

    marker: str
    title: str
    base_level: int
    slugify: Any
    sep: Any
    toc_class: Any
    title_class: str
    use_anchors: bool
    anchorlink_class: str
    use_permalinks: bool
    permalink_class: str
    permalink_title: str
    permalink_leading: bool
    header_rgx: Pattern[str]
    toc_top: int
    toc_bottom: int
    def __init__(self, md: Markdown, config: dict[str, Any]) -> None: ...
    def iterparent(self, node: Element) -> Iterator[tuple[Element, Element]]:
        """Iterator wrapper to get allowed parent and child all at once."""

    def replace_marker(self, root: Element, elem: Element) -> None:
        """Replace marker with elem."""

    def set_level(self, elem: Element) -> None:
        """Adjust header level according to base level."""

    def add_anchor(self, c: Element, elem_id: str) -> None: ...
    def add_permalink(self, c: Element, elem_id: str) -> None: ...
    def build_toc_div(self, toc_list: list[_TocToken]) -> Element:
        """Return a string div given a toc list."""

    def run(self, doc: Element) -> None: ...

class TocExtension(Extension):
    TreeProcessorClass: type[TocTreeprocessor]
    def __init__(self, **kwargs) -> None: ...
    md: Markdown
    def reset(self) -> None: ...

def makeExtension(**kwargs) -> TocExtension: ...
