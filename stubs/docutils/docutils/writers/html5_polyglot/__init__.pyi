"""
Plain HyperText Markup Language document tree Writer.

The output conforms to the `HTML 5` specification.

The cascading style sheet "minimal.css" is required for proper viewing,
the style sheet "plain.css" improves reading experience.
"""

from pathlib import Path
from typing import ClassVar, Final

from docutils.writers import _html_base

__docformat__: Final = "reStructuredText"

class Writer(_html_base.Writer):
    default_stylesheets: ClassVar[list[str]]
    default_stylesheet_dirs: ClassVar[list[str]]
    default_template: ClassVar[Path]
    translator_class: type[HTMLTranslator]

class HTMLTranslator(_html_base.HTMLTranslator):
    """
    This writer generates `polyglot markup`: HTML5 that is also valid XML.

    Safe subclassing: when overriding, treat ``visit_*`` and ``depart_*``
    methods as a unit to prevent breaks due to internal changes. See the
    docstring of docutils.writers._html_base.HTMLTranslator for details
    and examples.
    """

    supported_block_tags: set[str]
    supported_inline_tags: set[str]
