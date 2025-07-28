"""Jeff Bauer's lightweight date class, extended by us.  Predates Python's datetime module."""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

def getStdMonthNames(): ...
def getStdShortMonthNames(): ...
def getStdDayNames(): ...
def getStdShortDayNames(): ...
def isLeapYear(year):
    """determine if specified year is leap year, returns Python boolean"""

class NormalDateException(Exception):
    """Exception class for NormalDate"""

class NormalDate:
    """
    NormalDate is a specialized class to handle dates without
    all the excess baggage (time zones, daylight savings, leap
    seconds, etc.) of other date structures.  The minimalist
    strategy greatly simplifies its implementation and use.

    Internally, NormalDate is stored as an integer with values
    in a discontinuous range of -99990101 to 99991231.  The
    integer value is used principally for storage and to simplify
    the user interface.  Internal calculations are performed by
    a scalar based on Jan 1, 1900.

    Valid NormalDate ranges include (-9999,1,1) B.C.E. through
    (9999,12,31) C.E./A.D.


    1.0
        No changes, except the version number.  After 3 years of use by
        various parties I think we can consider it stable.

    0.8
        Added Prof. Stephen Walton's suggestion for a range method
         - module author resisted the temptation to use lambda <0.5 wink>

    0.7
        Added Dan Winkler's suggestions for __add__, __sub__ methods

    0.6
        Modifications suggested by Kevin Digweed to fix:
         - dayOfWeek, dayOfWeekAbbrev, clone methods
         - Permit NormalDate to be a better behaved superclass

    0.5
        Minor tweaking

    0.4
         - Added methods __cmp__, __hash__
         - Added Epoch variable, scoped to the module
         - Added setDay, setMonth, setYear methods

    0.3
        Minor touch-ups

    0.2
         - Fixed bug for certain B.C.E leap years
         - Added Jim Fulton's suggestions for short alias class name =ND
           and __getstate__, __setstate__ methods

    Special thanks:  Roedy Green
    """

    def __init__(self, normalDate=None) -> None:
        """
        Accept 1 of 4 values to initialize a NormalDate:
            1. None - creates a NormalDate for the current day
            2. integer in yyyymmdd format
            3. string in yyyymmdd format
            4. tuple in (yyyy, mm, dd) - localtime/gmtime can also be used
            5. string iso date format see _iso_re above
            6. datetime.datetime or datetime.date
        """

    def add(self, days) -> None:
        """add days to date; use negative integers to subtract"""

    def __add__(self, days):
        """add integer to normalDate and return a new, calculated value"""

    def __radd__(self, days):
        """for completeness"""

    def clone(self):
        """return a cloned instance of this normalDate"""

    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __ge__(self, other): ...
    def __gt__(self, other): ...
    def day(self):
        """return the day as integer 1-31"""

    def dayOfWeek(self):
        """return integer representing day of week, Mon=0, Tue=1, etc."""

    @property
    def __day_of_week_name__(self): ...
    def dayOfWeekAbbrev(self):
        """return day of week abbreviation for current date: Mon, Tue, etc."""

    def dayOfWeekName(self):
        """return day of week name for current date: Monday, Tuesday, etc."""

    def dayOfYear(self):
        """day of year"""

    def daysBetweenDates(self, normalDate):
        """
        return value may be negative, since calculation is
        self.scalar() - arg
        """

    def equals(self, target): ...
    def endOfMonth(self):
        """returns (cloned) last day of month"""

    def firstDayOfMonth(self):
        """returns (cloned) first day of month"""

    def formatUS(self):
        """return date as string in common US format: MM/DD/YY"""

    def formatUSCentury(self):
        """return date as string in 4-digit year US format: MM/DD/YYYY"""

    def formatMS(self, fmt):
        """format like MS date using the notation
        {YY}    --> 2 digit year
        {YYYY}  --> 4 digit year
        {M}     --> month as digit
        {MM}    --> 2 digit month
        {MMM}   --> abbreviated month name
        {MMMM}  --> monthname
        {MMMMM} --> first character of monthname
        {D}     --> day of month as digit
        {DD}    --> 2 digit day of month
        {DDD}   --> abrreviated weekday name
        {DDDD}  --> weekday name
        """

    def __hash__(self): ...
    def __int__(self) -> int: ...
    def isLeapYear(self):
        """
        determine if specified year is leap year, returning true (1) or
        false (0)
        """

    def lastDayOfMonth(self):
        """returns last day of the month as integer 28-31"""

    def localeFormat(self):
        """override this method to use your preferred locale format"""

    def month(self):
        """returns month as integer 1-12"""

    @property
    def __month_name__(self): ...
    def monthAbbrev(self):
        """returns month as a 3-character abbreviation, i.e. Jan, Feb, etc."""

    def monthName(self):
        """returns month name, i.e. January, February, etc."""

    def normalize(self, scalar) -> None:
        """convert scalar to normalDate"""

    def range(self, days):
        """Return a range of normalDates as a list.  Parameter
        may be an int or normalDate.
        """

    def scalar(self):
        """days since baseline date: Jan 1, 1900"""

    def setDay(self, day) -> None:
        """set the day of the month"""

    def setMonth(self, month) -> None:
        """set the month [1-12]"""
    normalDate: Incomplete
    def setNormalDate(self, normalDate) -> None:
        """
        accepts date as scalar string/integer (yyyymmdd) or tuple
        (year, month, day, ...)
        """

    def setYear(self, year) -> None: ...
    def __sub__(self, v): ...
    def __rsub__(self, v): ...
    def toTuple(self):
        """return date as (year, month, day) tuple"""

    def year(self):
        """return year in yyyy format, negative values indicate B.C."""

def bigBang():
    """return lower boundary as a NormalDate"""

def bigCrunch():
    """return upper boundary as a NormalDate"""

def dayOfWeek(y, m, d):
    """return integer representing day of week, Mon=0, Tue=1, etc."""

def firstDayOfYear(year):
    """number of days to the first of the year, relative to Jan 1, 1900"""

def FND(d):
    """convert to ND if required"""

Epoch: Incomplete
ND = NormalDate
BDEpoch: Incomplete
BDEpochScalar: int

class BusinessDate(NormalDate):
    """
    Specialised NormalDate
    """

    def add(self, days) -> None:
        """add days to date; use negative integers to subtract"""

    def __add__(self, days):
        """add integer to BusinessDate and return a new, calculated value"""

    def __sub__(self, v): ...
    def asNormalDate(self): ...
    def daysBetweenDates(self, normalDate): ...
    def normalize(self, i) -> None: ...
    def scalar(self): ...
    def setNormalDate(self, normalDate) -> None: ...
