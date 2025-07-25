"""
Quoting section 8.2.2 "Document Outline" of the 2006 PDF spec 1.7:
> The document outline consists of a tree-structured hierarchy of outline items (sometimes called bookmarks),
> which serve as a visual table of contents to display the document’s structure to the user.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete
from collections.abc import Generator, Iterable
from dataclasses import dataclass

from .fonts import TextStyle
from .fpdf import FPDF
from .structure_tree import StructElem
from .syntax import Destination, PDFObject, PDFString

@dataclass
class OutlineSection:
    """OutlineSection(name, level, page_number, dest, struct_elem=None)"""

    name: str
    level: int
    page_number: int
    dest: Destination
    struct_elem: StructElem | None = None

class OutlineItemDictionary(PDFObject):
    title: PDFString
    parent: Incomplete | None
    prev: Incomplete | None
    next: Incomplete | None
    first: Incomplete | None
    last: Incomplete | None
    count: int
    dest: Destination | None
    struct_elem: StructElem | None
    def __init__(self, title: str, dest: Destination | None = None, struct_elem: StructElem | None = None) -> None: ...

class OutlineDictionary(PDFObject):
    type: str
    first: Incomplete | None
    last: Incomplete | None
    count: int
    def __init__(self) -> None: ...

def build_outline_objs(
    sections: Iterable[Incomplete],
) -> Generator[Incomplete, None, list[OutlineDictionary | OutlineItemDictionary]]:
    """
    Build PDF objects constitutive of the documents outline,
    and yield them one by one, starting with the outline dictionary
    """

class TableOfContents:
    """
    A reference implementation of a Table of Contents (ToC) for use with `fpdf2`.

    This class provides a customizable Table of Contents that can be used directly or subclassed
    for additional functionality. To use this class, create an instance of `TableOfContents`,
    configure it as needed, and pass its `render_toc` method as the `render_toc_function` argument
    to `FPDF.insert_toc_placeholder()`.
    """

    text_style: TextStyle
    use_section_title_styles: bool
    level_indent: float
    line_spacing: float
    ignore_pages_before_toc: bool

    def __init__(
        self,
        text_style: TextStyle | None = None,
        use_section_title_styles: bool = False,
        level_indent: float = 7.5,
        line_spacing: float = 1.5,
        ignore_pages_before_toc: bool = True,
    ) -> None: ...
    def get_text_style(self, pdf: FPDF, item: OutlineSection) -> TextStyle: ...
    def render_toc_item(self, pdf: FPDF, item: OutlineSection) -> None: ...
    def render_toc(self, pdf: FPDF, outline: Iterable[OutlineSection]) -> None:
        """This method can be overridden by subclasses to customize the Table of Contents style."""
