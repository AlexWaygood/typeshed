"""
Transforms needed by most or all documents:

- `Decorations`: Generate a document's header & footer.
- `ExposeInternals`: Expose internal attributes.
- `Messages`: Placement of system messages generated after parsing.
- `FilterMessages`: Remove system messages below verbosity threshold.
- `TestMessages`: Like `Messages`, used on test runs.
- `StripComments`: Remove comment elements from the document tree.
- `StripClassesAndElements`: Remove elements with classes
  in `self.document.settings.strip_elements_with_classes`
  and class values in `self.document.settings.strip_classes`.
- `SmartQuotes`: Replace ASCII quotation marks with typographic form.
"""

from _typeshed import Incomplete
from collections.abc import Generator, Iterable
from typing import ClassVar, Final, Literal

from docutils import nodes
from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"

class Decorations(Transform):
    """
    Populate a document's decoration element (header, footer).
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...
    def generate_header(self) -> None: ...
    def generate_footer(self) -> list[nodes.paragraph] | None: ...

class ExposeInternals(Transform):
    """
    Expose internal attributes if ``expose_internals`` setting is set.
    """

    default_priority: ClassVar[int]
    def not_Text(self, node: object) -> bool: ...  # node passing to isinstance() method
    def apply(self) -> None: ...

class Messages(Transform):
    """
    Place any system messages generated after parsing into a dedicated section
    of the document.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class FilterMessages(Transform):
    """
    Remove system messages below verbosity threshold.

    Also convert <problematic> nodes referencing removed messages
    to <Text> nodes and remove "System Messages" section if empty.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class TestMessages(Transform):
    """
    Append all post-parse system messages to the end of the document.

    Used for testing purposes.
    """

    __test__: bool
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class StripComments(Transform):
    """
    Remove comment elements from the document tree (only if the
    ``strip_comments`` setting is enabled).
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class StripClassesAndElements(Transform):
    """
    Remove from the document tree all elements with classes in
    `self.document.settings.strip_elements_with_classes` and all "classes"
    attribute values in `self.document.settings.strip_classes`.
    """

    default_priority: ClassVar[int]
    strip_elements: set[Incomplete]
    def apply(self) -> None: ...
    def check_classes(self, node: object) -> bool: ...

class SmartQuotes(Transform):
    """
    Replace ASCII quotation marks with typographic form.

    Also replace multiple dashes with em-dash/en-dash characters.
    """

    default_priority: ClassVar[int]
    nodes_to_skip: ClassVar[tuple[type[nodes.Node], ...]]
    literal_nodes: ClassVar[tuple[type[nodes.Node | nodes.Body], ...]]
    smartquotes_action: ClassVar[str]
    unsupported_languages: set[str]
    def __init__(self, document: nodes.document, startnode: nodes.Node | None) -> None: ...
    def get_tokens(self, txtnodes: Iterable[nodes.Node]) -> Generator[tuple[Literal["literal", "plain"], str]]: ...
    def apply(self) -> None: ...
