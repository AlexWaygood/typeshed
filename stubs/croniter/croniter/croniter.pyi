import datetime
from _typeshed import Unused
from collections import OrderedDict
from collections.abc import Generator
from re import Match, Pattern
from typing import Any, Final, Generic, Literal, Protocol, TypeVar, overload
from typing_extensions import Never, Self, TypeAlias

_R_co = TypeVar("_R_co", float, datetime.datetime, default=float, covariant=True)
_R2_co = TypeVar("_R2_co", float, datetime.datetime, covariant=True)
_Expressions: TypeAlias = list[str]  # fixed-length list of 5 or 6 strings

class _AllIter(Protocol[_R_co]):
    @overload
    def __call__(
        self, ret_type: type[_R2_co], start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R2_co]: ...
    @overload
    def __call__(
        self, ret_type: None = None, start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R_co]: ...

def is_32bit() -> bool:
    """
    Detect if Python is running in 32-bit mode.
    Compatible with Python 2.6 and later versions.
    Returns True if running on 32-bit Python, False for 64-bit.
    """

OVERFLOW32B_MODE: Final[bool]

UTC_DT: Final[datetime.timezone]
EPOCH: Final[datetime.datetime]
M_ALPHAS: Final[dict[str, int]]
DOW_ALPHAS: Final[dict[str, int]]

MINUTE_FIELD: Final = 0
HOUR_FIELD: Final = 1
DAY_FIELD: Final = 2
MONTH_FIELD: Final = 3
DOW_FIELD: Final = 4
SECOND_FIELD: Final = 5
YEAR_FIELD: Final = 6

UNIX_FIELDS: Final[tuple[int, int, int, int, int]]
SECOND_FIELDS: Final[tuple[int, int, int, int, int, int]]
YEAR_FIELDS: Final[tuple[int, int, int, int, int, int, int]]

step_search_re: Final[Pattern[str]]
only_int_re: Final[Pattern[str]]

WEEKDAYS: Final[str]
MONTHS: Final[str]
star_or_int_re: Final[Pattern[str]]
special_dow_re: Final[Pattern[str]]
re_star: Final[Pattern[str]]
hash_expression_re: Final[Pattern[str]]

CRON_FIELDS: Final[dict[str | int, tuple[int, ...]]]
UNIX_CRON_LEN: Final = 5
SECOND_CRON_LEN: Final = 6
YEAR_CRON_LEN: Final = 7
VALID_LEN_EXPRESSION: Final[set[int]]
TIMESTAMP_TO_DT_CACHE: Final[dict[tuple[float, str], datetime.datetime]]
EXPRESSIONS: dict[tuple[str, bytes], _Expressions]
MARKER: object

def timedelta_to_seconds(td: datetime.timedelta) -> float: ...
def datetime_to_timestamp(d: datetime.datetime) -> float: ...

class CroniterError(ValueError):
    """General top-level Croniter base exception"""

class CroniterBadTypeRangeError(TypeError):
    """."""

class CroniterBadCronError(CroniterError):
    """Syntax, unknown value, or range error within a cron expression"""

class CroniterUnsupportedSyntaxError(CroniterBadCronError):
    """Valid cron syntax, but likely to produce inaccurate results"""

class CroniterBadDateError(CroniterError):
    """Unable to find next/prev timestamp match"""

class CroniterNotAlphaError(CroniterError):
    """Cron syntax contains an invalid day or month abbreviation"""

class croniter(Generic[_R_co]):
    MONTHS_IN_YEAR: Final = 12
    RANGES: Final[
        tuple[
            tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]
        ]
    ]
    DAYS: Final[
        tuple[
            Literal[31],
            Literal[28],
            Literal[31],
            Literal[30],
            Literal[31],
            Literal[30],
            Literal[31],
            Literal[31],
            Literal[30],
            Literal[31],
            Literal[30],
            Literal[31],
        ]
    ]
    ALPHACONV: Final[
        tuple[
            dict[Never, Never],
            dict[Never, Never],
            dict[str, str],
            dict[str, int],
            dict[str, int],
            dict[Never, Never],
            dict[Never, Never],
        ]
    ]
    LOWMAP: Final[
        tuple[
            dict[Never, Never],
            dict[Never, Never],
            dict[int, int],
            dict[int, int],
            dict[int, int],
            dict[Never, Never],
            dict[Never, Never],
        ]
    ]
    LEN_MEANS_ALL: Final[tuple[int, int, int, int, int, int, int]]

    second_at_beginning: bool
    tzinfo: datetime.tzinfo | None

    # Initialized to None, but immediately set to a float.
    start_time: float
    dst_start_time: float
    cur: float

    expanded: list[list[str]]
    nth_weekday_of_month: dict[str, set[int]]
    fields: tuple[int, ...]
    expressions: _Expressions

    @overload
    def __new__(
        cls,
        expr_format: str,
        start_time: float | datetime.datetime | None = None,
        ret_type: type[float] = ...,
        day_or: bool = True,
        max_years_between_matches: int | None = None,
        is_prev: bool = False,
        hash_id: str | bytes | None = None,
        implement_cron_bug: bool = False,
        second_at_beginning: bool | None = None,
        expand_from_start_time: bool = False,
    ) -> croniter[float]: ...
    @overload
    def __new__(
        cls,
        expr_format: str,
        start_time: float | datetime.datetime | None,
        ret_type: type[datetime.datetime],
        day_or: bool = True,
        max_years_between_matches: int | None = None,
        is_prev: bool = False,
        hash_id: str | bytes | None = None,
        implement_cron_bug: bool = False,
        second_at_beginning: bool | None = None,
        expand_from_start_time: bool = False,
    ) -> croniter[datetime.datetime]: ...
    @overload
    def __new__(
        cls,
        expr_format: str,
        *,
        ret_type: type[datetime.datetime],
        day_or: bool = True,
        max_years_between_matches: int | None = None,
        is_prev: bool = False,
        hash_id: str | bytes | None = None,
        implement_cron_bug: bool = False,
        second_at_beginning: bool | None = None,
        expand_from_start_time: bool = False,
    ) -> croniter[datetime.datetime]: ...
    def __init__(
        self,
        expr_format: str,
        start_time: float | datetime.datetime | None = None,
        ret_type: type[_R_co] = ...,
        day_or: bool = True,
        max_years_between_matches: int | None = None,
        is_prev: bool = False,
        hash_id: str | bytes | None = None,
        implement_cron_bug: bool = False,
        second_at_beginning: bool | None = None,
        expand_from_start_time: bool = False,
    ) -> None: ...
    @overload
    def get_next(
        self, ret_type: type[_R2_co], start_time: float | datetime.datetime | None = None, update_current: bool = True
    ) -> _R2_co: ...
    @overload
    def get_next(
        self, ret_type: None = None, start_time: float | datetime.datetime | None = None, update_current: bool = True
    ) -> _R_co: ...
    @overload
    def get_prev(
        self, ret_type: type[_R2_co], start_time: float | datetime.datetime | None = None, update_current: bool = True
    ) -> _R2_co: ...
    @overload
    def get_prev(
        self, ret_type: None = None, start_time: float | datetime.datetime | None = None, update_current: bool = True
    ) -> _R_co: ...
    @overload
    def get_current(self, ret_type: type[_R2_co]) -> _R2_co: ...
    @overload
    def get_current(self, ret_type: None = None) -> _R_co: ...
    def set_current(self, start_time: float | datetime.datetime | None, force: bool = True) -> float: ...
    @staticmethod
    def datetime_to_timestamp(d: datetime.datetime) -> float:
        """
        Converts a `datetime` object `d` into a UNIX timestamp.
        """

    def timestamp_to_datetime(self, timestamp: float, tzinfo: datetime.tzinfo | None = ...) -> datetime.datetime:
        """
        Converts a UNIX `timestamp` into a `datetime` object.
        """

    @staticmethod
    def timedelta_to_seconds(td: datetime.timedelta) -> float:
        """
        Converts a 'datetime.timedelta' object `td` into seconds contained in
        the duration.
        Note: We cannot use `timedelta.total_seconds()` because this is not
        supported by Python 2.6.
        """

    @overload
    def all_next(
        self, ret_type: type[_R2_co], start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R2_co]:
        """
        Returns a generator yielding consecutive dates.

        May be used instead of an implicit call to __iter__ whenever a
        non-default `ret_type` needs to be specified.
        """

    @overload
    def all_next(
        self, ret_type: None = None, start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R_co]: ...
    @overload
    def all_prev(
        self, ret_type: type[_R2_co], start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R2_co]:
        """
        Returns a generator yielding previous dates.
        """

    @overload
    def all_prev(
        self, ret_type: None = None, start_time: float | datetime.datetime | None = None, update_current: bool | None = None
    ) -> Generator[_R_co]: ...
    def iter(self, *args: Unused, **kwargs: Unused) -> _AllIter[_R_co]: ...
    def __iter__(self) -> Self: ...
    @overload
    def next(
        self,
        ret_type: type[_R2_co],
        start_time: float | datetime.datetime | None = None,
        is_prev: bool | None = None,
        update_current: bool | None = None,
    ) -> _R2_co: ...
    @overload
    def next(
        self,
        ret_type: None = None,
        start_time: float | datetime.datetime | None = None,
        is_prev: bool | None = None,
        update_current: bool | None = None,
    ) -> _R_co: ...
    __next__ = next
    @staticmethod
    def is_leap(year: int) -> bool: ...
    @classmethod
    def value_alias(
        cls,
        val: int,
        field_index: Literal[0, 1, 2, 3, 4, 5, 6],
        len_expressions: int | list[Any] | dict[Any, Any] | tuple[Any, ...] | set[Any] = 5,
    ) -> int: ...
    @classmethod
    def expand(
        cls,
        expr_format: str,
        hash_id: bytes | None = None,
        second_at_beginning: bool = False,
        from_timestamp: float | None = None,
    ) -> tuple[list[list[str]], dict[str, set[int]]]:
        """
        Expand a cron expression format into a noramlized format of
        list[list[int | 'l' | '*']]. The first list representing each element
        of the epxression, and each sub-list representing the allowed values
        for that expression component.

        A tuple is returned, the first value being the expanded epxression
        list, and the second being a `nth_weekday_of_month` mapping.

        Examples:

        # Every minute
        >>> croniter.expand('* * * * *')
        ([['*'], ['*'], ['*'], ['*'], ['*']], {})

        # On the hour
        >>> croniter.expand('0 0 * * *')
        ([[0], [0], ['*'], ['*'], ['*']], {})

        # Hours 0-5 and 10 monday through friday
        >>> croniter.expand('0-5,10 * * * mon-fri')
        ([[0, 1, 2, 3, 4, 5, 10], ['*'], ['*'], ['*'], [1, 2, 3, 4, 5]], {})

        Note that some special values such as nth day of week are expanded to a
        special mapping format for later processing:

        # Every minute on the 3rd tuesday of the month
        >>> croniter.expand('* * * * 2#3')
        ([['*'], ['*'], ['*'], ['*'], [2]], {2: {3}})

        # Every hour on the last day of the month
        >>> croniter.expand('0 * l * *')
        ([[0], ['*'], ['l'], ['*'], ['*']], {})

        # On the hour every 15 seconds
        >>> croniter.expand('0 0 * * * */15')
        ([[0], [0], ['*'], ['*'], ['*'], [0, 15, 30, 45]], {})
        """

    @classmethod
    def is_valid(
        cls, expression: str, hash_id: bytes | None = None, encoding: str = "UTF-8", second_at_beginning: bool = False
    ) -> bool: ...
    @classmethod
    def match(
        cls,
        cron_expression: str,
        testdate: float | datetime.datetime | None,
        day_or: bool = True,
        second_at_beginning: bool = False,
    ) -> bool: ...
    @classmethod
    def match_range(
        cls,
        cron_expression: str,
        from_datetime: datetime.datetime,
        to_datetime: datetime.datetime,
        day_or: bool = True,
        second_at_beginning: bool = False,
    ) -> bool: ...

@overload
def croniter_range(
    start: float | datetime.datetime,
    stop: float | datetime.datetime,
    expr_format: str,
    ret_type: type[_R2_co],
    day_or: bool = True,
    exclude_ends: bool = False,
    _croniter: type[croniter] | None = None,
    second_at_beginning: bool = False,
    expand_from_start_time: bool = False,
) -> Generator[_R2_co, None, None]:
    """
    Generator that provides all times from start to stop matching the given cron expression.
    If the cron expression matches either 'start' and/or 'stop', those times will be returned as
    well unless 'exclude_ends=True' is passed.

    You can think of this function as sibling to the builtin range function for datetime objects.
    Like range(start,stop,step), except that here 'step' is a cron expression.
    """

@overload
def croniter_range(
    start: float,
    stop: float | datetime.datetime,
    expr_format: str,
    ret_type: None = None,
    day_or: bool = True,
    exclude_ends: bool = False,
    _croniter: type[croniter] | None = None,
    second_at_beginning: bool = False,
    expand_from_start_time: bool = False,
) -> Generator[float, None, None]: ...
@overload
def croniter_range(
    start: datetime.datetime,
    stop: float | datetime.datetime,
    expr_format: str,
    ret_type: None = None,
    day_or: bool = True,
    exclude_ends: bool = False,
    _croniter: type[croniter] | None = None,
    second_at_beginning: bool = False,
    expand_from_start_time: bool = False,
) -> Generator[datetime.datetime, None, None]: ...

class HashExpander:
    cron: croniter
    def __init__(self, cronit: croniter) -> None: ...
    @overload
    def do(
        self,
        idx: int,
        hash_type: Literal["r"],
        hash_id: None = None,
        range_end: int | None = None,
        range_begin: int | None = None,
    ) -> int:
        """Return a hashed/random integer given range/hash information"""

    @overload
    def do(
        self, idx: int, hash_type: str, hash_id: bytes, range_end: int | None = None, range_begin: int | None = None
    ) -> int: ...
    @overload
    def do(
        self, idx: int, hash_type: str = "h", *, hash_id: bytes, range_end: int | None = None, range_begin: int | None = None
    ) -> int: ...
    def match(self, efl: Unused, idx: Unused, expr: str, hash_id: bytes | None = None, **kw: Unused) -> Match[str] | None: ...
    def expand(
        self,
        efl: object,
        idx: int,
        expr: str,
        hash_id: bytes | None = None,
        match: Match[str] | None | Literal[""] = "",
        **kw: object,
    ) -> str:
        """Expand a hashed/random expression to its normal representation"""

EXPANDERS: OrderedDict[str, HashExpander]
