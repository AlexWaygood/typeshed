from _typeshed import SupportsItems
from collections.abc import Collection, Iterator, MutableMapping
from typing import Any, Literal, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from markupsafe import Markup
from wtforms.fields.core import Field, UnboundField
from wtforms.form import BaseForm

_FieldT = TypeVar("_FieldT", bound=Field)

class _SupportsGettextAndNgettext(Protocol):
    def gettext(self, string: str, /) -> str: ...
    def ngettext(self, singular: str, plural: str, n: int, /) -> str: ...

# these are the methods WTForms depends on, the dict can either provide
# a getlist or getall, if it only provides getall, it will wrapped, to
# provide getlist instead
class _MultiDictLikeBase(Protocol):
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: Any, /) -> bool: ...

# since how file uploads are represented in formdata is implementation-specific
# we have to be generous in what we accept in the return of getlist/getall
# we can make this generic if we ever want to be more specific
class _MultiDictLikeWithGetlist(_MultiDictLikeBase, Protocol):
    def getlist(self, key: str, /) -> list[Any]: ...

class _MultiDictLikeWithGetall(_MultiDictLikeBase, Protocol):
    def getall(self, key: str, /) -> list[Any]: ...

_MultiDictLike: TypeAlias = _MultiDictLikeWithGetall | _MultiDictLikeWithGetlist

class DefaultMeta:
    """
    This is the default Meta class which defines all the default values and
    therefore also the 'API' of the class Meta interface.
    """

    def bind_field(self, form: BaseForm, unbound_field: UnboundField[_FieldT], options: MutableMapping[str, Any]) -> _FieldT:
        """
        bind_field allows potential customization of how fields are bound.

        The default implementation simply passes the options to
        :meth:`UnboundField.bind`.

        :param form: The form.
        :param unbound_field: The unbound field.
        :param options:
            A dictionary of options which are typically passed to the field.

        :return: A bound field
        """

    @overload
    def wrap_formdata(self, form: BaseForm, formdata: None) -> None:
        """
        wrap_formdata allows doing custom wrappers of WTForms formdata.

        The default implementation detects webob-style multidicts and wraps
        them, otherwise passes formdata back un-changed.

        :param form: The form.
        :param formdata: Form data.
        :return: A form-input wrapper compatible with WTForms.
        """

    @overload
    def wrap_formdata(self, form: BaseForm, formdata: _MultiDictLike) -> _MultiDictLikeWithGetlist: ...
    def render_field(self, field: Field, render_kw: SupportsItems[str, Any]) -> Markup:
        """
        render_field allows customization of how widget rendering is done.

        The default implementation calls ``field.widget(field, **render_kw)``
        """
    csrf: bool
    csrf_field_name: str
    csrf_secret: Any | None
    csrf_context: Any | None
    csrf_class: type[Any] | None
    def build_csrf(self, form: BaseForm) -> Any:
        """
        Build a CSRF implementation. This is called once per form instance.

        The default implementation builds the class referenced to by
        :attr:`csrf_class` with zero arguments. If `csrf_class` is ``None``,
        will instead use the default implementation
        :class:`wtforms.csrf.session.SessionCSRF`.

        :param form: The form.
        :return: A CSRF implementation.
        """
    locales: Literal[False] | Collection[str]
    cache_translations: bool
    translations_cache: dict[str, _SupportsGettextAndNgettext]
    def get_translations(self, form: BaseForm) -> _SupportsGettextAndNgettext:
        """
        Override in subclasses to provide alternate translations factory.
        See the i18n documentation for more.

        :param form: The form.
        :return: An object that provides gettext() and ngettext() methods.
        """

    def update_values(self, values: SupportsItems[str, Any]) -> None:
        """
        Given a dictionary of values, update values on this `Meta` instance.
        """
    # since meta can be extended with arbitrary data we add a __getattr__
    # method that returns Any
    def __getattr__(self, name: str) -> Any: ...
