"""
Auxiliary transforms mainly to be used by Writer components.

This module is called "writer_aux" because otherwise there would be
conflicting imports like this one::

    from docutils import writers
    from docutils.transforms import writers
"""

from typing import ClassVar, Final
from typing_extensions import deprecated

from docutils import nodes
from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"

@deprecated("docutils.transforms.writer_aux.Compound is deprecated and will be removed in Docutils 0.21 or later.")
class Compound(Transform):
    """
    .. warning:: This transform is not used by Docutils since Dec 2010
                 and will be removed in Docutils 0.21 or later.

    Flatten all compound paragraphs.  For example, transform ::

        <compound>
            <paragraph>
            <literal_block>
            <paragraph>

    into ::

        <paragraph>
        <literal_block classes="continued">
        <paragraph classes="continued">
    """

    default_priority: ClassVar[int]
    def __init__(self, document: nodes.document, startnode: nodes.Node | None = None) -> None: ...
    def apply(self) -> None: ...

class Admonitions(Transform):
    """
    Transform specific admonitions, like this:

        <note>
            <paragraph>
                 Note contents ...

    into generic admonitions, like this::

        <admonition classes="note">
            <title>
                Note
            <paragraph>
                Note contents ...

    The admonition title is localized.
    """

    default_priority: ClassVar[int]
    def apply(self) -> None: ...
