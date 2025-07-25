from _typeshed import SupportsItems
from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any, ClassVar, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from wtforms.fields.core import Field, UnboundField
from wtforms.meta import DefaultMeta, _MultiDictLike

_T = TypeVar("_T")
_FormErrors: TypeAlias = dict[str, Sequence[str] | _FormErrors]

# _unbound_fields will always be a list on an instance, but on a
# class it might be None, if it never has been instantiated, or
# not instantianted after a new field had been added/removed
class _UnboundFields(Protocol):
    @overload
    def __get__(self, obj: None, owner: type[object] | None = None, /) -> list[tuple[str, UnboundField[Any]]] | None: ...
    @overload
    def __get__(self, obj: object, owner: type[object] | None = None, /) -> list[tuple[str, UnboundField[Any]]]: ...

class BaseForm:
    """
    Base Form Class.  Provides core behaviour like field construction,
    validation, and data and error proxying.
    """

    meta: DefaultMeta
    form_errors: list[str]
    # we document this, because it's the only efficient way to introspect
    # the field names of the form, it also seems to be stable API-wise
    _fields: dict[str, Field]
    def __init__(
        self,
        fields: SupportsItems[str, UnboundField[Any]] | Iterable[tuple[str, UnboundField[Any]]],
        prefix: str = "",
        meta: DefaultMeta = ...,
    ) -> None:
        """
        :param fields:
            A dict or sequence of 2-tuples of partially-constructed fields.
        :param prefix:
            If provided, all fields will have their name prefixed with the
            value.
        :param meta:
            A meta instance which is used for configuration and customization
            of WTForms behaviors.
        """

    def __iter__(self) -> Iterator[Field]:
        """Iterate form fields in creation order."""

    def __contains__(self, name: str) -> bool:
        """Returns `True` if the named field is a member of this form."""

    def __getitem__(self, name: str) -> Field:
        """Dict-style access to this form's fields."""

    def __setitem__(self, name: str, value: UnboundField[Any]) -> None:
        """Bind a field to this form."""

    def __delitem__(self, name: str) -> None:
        """Remove a field from this form."""

    def populate_obj(self, obj: object) -> None:
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields.

        :note: This is a destructive operation; Any attribute with the same name
               as a field will be overridden. Use with caution.
        """
    # while we would like to be more strict on extra_filters, we can't easily do that
    # without it being annoying in most situations
    def process(
        self,
        formdata: _MultiDictLike | None = None,
        obj: object | None = None,
        data: Mapping[str, Any] | None = None,
        extra_filters: Mapping[str, Sequence[Any]] | None = None,
        **kwargs: object,
    ) -> None:
        """Process default and input data with each field.

        :param formdata: Input data coming from the client, usually
            ``request.form`` or equivalent. Should provide a "multi
            dict" interface to get a list of values for a given key,
            such as what Werkzeug, Django, and WebOb provide.
        :param obj: Take existing data from attributes on this object
            matching form field attributes. Only used if ``formdata`` is
            not passed.
        :param data: Take existing data from keys in this dict matching
            form field attributes. ``obj`` takes precedence if it also
            has a matching attribute. Only used if ``formdata`` is not
            passed.
        :param extra_filters: A dict mapping field attribute names to
            lists of extra filter functions to run. Extra filters run
            after filters passed when creating the field. If the form
            has ``filter_<fieldname>``, it is the last extra filter.
        :param kwargs: Merged with ``data`` to allow passing existing
            data as parameters. Overwrites any duplicate keys in
            ``data``. Only used if ``formdata`` is not passed.
        """
    # same thing here with extra_validators
    def validate(self, extra_validators: Mapping[str, Sequence[Any]] | None = None) -> bool:
        """
        Validates the form by calling `validate` on each field.

        :param extra_validators:
            If provided, is a dict mapping field names to a sequence of
            callables which will be passed as extra validators to the field's
            `validate` method.

        Returns `True` if no errors occur.
        """

    @property
    def data(self) -> dict[str, Any]: ...
    # because of the Liskov violation in FormField.errors we need to make errors a recursive type
    @property
    def errors(self) -> _FormErrors: ...

class FormMeta(type):
    """
    The metaclass for `Form` and any subclasses of `Form`.

    `FormMeta`'s responsibility is to create the `_unbound_fields` list, which
    is a list of `UnboundField` instances sorted by their order of
    instantiation.  The list is created at the first instantiation of the form.
    If any fields are added/removed from the form, the list is cleared to be
    re-generated on the next instantiation.

    Any properties which begin with an underscore or are not `UnboundField`
    instances are ignored by the metaclass.
    """

    def __init__(cls, name: str, bases: Sequence[type[object]], attrs: Mapping[str, Any]) -> None: ...
    def __call__(cls: type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Construct a new `Form` instance.

        Creates the `_unbound_fields` list and the internal `_wtforms_meta`
        subclass of the class Meta in order to allow a proper inheritance
        hierarchy.
        """

    def __setattr__(cls, name: str, value: object) -> None:
        """
        Add an attribute to the class, clearing `_unbound_fields` if needed.
        """

    def __delattr__(cls, name: str) -> None:
        """
        Remove an attribute from the class, clearing `_unbound_fields` if
        needed.
        """

class Form(BaseForm, metaclass=FormMeta):
    """
    Declarative Form base class. Extends BaseForm's core behaviour allowing
    fields to be defined on Form subclasses as class attributes.

    In addition, form and instance input data are taken at construction time
    and passed to `process()`.
    """

    # due to the metaclass this should always be a subclass of DefaultMeta
    # but if we annotate this as such, then subclasses cannot use it in the
    # intended way
    Meta: ClassVar[type[Any]]
    # this attribute is documented, so we annotate it
    _unbound_fields: _UnboundFields
    def __init__(
        self,
        formdata: _MultiDictLike | None = None,
        obj: object | None = None,
        prefix: str = "",
        data: Mapping[str, Any] | None = None,
        meta: Mapping[str, Any] | None = None,
        *,
        # same issue as with process
        extra_filters: Mapping[str, Sequence[Any]] | None = None,
        **kwargs: object,
    ) -> None:
        """
        :param formdata: Input data coming from the client, usually
            ``request.form`` or equivalent. Should provide a "multi
            dict" interface to get a list of values for a given key,
            such as what Werkzeug, Django, and WebOb provide.
        :param obj: Take existing data from attributes on this object
            matching form field attributes. Only used if ``formdata`` is
            not passed.
        :param prefix: If provided, all fields will have their name
            prefixed with the value. This is for distinguishing multiple
            forms on a single page. This only affects the HTML name for
            matching input data, not the Python name for matching
            existing data.
        :param data: Take existing data from keys in this dict matching
            form field attributes. ``obj`` takes precedence if it also
            has a matching attribute. Only used if ``formdata`` is not
            passed.
        :param meta: A dict of attributes to override on this form's
            :attr:`meta` instance.
        :param extra_filters: A dict mapping field attribute names to
            lists of extra filter functions to run. Extra filters run
            after filters passed when creating the field. If the form
            has ``filter_<fieldname>``, it is the last extra filter.
        :param kwargs: Merged with ``data`` to allow passing existing
            data as parameters. Overwrites any duplicate keys in
            ``data``. Only used if ``formdata`` is not passed.
        """
    # this should emit a type_error, since it's not allowed to be called
    def __setitem__(self, name: str, value: None) -> None: ...  # type: ignore[override]
    def __delitem__(self, name: str) -> None: ...
    def __delattr__(self, name: str) -> None: ...

__all__ = ("BaseForm", "Form")
