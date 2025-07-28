from builtins import type as _type  # type is being shadowed in Field
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Generic, Protocol, TypeVar, overload
from typing_extensions import Self, TypeAlias

from markupsafe import Markup
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta, _MultiDictLikeWithGetlist, _SupportsGettextAndNgettext

_FormT = TypeVar("_FormT", bound=BaseForm)
_FieldT = TypeVar("_FieldT", bound=Field)
_FormT_contra = TypeVar("_FormT_contra", bound=BaseForm, contravariant=True)
_FieldT_contra = TypeVar("_FieldT_contra", bound=Field, contravariant=True)
# It would be nice to annotate this as invariant, i.e. input type and output type
# needs to be the same, but it will probably be too annoying to use, for now we
# trust, that people won't use it to change the type of data in a field...
_Filter: TypeAlias = Callable[[Any], Any]

class _Validator(Protocol[_FormT_contra, _FieldT_contra]):
    def __call__(self, form: _FormT_contra, field: _FieldT_contra, /) -> object: ...

class _Widget(Protocol[_FieldT_contra]):
    def __call__(self, field: _FieldT_contra, **kwargs: Any) -> Markup: ...

class Field:
    """
    Field base class
    """

    errors: Sequence[str]
    process_errors: Sequence[str]
    raw_data: list[Any] | None
    object_data: Any
    data: Any
    validators: Sequence[_Validator[Any, Self]]
    # even though this could be None on the base class, this should
    # never actually be None in a real field
    widget: _Widget[Self]
    do_not_call_in_templates: bool
    meta: DefaultMeta
    default: Any | None
    description: str
    render_kw: dict[str, Any]
    filters: Sequence[_Filter]
    flags: Flags
    name: str
    short_name: str
    id: str
    type: str
    label: Label
    # technically this can return UnboundField, but that is not allowed
    # by type checkers, so we use a descriptor hack to get around this
    # limitation instead
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
    def __init__(
        self,
        label: str | None = None,
        # for tuple we can be a bit more type safe and only accept validators
        # that would work on this or a less specific field, but in general it
        # would be too annoying to restrict to Sequence[_Validator], since mypy
        # will infer a list of mixed validators as list[object], since that is
        # the common base class between all validators
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: object | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None:
        """
        Construct a new field.

        :param label:
            The label of the field.
        :param validators:
            A sequence of validators to call when `validate` is called.
        :param filters:
            A sequence of callable which are run by :meth:`~Field.process`
            to filter or transform the input data. For example
            ``StringForm(filters=[str.strip, str.upper])``.
            Note that filters are applied after processing the default and
            incoming data, but before validation.
        :param description:
            A description for the field, typically used for help text.
        :param id:
            An id to use for the field. A reasonable default is set by the form,
            and you shouldn't need to set this manually.
        :param default:
            The default value to assign to the field, if no form or object
            input is provided. May be a callable.
        :param widget:
            If provided, overrides the widget used to render the field.
        :param dict render_kw:
            If provided, a dictionary which provides default keywords that
            will be given to the widget at render time.
        :param name:
            The HTML name of this field. The default value is the Python
            attribute name.
        :param _form:
            The form holding this field. It is passed by the form itself during
            construction. You should never pass this value yourself.
        :param _prefix:
            The prefix to prepend to the form name of this field, passed by
            the enclosing form during construction.
        :param _translations:
            A translations object providing message translations. Usually
            passed by the enclosing form during construction. See
            :doc:`I18n docs <i18n>` for information on message translations.
        :param _meta:
            If provided, this is the 'meta' instance from the form. You usually
            don't pass this yourself.

        If `_form` isn't provided, an :class:`UnboundField` will be
        returned instead. Call its :func:`bind` method with a form instance and
        a name to construct the field.
        """

    def __html__(self) -> str:
        """
        Returns a HTML representation of the field. For more powerful rendering,
        see the :meth:`__call__` method.
        """

    def __call__(self, **kwargs: object) -> Markup:
        """
        Render this field as HTML, using keyword args as additional attributes.

        This delegates rendering to
        :meth:`meta.render_field <wtforms.meta.DefaultMeta.render_field>`
        whose default behavior is to call the field's widget, passing any
        keyword arguments from this call along to the widget.

        In all of the WTForms HTML widgets, keyword arguments are turned to
        HTML attributes, though in theory a widget is free to do anything it
        wants with the supplied keyword arguments, and widgets don't have to
        even do anything related to HTML.
        """

    @classmethod
    def check_validators(cls, validators: Iterable[_Validator[_FormT, Self]] | None) -> None: ...
    def gettext(self, string: str) -> str:
        """
        Get a translation for the given message.

        This proxies for the internal translations object.

        :param string: A string to be translated.
        :return: A string which is the translated output.
        """

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        """
        Get a translation for a message which can be pluralized.

        :param str singular: The singular form of the message.
        :param str plural: The plural form of the message.
        :param int n: The number of elements this message is referring to
        """

    def validate(self, form: BaseForm, extra_validators: tuple[_Validator[_FormT, Self], ...] | list[Any] = ()) -> bool:
        """
        Validates the field and returns True or False. `self.errors` will
        contain any errors raised during validation. This is usually only
        called by `Form.validate`.

        Subfields shouldn't override this, but rather override either
        `pre_validate`, `post_validate` or both, depending on needs.

        :param form: The form the field belongs to.
        :param extra_validators: A sequence of extra validators to run.
        """

    def pre_validate(self, form: BaseForm) -> None:
        """
        Override if you need field-level validation. Runs before any other
        validators.

        :param form: The form the field belongs to.
        """

    def post_validate(self, form: BaseForm, validation_stopped: bool) -> None:
        """
        Override if you need to run any field-level validation tasks after
        normal validation. This shouldn't be needed in most cases.

        :param form: The form the field belongs to.
        :param validation_stopped:
            `True` if any validator raised StopValidation.
        """

    def process(
        self, formdata: _MultiDictLikeWithGetlist | None, data: Any = ..., extra_filters: Sequence[_Filter] | None = None
    ) -> None:
        """
        Process incoming data, calling process_data, process_formdata as needed,
        and run filters.

        If `data` is not provided, process_data will be called on the field's
        default.

        Field subclasses usually won't override this, instead overriding the
        process_formdata and process_data methods. Only override this for
        special advanced processing, such as when a field encapsulates many
        inputs.

        :param extra_filters: A sequence of extra filters to run.
        """

    def process_data(self, value: Any) -> None:
        """
        Process the Python data applied to this field and store the result.

        This will be called during form construction by the form's `kwargs` or
        `obj` argument.

        :param value: The python object containing the value to process.
        """

    def process_formdata(self, valuelist: list[Any]) -> None:
        """
        Process data received over the wire from a form.

        This will be called during form construction with data supplied
        through the `formdata` argument.

        :param valuelist: A list of strings to process.
        """

    def populate_obj(self, obj: object, name: str) -> None:
        """
        Populates `obj.<name>` with the field's data.

        :note: This is a destructive operation. If `obj.<name>` already exists,
               it will be overridden. Use with caution.
        """
    # this is a workaround for what is essentially illegal in static type checking
    # Field.__new__ would return an UnboundField, unless the _form parameter is
    # specified. We can't really work around it by making UnboundField a subclass
    # of Field, since all subclasses of Field still need to return an UnboundField
    # and we can't expect third parties to add a __new__ method to every field
    # they define...
    # This workaround only works for Form, not BaseForm, but we take what we can get
    # BaseForm shouldn't really be used anyways
    @overload
    def __get__(self, obj: None, owner: _type[object] | None = None) -> UnboundField[Self]: ...
    @overload
    def __get__(self, obj: object, owner: _type[object] | None = None) -> Self: ...

class UnboundField(Generic[_FieldT]):
    creation_counter: int
    field_class: type[_FieldT]
    name: str | None
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    def __init__(self, field_class: type[_FieldT], *args: object, name: str | None = None, **kwargs: object) -> None: ...
    def bind(
        self,
        form: BaseForm,
        name: str,
        prefix: str = "",
        translations: _SupportsGettextAndNgettext | None = None,
        **kwargs: object,
    ) -> _FieldT: ...

class Flags:
    """
    Holds a set of flags as attributes.

    Accessing a non-existing attribute returns None for its value.
    """

    # the API for this is a bit loosey goosey, the intention probably
    # was that the values should always be boolean, but __contains__
    # just returns the same thing as __getattr__ and in the widgets
    # there are fields that could accept numeric values from Flags
    def __getattr__(self, name: str) -> Any | None: ...
    def __setattr__(self, name: str, value: object) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __contains__(self, name: str) -> Any | None: ...

class Label:
    """
    An HTML form label.
    """

    field_id: str
    text: str
    def __init__(self, field_id: str, text: str) -> None: ...
    def __html__(self) -> str: ...
    def __call__(self, text: str | None = None, **kwargs: Any) -> Markup: ...
