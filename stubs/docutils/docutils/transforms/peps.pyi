"""
Transforms for PEP processing.

- `Headers`: Used to transform a PEP's initial RFC-2822 header.  It remains a
  field list, but some entries get processed.
- `Contents`: Auto-inserts a table of contents.
- `PEPZero`: Special processing for PEP 0.
"""

import re
from typing import ClassVar, Final

from docutils import nodes
from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"

class Headers(Transform):
    """
    Process fields in a PEP's initial RFC-2822 header.
    """

    default_priority: ClassVar[int]
    pep_url: ClassVar[str]
    pep_cvs_url: ClassVar[str]
    rcs_keyword_substitutions: ClassVar[tuple[tuple[re.Pattern[str], str], ...]]
    def apply(self) -> None: ...

class Contents(Transform):
    """
    Insert an empty table of contents topic and a transform placeholder into
    the document after the RFC 2822 header.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class TargetNotes(Transform):
    """
    Locate the "References" section, insert a placeholder for an external
    target footnote insertion transform at the end, and schedule the
    transform to run immediately.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...
    def cleanup_callback(self, pending: nodes.pending) -> None:
        """
        Remove an empty "References" section.

        Called after the `references.TargetNotes` transform is complete.
        """

class PEPZero(Transform):
    """
    Special processing for PEP 0.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class PEPZeroSpecial(nodes.SparseNodeVisitor):
    """
    Perform the special processing needed by PEP 0:

    - Mask email addresses.

    - Link PEP numbers in the second column of 4-column tables to the PEPs
      themselves.
    """

    pep_url: ClassVar[str]
    def unknown_visit(self, node: nodes.Node) -> None: ...
    def visit_reference(self, node: nodes.reference) -> None: ...
    def visit_field_list(self, node: nodes.field_list) -> None: ...
    pep_table: bool
    entry: int
    def visit_tgroup(self, node: nodes.tgroup) -> None: ...
    def visit_colspec(self, node: nodes.colspec) -> None: ...
    def visit_row(self, node: nodes.row) -> None: ...
    def visit_entry(self, node: nodes.entry) -> None: ...

non_masked_addresses: tuple[str, ...]

def mask_email(ref: nodes.reference, pepno: int | None = None) -> nodes.Node:
    """
    Mask the email address in `ref` and return a replacement node.

    `ref` is returned unchanged if it contains no email address.

    For email addresses such as "user@host", mask the address as "user at
    host" (text) to thwart simple email address harvesters (except for those
    listed in `non_masked_addresses`).  If a PEP number (`pepno`) is given,
    return a reference including a default email subject.
    """
