"""
This module imports a copy of [`html.parser.HTMLParser`][] and modifies it heavily through monkey-patches.
A copy is imported rather than the module being directly imported as this ensures that the user can import
and  use the unmodified library for their own needs.
"""

import html.parser as htmlparser
import re
from _frozen_importlib import ModuleSpec
from collections.abc import Sequence

from markdown import Markdown

spec: ModuleSpec
blank_line_re: re.Pattern[str]

class HTMLExtractor(htmlparser.HTMLParser):
    """
    Extract raw HTML from text.

    The raw HTML is stored in the [`htmlStash`][markdown.util.HtmlStash] of the
    [`Markdown`][markdown.Markdown] instance passed to `md` and the remaining text
    is stored in `cleandoc` as a list of strings.
    """

    empty_tags: set[str]
    lineno_start_cache: list[int]
    md: Markdown
    def __init__(self, md: Markdown, *args, **kwargs): ...
    inraw: bool
    intail: bool
    stack: list[str]
    cleandoc: list[str]
    @property
    def line_offset(self) -> int:
        """Returns char index in `self.rawdata` for the start of the current line."""

    def at_line_start(self) -> bool:
        """
        Returns True if current position is at start of line.

        Allows for up to three blank spaces at start of line.
        """

    def get_endtag_text(self, tag: str) -> str:
        """
        Returns the text of the end tag.

        If it fails to extract the actual text from the raw data, it builds a closing tag with `tag`.
        """

    def handle_starttag(self, tag: str, attrs: Sequence[tuple[str, str]]) -> None: ...  # type: ignore[override]
    def handle_empty_tag(self, data: str, is_block: bool) -> None:
        """Handle empty tags (`<data>`)."""

    def handle_decl(self, data: str) -> None: ...
    def parse_bogus_comment(self, i: int, report: int = 0) -> int: ...
    def get_starttag_text(self) -> str:
        """Return full source of start tag: `<...>`."""
