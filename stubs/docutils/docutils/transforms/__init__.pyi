"""
This package contains modules for standard tree transforms available
to Docutils components. Tree transforms serve a variety of purposes:

- To tie up certain syntax-specific "loose ends" that remain after the
  initial parsing of the input plaintext. These transforms are used to
  supplement a limited syntax.

- To automate the internal linking of the document tree (hyperlink
  references, footnote references, etc.).

- To extract useful information from the document tree. These
  transforms may be used to construct (for example) indexes and tables
  of contents.

Each transform is an optional step that a Docutils component may
choose to perform on the parsed document.
"""

from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from typing import Any, ClassVar, Final
from typing_extensions import TypeAlias

from docutils import ApplicationError, TransformSpec, nodes
from docutils.languages import LanguageImporter

_TransformTuple: TypeAlias = tuple[str, type[Transform], nodes.Node | None, dict[str, Any]]

__docformat__: Final = "reStructuredText"

class TransformError(ApplicationError): ...

class Transform:
    """Docutils transform component abstract base class."""

    default_priority: ClassVar[int | None]
    document: nodes.document
    startnode: nodes.Node | None
    language: LanguageImporter
    def __init__(self, document: nodes.document, startnode: nodes.Node | None = None) -> None:
        """
        Initial setup for in-place document transforms.
        """

    def __getattr__(self, name: str, /) -> Incomplete: ...  # method apply is not implemented

class Transformer(TransformSpec):
    """
    Store "transforms" and apply them to the document tree.

    Collect lists of `Transform` instances and "unknown_reference_resolvers"
    from Docutils components (`TransformSpec` instances).
    Apply collected "transforms" to the document tree.

    Also keeps track of components by component type name.

    https://docutils.sourceforge.io/docs/peps/pep-0258.html#transformer
    """

    transforms: list[_TransformTuple]
    document: nodes.document
    applied: list[_TransformTuple]
    sorted: bool
    components: Mapping[str, TransformSpec]
    serialno: int
    def __init__(self, document: nodes.document): ...
    def add_transform(self, transform_class: type[Transform], priority: int | None = None, **kwargs) -> None:
        """
        Store a single transform.  Use `priority` to override the default.
        `kwargs` is a dictionary whose contents are passed as keyword
        arguments to the `apply` method of the transform.  This can be used to
        pass application-specific data to the transform instance.
        """

    def add_transforms(self, transform_list: Iterable[type[Transform]]) -> None:
        """Store multiple transforms, with default priorities."""

    def add_pending(self, pending: nodes.pending, priority: int | None = None) -> None:
        """Store a transform with an associated `pending` node."""

    def get_priority_string(self, priority: int) -> str:
        """
        Return a string, `priority` combined with `self.serialno`.

        This ensures FIFO order on transforms with identical priority.
        """

    def populate_from_components(self, components: Iterable[TransformSpec]) -> None:
        """
        Store each component's default transforms and reference resolvers

        Transforms are stored with default priorities for later sorting.
        "Unknown reference resolvers" are sorted and stored.
        Components that don't inherit from `TransformSpec` are ignored.

        Also, store components by type name in a mapping for later lookup.
        """

    def apply_transforms(self) -> None:
        """Apply all of the stored transforms, in priority order."""
