"""
An extension to Python Markdown which implements legacy attributes.

Prior to Python-Markdown version 3.0, the Markdown class had an `enable_attributes`
keyword which was on by default and provided for attributes to be defined for elements
using the format `{@key=value}`. This extension is provided as a replacement for
backward compatibility. New documents should be authored using `attr_lists`. However,
numerous documents exist which have been using the old attribute format for many
years. This extension can be used to continue to render those documents correctly.
"""

from re import Pattern
from xml.etree.ElementTree import Element

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

ATTR_RE: Pattern[str]

class LegacyAttrs(Treeprocessor):
    def run(self, doc: Element) -> None:
        """Find and set values of attributes ({@key=value})."""

    def handleAttributes(self, el: Element, txt: str) -> str:
        """Set attributes and return text without definitions."""

class LegacyAttrExtension(Extension): ...

def makeExtension(**kwargs) -> LegacyAttrExtension: ...
