"""
Python-Markdown provides two serializers which render [`ElementTree.Element`][xml.etree.ElementTree.Element]
objects to a string of HTML. Both functions wrap the same underlying code with only a few minor
differences as outlined below:

1. Empty (self-closing) tags are rendered as `<tag>` for HTML and as `<tag />` for XHTML.
2. Boolean attributes are rendered as `attrname` for HTML and as `attrname="attrname"` for XHTML.
"""

import re
from xml.etree.ElementTree import Element

__all__ = ["to_html_string", "to_xhtml_string"]

RE_AMP: re.Pattern[str]

def to_html_string(element: Element) -> str:
    """Serialize element and its children to a string of HTML5."""

def to_xhtml_string(element: Element) -> str:
    """Serialize element and its children to a string of XHTML."""
