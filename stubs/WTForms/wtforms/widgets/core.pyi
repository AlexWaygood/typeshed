from decimal import Decimal
from typing import Any, Literal

from markupsafe import Markup
from wtforms.fields import Field, FormField, StringField
from wtforms.fields.choices import SelectFieldBase, _Option

__all__ = (
    "CheckboxInput",
    "ColorInput",
    "DateInput",
    "DateTimeInput",
    "DateTimeLocalInput",
    "EmailInput",
    "FileInput",
    "HiddenInput",
    "ListWidget",
    "MonthInput",
    "NumberInput",
    "Option",
    "PasswordInput",
    "RadioInput",
    "RangeInput",
    "SearchInput",
    "Select",
    "SubmitInput",
    "TableWidget",
    "TextArea",
    "TextInput",
    "TelInput",
    "TimeInput",
    "URLInput",
    "WeekInput",
)

def html_params(**kwargs: object) -> str:
    """
    Generate HTML attribute syntax from inputted keyword arguments.

    The output value is sorted by the passed keys, to provide consistent output
    each time this function is called with the same parameters. Because of the
    frequent use of the normally reserved keywords `class` and `for`, suffixing
    these with an underscore will allow them to be used.

    In order to facilitate the use of ``data-`` and ``aria-`` attributes, if the
    name of the attribute begins with ``data_`` or ``aria_``, then every
    underscore will be replaced with a hyphen in the generated attribute.

    >>> html_params(data_attr='user.name', aria_labeledby='name')
    'data-attr="user.name" aria-labeledby="name"'

    In addition, the values ``True`` and ``False`` are special:
      * ``attr=True`` generates the HTML compact output of a boolean attribute,
        e.g. ``checked=True`` will generate simply ``checked``
      * ``attr=False`` will be ignored and generate no output.

    >>> html_params(name='text1', id='f', class_='text')
    'class="text" id="f" name="text1"'
    >>> html_params(checked=True, readonly=False, name="text1", abc="hello")
    'abc="hello" checked name="text1"'

    .. versionchanged:: 3.0
        ``aria_`` args convert underscores to hyphens like ``data_``
        args.

    .. versionchanged:: 2.2
        ``data_`` args convert all underscores to hyphens, instead of
        only the first one.
    """

class ListWidget:
    """
    Renders a list of fields as a `ul` or `ol` list.

    This is used for fields which encapsulate many inner fields as subfields.
    The widget will try to iterate the field to get access to the subfields and
    call them to render them.

    If `prefix_label` is set, the subfield's label is printed before the field,
    otherwise afterwards. The latter is useful for iterating radios or
    checkboxes.
    """

    html_tag: Literal["ul", "ol"]
    prefix_label: bool
    def __init__(self, html_tag: Literal["ul", "ol"] = "ul", prefix_label: bool = True) -> None: ...
    # any iterable field is fine, since people might define iterable fields
    # that are not derived from FieldList, we just punt and accept any field
    # with Intersection we could be more specific
    def __call__(self, field: Field, **kwargs: object) -> Markup: ...

class TableWidget:
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """

    with_table_tag: bool
    def __init__(self, with_table_tag: bool = True) -> None: ...
    def __call__(self, field: FormField[Any], **kwargs: object) -> Markup: ...

class Input:
    """
    Render a basic ``<input>`` field.

    This is used as the basis for most of the other input fields.

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    validation_attrs: list[str]
    input_type: str
    def __init__(self, input_type: str | None = None) -> None: ...
    def __call__(self, field: Field, **kwargs: object) -> Markup: ...
    @staticmethod
    def html_params(**kwargs: object) -> str:
        """
        Generate HTML attribute syntax from inputted keyword arguments.

        The output value is sorted by the passed keys, to provide consistent output
        each time this function is called with the same parameters. Because of the
        frequent use of the normally reserved keywords `class` and `for`, suffixing
        these with an underscore will allow them to be used.

        In order to facilitate the use of ``data-`` and ``aria-`` attributes, if the
        name of the attribute begins with ``data_`` or ``aria_``, then every
        underscore will be replaced with a hyphen in the generated attribute.

        >>> html_params(data_attr='user.name', aria_labeledby='name')
        'data-attr="user.name" aria-labeledby="name"'

        In addition, the values ``True`` and ``False`` are special:
          * ``attr=True`` generates the HTML compact output of a boolean attribute,
            e.g. ``checked=True`` will generate simply ``checked``
          * ``attr=False`` will be ignored and generate no output.

        >>> html_params(name='text1', id='f', class_='text')
        'class="text" id="f" name="text1"'
        >>> html_params(checked=True, readonly=False, name="text1", abc="hello")
        'abc="hello" checked name="text1"'

        .. versionchanged:: 3.0
            ``aria_`` args convert underscores to hyphens like ``data_``
            args.

        .. versionchanged:: 2.2
            ``data_`` args convert all underscores to hyphens, instead of
            only the first one.
        """

class TextInput(Input):
    """
    Render a single-line text input.
    """

class PasswordInput(Input):
    """
    Render a password input.

    For security purposes, this field will not reproduce the value on a form
    submit by default. To have the value filled in, set `hide_value` to
    `False`.
    """

    hide_value: bool
    def __init__(self, hide_value: bool = True) -> None: ...

class HiddenInput(Input):
    """
    Render a hidden input.
    """

    field_flags: dict[str, Any]

class CheckboxInput(Input):
    """
    Render a checkbox.

    The ``checked`` HTML attribute is set if the field's data is a non-false value.
    """

class RadioInput(Input):
    """
    Render a single radio button.

    This widget is most commonly used in conjunction with ListWidget or some
    other listing, as singular radio buttons are not very useful.
    """

class FileInput(Input):
    """Render a file chooser input.

    :param multiple: allow choosing multiple files
    """

    multiple: bool
    def __init__(self, multiple: bool = False) -> None: ...

class SubmitInput(Input):
    """
    Renders a submit button.

    The field's label is used as the text of the submit button instead of the
    data on the field.
    """

class TextArea:
    """
    Renders a multi-line text area.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    validation_attrs: list[str]
    def __call__(self, field: StringField, **kwargs: object) -> Markup: ...

class Select:
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)` or `(value, label, selected, render_kw)`.
    It also must provide a `has_groups()` method which tells whether choices
    are divided into groups, and if they do, the field must have an
    `iter_groups()` method that yields tuples of `(label, choices)`, where
    `choices` is a iterable of `(value, label, selected)` tuples.
    """

    validation_attrs: list[str]
    multiple: bool
    def __init__(self, multiple: bool = False) -> None: ...
    def __call__(self, field: SelectFieldBase, **kwargs: object) -> Markup: ...
    @classmethod
    def render_option(cls, value: object, label: str, selected: bool, **kwargs: object) -> Markup: ...

class Option:
    """
    Renders the individual option from a select field.

    This is just a convenience for various custom rendering situations, and an
    option by itself does not constitute an entire field.
    """

    def __call__(self, field: _Option, **kwargs: object) -> Markup: ...

class SearchInput(Input):
    """
    Renders an input with type "search".
    """

class TelInput(Input):
    """
    Renders an input with type "tel".
    """

class URLInput(Input):
    """
    Renders an input with type "url".
    """

class EmailInput(Input):
    """
    Renders an input with type "email".
    """

class DateTimeInput(Input):
    """
    Renders an input with type "datetime".
    """

class DateInput(Input):
    """
    Renders an input with type "date".
    """

class MonthInput(Input):
    """
    Renders an input with type "month".
    """

class WeekInput(Input):
    """
    Renders an input with type "week".
    """

class TimeInput(Input):
    """
    Renders an input with type "time".
    """

class DateTimeLocalInput(Input):
    """
    Renders an input with type "datetime-local".
    """

class NumberInput(Input):
    """
    Renders an input with type "number".
    """

    step: Decimal | float | str | None
    min: Decimal | float | str | None
    max: Decimal | float | str | None
    def __init__(
        self,
        step: Decimal | float | str | None = None,
        min: Decimal | float | str | None = None,
        max: Decimal | float | str | None = None,
    ) -> None: ...

class RangeInput(Input):
    """
    Renders an input with type "range".
    """

    # maybe we should allow any str for this
    step: Decimal | float | str | None
    def __init__(self, step: Decimal | float | str | None = None) -> None: ...

class ColorInput(Input):
    """
    Renders an input with type "color".
    """
