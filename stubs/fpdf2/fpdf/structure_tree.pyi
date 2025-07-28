"""
Quoting the PDF spec:
> PDF’s logical _structure facilities_ provide a mechanism for incorporating
> structural information about a document’s content into a PDF file.

> The logical structure of a document is described by a hierarchy of objects called
> the _structure hierarchy_ or _structure tree_.
> At the root of the hierarchy is a dictionary object called the _structure tree root_,
> located by means of the **StructTreeRoot** entry in the document catalog.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete, Unused
from collections import defaultdict
from collections.abc import Iterable, Iterator

from .encryption import StandardSecurityHandler
from .syntax import PDFArray, PDFObject, PDFString

class NumberTree(PDFObject):
    """A number tree is similar to a name tree, except that its keys are integers
    instead of strings and are sorted in ascending numerical order.

    A name tree serves a similar purpose to a dictionary—associating keys and
    values—but by different means.

    The values associated with the keys may be objects of any type. Stream objects
    are required to be specified by indirect object references. It is recommended,
    though not required, that dictionary, array, and string objects be specified by
    indirect object references, and other PDF objects (nulls, numbers, booleans,
    and names) be specified as direct objects
    """

    nums: defaultdict[Incomplete, list[Incomplete]]
    def __init__(self) -> None: ...
    def serialize(self, obj_dict: Unused = None, _security_handler: StandardSecurityHandler | None = None) -> str: ...

class StructTreeRoot(PDFObject):
    type: str
    parent_tree: NumberTree
    k: PDFArray[Incomplete]
    def __init__(self) -> None: ...

class StructElem(PDFObject):
    type: str
    s: str
    p: PDFObject
    k: PDFArray[Incomplete]
    t: PDFString | None
    alt: PDFString | None
    pg: Incomplete | None
    def __init__(
        self,
        struct_type: str,
        parent: PDFObject,
        kids: Iterable[int] | Iterable[StructElem],
        page_number: int | None = None,
        title: str | None = None,
        alt: str | None = None,
    ) -> None: ...
    def page_number(self) -> int | None: ...

class StructureTreeBuilder:
    struct_tree_root: Incomplete
    doc_struct_elem: Incomplete
    struct_elem_per_mc: Incomplete
    def __init__(self) -> None: ...
    def add_marked_content(
        self, page_number: int, struct_type: str, mcid: int | None = None, title: str | None = None, alt_text: str | None = None
    ) -> tuple[Incomplete, Incomplete]: ...
    def next_mcid_for_page(self, page_number: int) -> int: ...
    def empty(self) -> bool: ...
    def __iter__(self) -> Iterator[Incomplete]:
        """Iterate all PDF objects in the tree, starting with the tree root"""
