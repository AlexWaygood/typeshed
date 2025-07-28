"""
pygments.sphinxext
~~~~~~~~~~~~~~~~~~

Sphinx extension to generate automatic documentation of lexers,
formatters and filters.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from docutils.parsers.rst import Directive

MODULEDOC: str
LEXERDOC: str
FMTERDOC: str
FILTERDOC: str

class PygmentsDoc(Directive):
    """
    A directive to collect all lexers/formatters/filters and generate
    autoclass directives for them.
    """

    filenames: set[str]
    def document_lexers(self) -> str: ...
    def document_formatters(self) -> str: ...
    def document_filters(self) -> str: ...

def setup(app) -> None: ...
