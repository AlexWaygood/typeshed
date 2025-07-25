"""
Adds attribute list syntax to Python-Markdown.
Inspired by
[Maruku](http://maruku.rubyforge.org/proposal.html#attribute_lists)'s
feature of the same name.

See the [documentation](https://Python-Markdown.github.io/extensions/attr_list)
for details.
"""

from re import Pattern
from xml.etree.ElementTree import Element

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

def get_attrs_and_remainder(attrs_string: str) -> tuple[list[tuple[str, str]], str]:
    """Parse attribute list and return a list of attribute tuples.

    Additionally, return any text that remained after a curly brace. In typical cases, its presence
    should mean that the input does not match the intended attribute list syntax.
    """

def get_attrs(str: str) -> list[tuple[str, str]]:
    """Soft-deprecated. Prefer `get_attrs_and_remainder`."""

def isheader(elem: Element) -> bool: ...

class AttrListTreeprocessor(Treeprocessor):
    BASE_RE: str
    HEADER_RE: Pattern[str]
    BLOCK_RE: Pattern[str]
    INLINE_RE: Pattern[str]
    NAME_RE: Pattern[str]
    def run(self, doc: Element) -> None: ...
    def assign_attrs(self, elem: Element, attrs_string: str, *, strict: bool = False) -> str:
        """Assign `attrs` to element.

        If the `attrs_string` has an extra closing curly brace, the remaining text is returned.

        The `strict` argument controls whether to still assign `attrs` if there is a remaining `}`.
        """

    def sanitize_name(self, name: str) -> str:
        """
        Sanitize name as 'an XML Name, minus the `:`.'
        See <https://www.w3.org/TR/REC-xml-names/#NT-NCName>.
        """

class AttrListExtension(Extension):
    """Attribute List extension for Python-Markdown"""

def makeExtension(**kwargs) -> AttrListExtension: ...
