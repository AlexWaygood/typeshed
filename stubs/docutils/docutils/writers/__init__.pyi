"""
This package contains Docutils Writer modules.
"""

from typing import Any, Final, Generic, TypedDict, TypeVar, type_check_only
from typing_extensions import Required

from docutils import Component, nodes
from docutils.io import Output
from docutils.languages import LanguageImporter

_S = TypeVar("_S")

__docformat__: Final = "reStructuredText"

# It would probably be better to specialize writers for subclasses,
# but this gives us all possible Writer items w/o instance checks
@type_check_only
class _WriterParts(TypedDict, total=False):
    # Parts Provided by All Writers https://docutils.sourceforge.io/docs/api/publisher.html#parts-provided-by-all-writers

    # See Writer.assemble_parts
    whole: Required[str | bytes]
    encoding: Required[str]
    errors: Required[str]
    version: Required[str]

    # Parts Provided by the HTML Writers https://docutils.sourceforge.io/docs/api/publisher.html#parts-provided-by-the-html-writers

    # HTML4 Writer https://docutils.sourceforge.io/docs/api/publisher.html#html4-writer
    # + HTML5 Writer https://docutils.sourceforge.io/docs/api/publisher.html#html5-writer
    body: str
    body_prefix: str
    body_pre_docinfo: str
    body_suffix: str
    docinfo: str
    footer: str
    fragment: str
    head: str
    head_prefix: str
    header: str
    html_body: str
    html_head: str
    html_prolog: str
    html_subtitle: str
    html_title: str
    meta: str
    stylesheet: str
    subtitle: str
    title: str
    # PEP/HTML Writer https://docutils.sourceforge.io/docs/api/publisher.html#pep-html-writer
    # + S5/HTML Writer https://docutils.sourceforge.io/docs/api/publisher.html#s5-html-writer
    pepnum: str

    # Parts Provided by the (Xe)LaTeX Writers https://docutils.sourceforge.io/docs/api/publisher.html#parts-provided-by-the-xe-latex-writers

    # (commenting out those already included)
    abstract: str
    # body: str
    # body_pre_docinfo: str
    dedication: str
    # docinfo: str
    fallbacks: str
    # head_prefix: str
    latex_preamble: str
    pdfsetup: str
    requirements: str
    # stylesheet: str
    # subtitle: str
    # title: str
    titledata: str

class Writer(Component, Generic[_S]):
    """
    Abstract base class for docutils Writers.

    Each writer module or package must export a subclass also called 'Writer'.
    Each writer must support all standard node types listed in
    `docutils.nodes.node_class_names`.

    The `write()` method is the main entry point.
    """

    parts: _WriterParts
    language: LanguageImporter | None = None
    document: nodes.document | None = None
    destination: Output | None = None
    output: _S | None = None
    def __init__(self) -> None: ...
    def write(self, document: nodes.document, destination: Output) -> str | bytes | None:
        """
        Process a document into its final form.

        Translate `document` (a Docutils document tree) into the Writer's
        native format, and write it out to its `destination` (a
        `docutils.io.Output` subclass object).

        Normally not overridden or extended in subclasses.
        """

    def translate(self) -> None:
        """
        Do final translation of `self.document` into `self.output`.  Called
        from `write`.  Override in subclasses.

        Usually done with a `docutils.nodes.NodeVisitor` subclass, in
        combination with a call to `docutils.nodes.Node.walk()` or
        `docutils.nodes.Node.walkabout()`.  The ``NodeVisitor`` subclass must
        support all standard elements (listed in
        `docutils.nodes.node_class_names`) and possibly non-standard elements
        used by the current Reader as well.
        """

    def assemble_parts(self) -> None:
        """Assemble the `self.parts` dictionary.  Extend in subclasses.

        See <https://docutils.sourceforge.io/docs/api/publisher.html>.
        """

class UnfilteredWriter(Writer[_S]):
    """
    A writer that passes the document tree on unchanged (e.g. a
    serializer.)

    Documents written by UnfilteredWriters are typically reused at a
    later date using a subclass of `readers.ReReader`.
    """

def get_writer_class(writer_name: str) -> type[Writer[Any]]:
    """Return the Writer class from the `writer_name` module."""
