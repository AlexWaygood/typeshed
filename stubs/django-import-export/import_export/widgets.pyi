from collections.abc import Mapping
from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar, overload
from typing_extensions import deprecated

from django.db.models import Model, QuerySet

def format_datetime(value: datetime, datetime_format: str) -> str: ...

class Widget:
    """
    A Widget handles converting between import and export representations.
    """

    coerce_to_string: bool
    def __init__(self, coerce_to_string: bool = True) -> None:
        """
        :param coerce_to_string: If True, :meth:`~import_export.widgets.Widget.render`
          will return a string representation of the value, otherwise the value is
          returned.
        """

    def clean(self, value: Any, row: Mapping[str, Any] | None = None, **kwargs: Any) -> Any:
        """
        Returns an appropriate python object for an imported value.
        For example, a date string will be converted to a python datetime instance.

        :param value: The value to be converted to a native type.
        :param row: A dict containing row key/value pairs.
        :param **kwargs: Optional kwargs.
        """

    @overload
    @deprecated("The 'obj' parameter is deprecated and will be removed in a future release.")
    def render(self, value: Any, obj: Model, **kwargs: Any) -> Any:
        """
        Returns an export representation of a python value.

        :param value: The python value to be rendered.
        :param obj: The model instance from which the value is taken.
          This parameter is deprecated and will be removed in a future release.

        :return: By default, this value will be a string, with ``None`` values returned
          as empty strings.
        """

    @overload
    def render(self, value: Any, obj: None = None, **kwargs: Any) -> Any: ...

class NumberWidget(Widget):
    """
    Widget for converting numeric fields.
    """

    def is_empty(self, value: Any) -> bool: ...

class FloatWidget(NumberWidget):
    """
    Widget for converting float fields.
    """

class IntegerWidget(NumberWidget):
    """
    Widget for converting integer fields.
    """

class DecimalWidget(NumberWidget):
    """
    Widget for converting decimal fields.
    """

class CharWidget(Widget):
    """
    Widget for converting text fields.

    :param allow_blank:  If True, then :meth:`~import_export.widgets.Widget.clean`
      will return null values as empty strings, otherwise as ``None``.
    """

    allow_blank: bool
    def __init__(self, coerce_to_string: bool = True, allow_blank: bool = True) -> None:
        """ """

class BooleanWidget(Widget):
    """
    Widget for converting boolean fields.

    The widget assumes that ``True``, ``False``, and ``None`` are all valid
    values, as to match Django's `BooleanField
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#booleanfield>`_.
    That said, whether the database/Django will actually accept NULL values
    will depend on if you have set ``null=True`` on that Django field.

    While the BooleanWidget is set up to accept as input common variations of
    "True" and "False" (and "None"), you may need to munge less common values
    to ``True``/``False``/``None``. Probably the easiest way to do this is to
    override the :func:`~import_export.resources.Resource.before_import_row`
    function of your Resource class. A short example::

        from import_export import fields, resources, widgets

        class BooleanExample(resources.ModelResource):
            warn = fields.Field(widget=widgets.BooleanWidget())

            def before_import_row(self, row, **kwargs):
                if "warn" in row.keys():
                    # munge "warn" to "True"
                    if row["warn"] in ["warn", "WARN"]:
                        row["warn"] = True

                return super().before_import_row(row, **kwargs)
    """

    TRUE_VALUES: ClassVar[list[str | int | bool]]
    FALSE_VALUES: ClassVar[list[str | int | bool]]
    NULL_VALUES: ClassVar[list[str | None]]
    def __init__(self, coerce_to_string: bool = True) -> None:
        """ """

class DateWidget(Widget):
    """
    Widget for converting date fields to Python date instances.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATE_INPUT_FORMATS`` or ``"%Y-%m-%d"`` is used.
    """

    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class DateTimeWidget(Widget):
    """
    Widget for converting datetime fields to Python datetime instances.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATETIME_INPUT_FORMATS`` or ``"%Y-%m-%d %H:%M:%S"`` is used.
    """

    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class TimeWidget(Widget):
    """
    Widget for converting time fields.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATETIME_INPUT_FORMATS`` or ``"%H:%M:%S"`` is used.
    """

    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class DurationWidget(Widget):
    """
    Widget for converting time duration fields.
    """

class SimpleArrayWidget(Widget):
    """
    Widget for an Array field. Can be used for Postgres' Array field.

    :param separator: Defaults to ``','``
    """

    separator: str
    def __init__(self, separator: str | None = None, coerce_to_string: bool = True) -> None: ...

class JSONWidget(Widget):
    """
    Widget for a JSON object
    (especially required for jsonb fields in PostgreSQL database.)

    :param value: Defaults to JSON format.
    The widget covers two cases: Proper JSON string with double quotes, else it
    tries to use single quotes and then convert it to proper JSON.
    """

_ModelT = TypeVar("_ModelT", bound=Model)

class ForeignKeyWidget(Widget, Generic[_ModelT]):
    """
    Widget for a ``ForeignKey`` field which looks up a related model using
    either the PK or a user specified field that uniquely identifies the
    instance in both export and import.

    The lookup field defaults to using the primary key (``pk``) as lookup
    criterion but can be customized to use any field on the related model.

    Unlike specifying a related field in your resource like so…

    ::

        class Meta:
            fields = ('author__name',)

    …using a :class:`~import_export.widgets.ForeignKeyWidget` has the
    advantage that it can not only be used for exporting, but also importing
    data with foreign key relationships.

    Here's an example on how to use
    :class:`~import_export.widgets.ForeignKeyWidget` to lookup related objects
    using ``Author.name`` instead of ``Author.pk``::

        from import_export import fields, resources
        from import_export.widgets import ForeignKeyWidget

        class BookResource(resources.ModelResource):
            author = fields.Field(
                column_name='author',
                attribute='author',
                widget=ForeignKeyWidget(Author, 'name'))

            class Meta:
                fields = ('author',)

    :param model: The Model the ForeignKey refers to (required).
    :param field: A field on the related model used for looking up a particular
        object.
    :param use_natural_foreign_keys: Use natural key functions to identify
        related object, default to False
    """

    model: _ModelT
    field: str
    key_is_id: bool
    use_natural_foreign_keys: bool
    def __init__(
        self, model: _ModelT, field: str = "pk", use_natural_foreign_keys: bool = False, key_is_id: bool = False, **kwargs: Any
    ) -> None: ...
    def get_queryset(self, value: Any, row: Mapping[str, Any], *args: Any, **kwargs: Any) -> QuerySet[_ModelT]:
        """
        Returns a queryset of all objects for this Model.

        Overwrite this method if you want to limit the pool of objects from
        which the related object is retrieved.

        :param value: The field's value in the dataset.
        :param row: The dataset's current row.
        :param \\*args:
            Optional args.
        :param \\**kwargs:
            Optional kwargs.

        As an example; if you'd like to have ForeignKeyWidget look up a Person
        by their pre- **and** lastname column, you could subclass the widget
        like so::

            class FullNameForeignKeyWidget(ForeignKeyWidget):
                def get_queryset(self, value, row, *args, **kwargs):
                    return self.model.objects.filter(
                        first_name__iexact=row["first_name"],
                        last_name__iexact=row["last_name"]
                    )
        """

    def get_lookup_kwargs(self, value: Any, row: Mapping[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """
        :return: the key value pairs used to identify a model instance.
          Override this to customize instance lookup.

        :param value: The field's value in the dataset.
        :param row: The dataset's current row.
        :param \\**kwargs:
            Optional kwargs.
        """

class ManyToManyWidget(Widget, Generic[_ModelT]):
    """
    Widget that converts between representations of a ManyToMany relationships
    as a list and an actual ManyToMany field.

    :param model: The model the ManyToMany field refers to (required).
    :param separator: Defaults to ``','``.
    :param field: A field on the related model. Default is ``pk``.
    """

    model: _ModelT
    separator: str
    field: str
    def __init__(self, model: _ModelT, separator: str | None = None, field: str | None = None, **kwargs: Any) -> None: ...
