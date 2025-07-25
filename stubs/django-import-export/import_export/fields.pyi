from collections.abc import Callable, Mapping
from typing import Any, ClassVar

from django.db.models import Model
from django.db.models.fields import NOT_PROVIDED

from .widgets import Widget

class Field:
    """
    ``Field`` represents a mapping between an ``instance`` field and a representation of
    the field's data.

    :param attribute: A string of either an instance attribute or callable of
        the instance.

    :param column_name: An optional column name for the column that represents
        this field in the export.

    :param widget: Defines a widget that will be used to represent this
        field's data in the export, or transform the value during import.

    :param readonly: A Boolean which defines if this field will be ignored
        during import.

    :param default: This value will be returned by
        :meth:`~import_export.fields.Field.clean` if this field's widget returned
        a value defined in :attr:`~import_export.fields.empty_values`.

    :param saves_null_values: Controls whether null values are saved on the instance.
      This can be used if the widget returns null, but there is a default instance
      value which should not be overwritten.

    :param dehydrate_method: You can provide a `dehydrate_method` as a string to use
        instead of the default `dehydrate_{field_name}` syntax, or you can provide
        a callable that will be executed with the instance as its argument.

    :param m2m_add: changes save of this field to add the values, if they do not exist,
        to a ManyToMany field instead of setting all values.  Only useful if field is
        a ManyToMany field.
    """

    empty_values: ClassVar[list[str | None]]
    attribute: str | None
    default: type[NOT_PROVIDED] | Callable[[], Any] | Any
    column_name: str | None
    widget: Widget
    readonly: bool
    saves_null_values: bool
    dehydrate_method: str
    m2m_add: bool
    def __init__(
        self,
        attribute: str | None = None,
        column_name: str | None = None,
        widget: Widget | None = None,
        default: type[NOT_PROVIDED] | Callable[[], Any] | Any = ...,
        readonly: bool = False,
        saves_null_values: bool = True,
        dehydrate_method: str | None = None,
        m2m_add: bool = False,
    ) -> None: ...
    def clean(self, row: Mapping[str, Any], **kwargs: Any) -> Any:
        """
        Translates the value stored in the imported datasource to an
        appropriate Python object and returns it.
        """

    def get_value(self, instance: Model) -> Any:
        """
        Returns the value of the instance's attribute.
        """

    def save(self, instance: Model, row: Mapping[str, Any], is_m2m: bool = False, **kwargs: Any) -> None:
        """
        If this field is not declared readonly, the instance's attribute will
        be set to the value returned by :meth:`~import_export.fields.Field.clean`.
        """

    def export(self, instance: Model, **kwargs: Any) -> str:
        """
        Returns value from the provided instance converted to export
        representation.
        """

    def get_dehydrate_method(self, field_name: str | None = None) -> str:
        """
        Returns method name to be used for dehydration of the field.
        Defaults to `dehydrate_{field_name}`
        """
