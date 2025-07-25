"""
Modify the behavior of Lists in Python-Markdown to act in a sane manor.

See [documentation](https://Python-Markdown.github.io/extensions/sane_lists)
for details.
"""

from markdown import blockparser
from markdown.blockprocessors import OListProcessor, UListProcessor
from markdown.extensions import Extension

class SaneOListProcessor(OListProcessor):
    """Override `SIBLING_TAGS` to not include `ul` and set `LAZY_OL` to `False`."""

    def __init__(self, parser: blockparser.BlockParser) -> None: ...

class SaneUListProcessor(UListProcessor):
    """Override `SIBLING_TAGS` to not include `ol`."""

    def __init__(self, parser: blockparser.BlockParser) -> None: ...

class SaneListExtension(Extension):
    """Add sane lists to Markdown."""

def makeExtension(**kwargs) -> SaneListExtension: ...
