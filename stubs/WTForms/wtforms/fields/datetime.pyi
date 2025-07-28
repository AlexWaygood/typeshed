from collections.abc import Callable, Sequence
from datetime import date, datetime, time
from typing import Any
from typing_extensions import Self

from wtforms.fields.core import Field, _Filter, _FormT, _Validator, _Widget
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta, _SupportsGettextAndNgettext

__all__ = ("DateTimeField", "DateField", "TimeField", "MonthField", "DateTimeLocalField", "WeekField")

class DateTimeField(Field):
    """
    A text field which stores a :class:`datetime.datetime` matching one or
    several formats. If ``format`` is a list, any input value matching any
    format will be accepted, and the first format in the list will be used
    to produce HTML values.
    """

    format: list[str]
    strptime_format: list[str]
    data: datetime | None
    default: datetime | Callable[[], datetime] | None
    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = "%Y-%m-%d %H:%M:%S",
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: datetime | Callable[[], datetime] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...

class DateField(DateTimeField):
    """
    Same as :class:`~wtforms.fields.DateTimeField`, except stores a
    :class:`datetime.date`.
    """

    data: date | None  # type: ignore[assignment]
    default: date | Callable[[], date] | None  # type: ignore[assignment]
    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = "%Y-%m-%d",
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: date | Callable[[], date] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...

class TimeField(DateTimeField):
    """
    Same as :class:`~wtforms.fields.DateTimeField`, except stores a
    :class:`datetime.time`.
    """

    data: time | None  # type: ignore[assignment]
    default: time | Callable[[], time] | None  # type: ignore[assignment]
    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = "%H:%M",
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: time | Callable[[], time] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...

class MonthField(DateField):
    """
    Same as :class:`~wtforms.fields.DateField`, except represents a month,
    stores a :class:`datetime.date` with `day = 1`.
    """

    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = "%Y-%m",
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: time | Callable[[], time] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...

class WeekField(DateField):
    """
    Same as :class:`~wtforms.fields.DateField`, except represents a week,
    stores a :class:`datetime.date` of the monday of the given week.
    """

    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = "%Y-W%W",  # only difference is the default value
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: time | Callable[[], time] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...

class DateTimeLocalField(DateTimeField):
    """
    Same as :class:`~wtforms.fields.DateTimeField`, but represents an
    ``<input type="datetime-local">``.
    """

    def __init__(
        self,
        label: str | None = None,
        validators: tuple[_Validator[_FormT, Self], ...] | list[Any] | None = None,
        format: str | list[str] = ...,
        *,
        filters: Sequence[_Filter] = (),
        description: str = "",
        id: str | None = None,
        default: time | Callable[[], time] | None = None,
        widget: _Widget[Self] | None = None,
        render_kw: dict[str, Any] | None = None,
        name: str | None = None,
        _form: BaseForm | None = None,
        _prefix: str = "",
        _translations: _SupportsGettextAndNgettext | None = None,
        _meta: DefaultMeta | None = None,
    ) -> None: ...
