"""
This package contains modules for language-dependent features of
reStructuredText.
"""

from typing import ClassVar, Final, Protocol, type_check_only

from docutils.languages import LanguageImporter
from docutils.utils import Reporter

__docformat__: Final = "reStructuredText"

@type_check_only
class _RstLanguageModule(Protocol):
    directives: dict[str, str]
    roles: dict[str, str]

class RstLanguageImporter(LanguageImporter):
    """Import language modules.

    When called with a BCP 47 language tag, instances return a module
    with localisations for "directive" and "role" names for  from
    `docutils.parsers.rst.languages` or the PYTHONPATH.

    If there is no matching module, warn (if a `reporter` is passed)
    and return None.
    """

    cache: dict[str, _RstLanguageModule]  # type: ignore[assignment]
    fallback: ClassVar[None]  # type: ignore[assignment]
    def import_from_packages(self, name: str, reporter: Reporter | None = None) -> _RstLanguageModule:  # type: ignore[override]
        """Try loading module `name` from `self.packages`."""

    def check_content(self, module: _RstLanguageModule) -> None:  # type: ignore[override]
        """Check if we got an rST language module."""

    def __call__(self, language_code: str, reporter: Reporter | None = None) -> _RstLanguageModule: ...  # type: ignore[override]

get_language: RstLanguageImporter
