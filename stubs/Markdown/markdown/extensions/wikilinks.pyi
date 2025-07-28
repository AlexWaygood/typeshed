"""
Converts `[[WikiLinks]]` to relative links.

See the [documentation](https://Python-Markdown.github.io/extensions/wikilinks)
for details.
"""

from typing import Any

from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

def build_url(label: str, base: str, end: str) -> str:
    """Build a URL from the label, a base, and an end."""

class WikiLinkExtension(Extension):
    """Add inline processor to Markdown."""

    def __init__(self, **kwargs) -> None: ...
    md: Markdown

class WikiLinksInlineProcessor(InlineProcessor):
    """Build link from `wikilink`."""

    config: dict[str, Any]
    def __init__(self, pattern: str, config: dict[str, Any]) -> None: ...

def makeExtension(**kwargs) -> WikiLinkExtension: ...
