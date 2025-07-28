from collections.abc import Callable, Iterable
from gettext import GNUTranslations
from typing import Protocol, TypeVar, overload

_T = TypeVar("_T")

class _SupportsUgettextAndUngettext(Protocol):
    def ugettext(self, string: str, /) -> str: ...
    def ungettext(self, singular: str, plural: str, n: int, /) -> str: ...

def messages_path() -> str:
    """
    Determine the path to the 'messages' directory as best possible.
    """

def get_builtin_gnu_translations(languages: Iterable[str] | None = None) -> GNUTranslations:
    """
    Get a gettext.GNUTranslations object pointing at the
    included translation files.

    :param languages:
        A list of languages to try, in order. If omitted or None, then
        gettext will try to use locale information from the environment.
    """

@overload
def get_translations(
    languages: Iterable[str] | None = None, getter: Callable[[Iterable[str]], GNUTranslations] = ...
) -> GNUTranslations:
    """
    Get a WTForms translation object which wraps a low-level translations object.

    :param languages:
        A sequence of languages to try, in order.
    :param getter:
        A single-argument callable which returns a low-level translations object.
    """

@overload
def get_translations(languages: Iterable[str] | None = None, *, getter: Callable[[Iterable[str]], _T]) -> _T: ...
@overload
def get_translations(languages: Iterable[str] | None, getter: Callable[[Iterable[str]], _T]) -> _T: ...

class DefaultTranslations:
    """
    A WTForms translations object to wrap translations objects which use
    ugettext/ungettext.
    """

    translations: _SupportsUgettextAndUngettext
    def __init__(self, translations: _SupportsUgettextAndUngettext) -> None: ...
    def gettext(self, string: str) -> str: ...
    def ngettext(self, singular: str, plural: str, n: int) -> str: ...

class DummyTranslations:
    """
    A translations object which simply returns unmodified strings.

    This is typically used when translations are disabled or if no valid
    translations provider can be found.
    """

    def gettext(self, string: str) -> str: ...
    def ngettext(self, singular: str, plural: str, n: int) -> str: ...
