"""
Transforms related to document parts.
"""

from _typeshed import Incomplete, Unused
from collections.abc import Iterable, Sequence
from typing import ClassVar, Final, NoReturn

from docutils import nodes
from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"

class SectNum(Transform):
    """
    Automatically assigns numbers to the titles of document sections.

    It is possible to limit the maximum section level for which the numbers
    are added.  For those sections that are auto-numbered, the "autonum"
    attribute is set, informing the contents table generator that a different
    form of the TOC should be used.
    """

    default_priority: ClassVar[int]
    maxdepth: int
    startvalue: int
    prefix: str
    suffix: str
    def apply(self) -> None: ...
    def update_section_numbers(self, node: nodes.Element, prefix: Iterable[str] = (), depth: int = 0) -> None: ...

class Contents(Transform):
    """
    This transform generates a table of contents from the entire document tree
    or from a single branch.  It locates "section" elements and builds them
    into a nested bullet list, which is placed within a "topic" created by the
    contents directive.  A title is either explicitly specified, taken from
    the appropriate language module, or omitted (local table of contents).
    The depth may be specified.  Two-way references between the table of
    contents and section titles are generated (requires Writer support).

    This transform requires a startnode, which contains generation
    options and provides the location for the generated table of contents (the
    startnode is replaced by the table of contents "topic").
    """

    default_priority: ClassVar[int]
    toc_id: Incomplete
    backlinks: Incomplete
    def apply(self) -> None: ...
    def build_contents(
        self, node: nodes.Element, level: int = 0
    ) -> nodes.bullet_list | list[None]: ...  # return empty list if entries is empty
    def copy_and_filter(self, node: nodes.Node) -> Sequence[nodes.Node]:
        """Return a copy of a title, with references, images, etc. removed."""

class ContentsFilter(nodes.TreeCopyVisitor):
    def get_entry_text(self) -> Sequence[nodes.Node]: ...
    def ignore_node_but_process_children(self, node: Unused) -> NoReturn: ...
    visit_problematic = ignore_node_but_process_children
    visit_reference = ignore_node_but_process_children
    visit_target = ignore_node_but_process_children
