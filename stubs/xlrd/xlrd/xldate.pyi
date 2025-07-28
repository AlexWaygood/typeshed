"""
Tools for working with dates and times in Excel files.

The conversion from ``days`` to ``(year, month, day)`` starts with
an integral "julian day number" aka JDN.
FWIW:

- JDN 0 corresponds to noon on Monday November 24 in Gregorian year -4713.

More importantly:

- Noon on Gregorian 1900-03-01 (day 61 in the 1900-based system) is JDN 2415080.0
- Noon on Gregorian 1904-01-02 (day  1 in the 1904-based system) is JDN 2416482.0

"""

import datetime
from typing import Final, Literal

_JDN_delta: Final[tuple[int, int]]
epoch_1904: Final[datetime.datetime]
epoch_1900: Final[datetime.datetime]
epoch_1900_minus_1: Final[datetime.datetime]
_XLDAYS_TOO_LARGE: Final[tuple[int, int]]
_days_in_month: Final[tuple[None, int, int, int, int, int, int, int, int, int, int, int, int]]

class XLDateError(ValueError):
    """A base class for all datetime-related errors."""

class XLDateNegative(XLDateError):
    """``xldate < 0.00``"""

class XLDateAmbiguous(XLDateError):
    """The 1900 leap-year problem ``(datemode == 0 and 1.0 <= xldate < 61.0)``"""

class XLDateTooLarge(XLDateError):
    """Gregorian year 10000 or later"""

class XLDateBadDatemode(XLDateError):
    """``datemode`` arg is neither 0 nor 1"""

class XLDateBadTuple(XLDateError): ...

# 0: 1900-based, 1: 1904-based.
def xldate_as_tuple(xldate: float, datemode: Literal[0, 1]) -> tuple[int, int, int, int, int, int]:
    """
    Convert an Excel number (presumed to represent a date, a datetime or a time) into
    a tuple suitable for feeding to datetime or mx.DateTime constructors.

    :param xldate: The Excel number
    :param datemode: 0: 1900-based, 1: 1904-based.
    :raises xlrd.xldate.XLDateNegative:
    :raises xlrd.xldate.XLDateAmbiguous:

    :raises xlrd.xldate.XLDateTooLarge:
    :raises xlrd.xldate.XLDateBadDatemode:
    :raises xlrd.xldate.XLDateError:
    :returns: Gregorian ``(year, month, day, hour, minute, nearest_second)``.

    .. warning::

      When using this function to interpret the contents of a workbook, you
      should pass in the :attr:`~xlrd.book.Book.datemode`
      attribute of that workbook. Whether the workbook has ever been anywhere
      near a Macintosh is irrelevant.

    .. admonition:: Special case

        If ``0.0 <= xldate < 1.0``, it is assumed to represent a time;
        ``(0, 0, 0, hour, minute, second)`` will be returned.

    .. note::

        ``1904-01-01`` is not regarded as a valid date in the ``datemode==1``
        system; its "serial number" is zero.
    """

def xldate_as_datetime(xldate: float, datemode: Literal[0, 1]) -> datetime.datetime:
    """
    Convert an Excel date/time number into a :class:`datetime.datetime` object.

    :param xldate: The Excel number
    :param datemode: 0: 1900-based, 1: 1904-based.

    :returns: A :class:`datetime.datetime` object.
    """

def _leap(y: int) -> Literal[0, 1]: ...
def xldate_from_date_tuple(date_tuple: tuple[int, int, int], datemode: Literal[0, 1]) -> float:
    """
    Convert a date tuple (year, month, day) to an Excel date.

    :param year: Gregorian year.
    :param month: ``1 <= month <= 12``
    :param day: ``1 <= day <= last day of that (year, month)``
    :param datemode: 0: 1900-based, 1: 1904-based.
    :raises xlrd.xldate.XLDateAmbiguous:
    :raises xlrd.xldate.XLDateBadDatemode:
    :raises xlrd.xldate.XLDateBadTuple:
      ``(year, month, day)`` is too early/late or has invalid component(s)
    :raises xlrd.xldate.XLDateError:
    """

def xldate_from_time_tuple(time_tuple: tuple[int, int, int]) -> float:
    """
    Convert a time tuple ``(hour, minute, second)`` to an Excel "date" value
    (fraction of a day).

    :param hour: ``0 <= hour < 24``
    :param minute: ``0 <= minute < 60``
    :param second: ``0 <= second < 60``
    :raises xlrd.xldate.XLDateBadTuple: Out-of-range hour, minute, or second
    """

def xldate_from_datetime_tuple(datetime_tuple: tuple[int, int, int, int, int, int], datemode: Literal[0, 1]) -> float:
    """
    Convert a datetime tuple ``(year, month, day, hour, minute, second)`` to an
    Excel date value.
    For more details, refer to other xldate_from_*_tuple functions.

    :param datetime_tuple: ``(year, month, day, hour, minute, second)``
    :param datemode: 0: 1900-based, 1: 1904-based.
    """
