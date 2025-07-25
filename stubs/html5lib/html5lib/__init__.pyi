"""
HTML parsing library based on the `WHATWG HTML specification
<https://whatwg.org/html>`_. The parser is designed to be compatible with
existing HTML found in the wild and implements well-defined error recovery that
is largely compatible with modern desktop web browsers.

Example usage::

    import html5lib
    with open("my_document.html", "rb") as f:
        tree = html5lib.parse(f)

For convenience, this module re-exports the following names:

* :func:`~.html5parser.parse`
* :func:`~.html5parser.parseFragment`
* :class:`~.html5parser.HTMLParser`
* :func:`~.treebuilders.getTreeBuilder`
* :func:`~.treewalkers.getTreeWalker`
* :func:`~.serializer.serialize`
"""

from typing import Final

from .html5parser import HTMLParser as HTMLParser, parse as parse, parseFragment as parseFragment
from .serializer import serialize as serialize
from .treebuilders import getTreeBuilder as getTreeBuilder
from .treewalkers import getTreeWalker as getTreeWalker

__all__ = ["HTMLParser", "parse", "parseFragment", "getTreeBuilder", "getTreeWalker", "serialize"]

__version__: Final[str]
