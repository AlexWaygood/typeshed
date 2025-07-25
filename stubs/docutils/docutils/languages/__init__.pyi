"""
This package contains modules for language-dependent features of Docutils.
"""

from typing import ClassVar, Final, Protocol, type_check_only

from docutils.utils import Reporter

__docformat__: Final = "reStructuredText"

@type_check_only
class _LanguageModule(Protocol):
    labels: dict[str, str]
    author_separators: list[str]
    bibliographic_fields: list[str]

class LanguageImporter:
    """Import language modules.

    When called with a BCP 47 language tag, instances return a module
    with localisations from `docutils.languages` or the PYTHONPATH.

    If there is no matching module, warn (if a `reporter` is passed)
    and fall back to English.
    """

    packages: ClassVar[tuple[str, ...]]
    warn_msg: ClassVar[str]
    fallback: ClassVar[str]
    cache: dict[str, _LanguageModule]
    def __init__(self) -> None: ...
    def import_from_packages(self, name: str, reporter: Reporter | None = None) -> _LanguageModule:
        """Try loading module `name` from `self.packages`."""

    def check_content(self, module: _LanguageModule) -> None:
        """Check if we got a Docutils language module."""

    def __call__(self, language_code: str, reporter: Reporter | None = None) -> _LanguageModule: ...

get_language: LanguageImporter
