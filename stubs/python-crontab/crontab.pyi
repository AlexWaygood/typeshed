"""
from crontab import CronTab
import sys

# Create a new non-installed crontab
cron = CronTab(tab='')
job  = cron.new(command='/usr/bin/echo')

job.minute.during(5,50).every(5)
job.hour.every(4)

job.dow.on('SUN')
job.month.during('APR', 'JUN')
job.month.also.during('OCT', 'DEC')

job.every(2).days()
job.setall(1, 12, None, None, None)

job2 = cron.new(command='/foo/bar', comment='SomeID')
job2.every_reboot()

jobs = list(cron.find_command('bar'))
job3 = jobs[0]
job3.clear()
job3.minute.every(1)

sys.stdout.write(str(cron.render()))

job3.enable(False)

for job4 in cron.find_command('echo'):
    sys.stdout.write(job4)

for job5 in cron.find_comment('SomeID'):
    sys.stdout.write(job5)

for job6 in cron:
    sys.stdout.write(job6)

for job7 in cron:
    job7.every(3).hours()
    sys.stdout.write(job7)
    job7.every().dow()

cron.remove_all(command='/foo/bar')
cron.remove_all(comment='This command')
cron.remove_all(time='* * * * *')
cron.remove_all()

output = cron.render()

cron.write()

cron.write(filename='/tmp/output.txt')

#cron.write_to_user(user=True)

#cron.write_to_user(user='root')

# Croniter Extentions allow you to ask for the scheduled job times, make
# sure you have croniter installed, it's not a hard dependancy.

job3.schedule().get_next()
job3.schedule().get_prev()

"""

import re
import subprocess
from _typeshed import Incomplete, StrPath
from builtins import range as _range
from collections import OrderedDict
from collections.abc import Callable, Generator, Iterable, Iterator
from datetime import datetime
from logging import Logger
from types import TracebackType
from typing import Any, Final, Literal, Protocol, SupportsIndex, TypeVar, overload, type_check_only
from typing_extensions import Self, TypeAlias

from croniter.croniter import croniter
from cronlog import CronLog

_User: TypeAlias = str | bool | None
_K = TypeVar("_K")
_V = TypeVar("_V")

# cron_descriptor.Options class
@type_check_only
class _Options(Protocol):
    casing_type: Literal[1, 2, 3]
    verbose: bool
    day_of_week_start_index_zero: bool
    use_24hour_time_format: bool
    locale_location: StrPath | None
    locale_code: str | None
    def __init__(self) -> None: ...

__pkgname__: Final[str]
__version__: Final[str]
ITEMREX: Final[re.Pattern[str]]
SPECREX: Final[re.Pattern[str]]
DEVNULL: Final[str]
WEEK_ENUM: Final[list[str]]
MONTH_ENUM: Final[list[str | None]]
SPECIALS_CONVERSION: Final[bool]
SPECIALS: Final[dict[str, str]]
SPECIAL_IGNORE: Final[list[str]]
S_INFO: Final[list[dict[str, str | int | list[str] | list[str | None]]]]
WINOS: Final[bool]
POSIX: Final[bool]
SYSTEMV: Final[bool]
ZERO_PAD: Final[bool]
LOG: Logger
CRON_COMMAND: Final[str]
SHELL: Final[str]
current_user: Callable[[], str | None]

class Process:
    """Runs a program and orders the arguments for compatability.

    a. keyword args are flags and always appear /before/ arguments for bsd
    """

    env: subprocess._ENV | None
    args: tuple[str, ...]
    has_run: bool
    stdout: str | None
    stderr: str | None
    returncode: int | None
    # `posix` and `env` are known special kwargs:
    def __init__(self, cmd: str, *args: str, posix: bool = ..., env: subprocess._ENV | None = None, **flags: object) -> None: ...
    def run(self) -> Self:
        """Run this process and store whatever is returned"""

    def __int__(self) -> int: ...  # technically, it can return `None` before `run` is called
    def __eq__(self, other: object) -> bool: ...

class CronTab:
    """
    Crontab object which can access any time based cron using the standard.

    user    - Set the user of the crontab (default: None)
      * 'user' = Load from $username's crontab (instead of tab or tabfile)
      * None   = Don't load anything from any user crontab.
      * True   = Load from current $USER's crontab (unix only)
      * False  = This is a system crontab, each command has a username

    tab     - Use a string variable as the crontab instead of installed crontab
    tabfile - Use a file for the crontab instead of installed crontab
    log     - Filename for logfile instead of /var/log/syslog
    """

    lines: list[str | CronItem] | None
    crons: list[CronItem] | None
    filen: str | None
    cron_command: str
    env: OrderedVariableList[Incomplete, Incomplete] | None
    root: bool
    intab: str | None
    tabfile: str | None
    def __init__(
        self, user: _User = ..., tab: str | None = ..., tabfile: str | None = ..., log: CronLog | str | None = ...
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    @property
    def log(self) -> CronLog:
        """Returns the CronLog object for this tab (user or root tab only)"""

    @property
    def user(self) -> _User:
        """Return user's username of this crontab if applicable"""

    @property
    def user_opt(self) -> dict[str, str]:
        """Returns the user option for the crontab commandline"""

    def read(self, filename: str | None = ...) -> None:
        """
        Read in the crontab from the system into the object, called
        automatically when listing or using the object. use for refresh.
        """

    def append(
        self,
        item: CronItem,
        line: str = ...,
        read: bool = ...,
        before: str | re.Pattern[str] | list[CronItem] | tuple[CronItem, ...] | Generator[CronItem] | None = ...,
    ) -> None:
        """Append a CronItem object to this CronTab

        Keyword arguments:
         item   - The CronItem object to append
         line   - The textual line which this item is.
         read   - Internal use only
         before - Append before this CronItem, comment regex or generator
        """

    def write(self, filename: str | None = ..., user: _User = ..., errors: bool = ...) -> None:
        """Write the crontab to it's source or a given filename."""

    def write_to_user(self, user: bool | str = ...) -> None:
        """Write the crontab to a user (or root) instead of a file."""
    # Usually `kwargs` are just `now: datetime | None`, but technically this can
    # work for `CronItem` subclasses, which might define other kwargs.
    def run_pending(self, *, now: datetime | None = ..., **kwargs: Any) -> Iterator[str]:
        """Run all commands in this crontab if pending (generator)"""

    def run_scheduler(self, timeout: int = -1, cadence: int = 60, warp: bool = False) -> Iterator[str]:
        """Run the CronTab as an internal scheduler (generator)"""

    def render(self, errors: bool = ...) -> str:
        """Render this crontab as it would be in the crontab.

        errors - Should we not comment out invalid entries and cause errors?
        """

    def new(
        self,
        command: str = ...,
        comment: str = ...,
        user: str | None = ...,
        pre_comment: bool = ...,
        before: str | re.Pattern[str] | list[CronItem] | tuple[CronItem, ...] | Generator[CronItem] | None = ...,
    ) -> CronItem:
        """
        Create a new CronItem and append it to the cron.

        Keyword arguments:
         command     - The command that will be run.
         comment     - The comment that should be associated with this command.
         user        - For system cron tabs, the user this command should run as.
         pre_comment - If true the comment will apear just before the command line.
         before      - Append this command before this item instead of at the end.

        Returns the new CronItem object.
        """

    def find_command(self, command: str | re.Pattern[str]) -> Iterator[CronItem]:
        """Return an iter of jobs matching any part of the command."""

    def find_comment(self, comment: str | re.Pattern[str]) -> Iterator[CronItem]:
        """Return an iter of jobs that match the comment field exactly."""

    def find_time(self, *args: Any) -> Iterator[CronItem]:
        """Return an iter of jobs that match this time pattern"""

    @property
    def commands(self) -> Iterator[str]:
        """Return a generator of all unqiue commands used in this crontab"""

    @property
    def comments(self) -> Iterator[str]:
        """Return a generator of all unique comments/Id used in this crontab"""
    # You cannot actually pass `*args`, it will raise an exception,
    # also known kwargs are added:
    def remove_all(
        self, *, command: str | re.Pattern[str] = ..., comment: str | re.Pattern[str] = ..., time: Any = ..., **kwargs: object
    ) -> int:
        """Removes all crons using the stated command OR that have the
        stated comment OR removes everything if no arguments specified.

           command - Remove all with this command
           comment - Remove all with this comment or ID
           time    - Remove all with this time code
        """

    def remove(self, *items: CronItem | Iterable[CronItem]) -> int:
        """Remove a selected cron from the crontab."""

    def __iter__(self) -> Iterator[CronItem]:
        """Return generator so we can track jobs after removal"""

    def __getitem__(self, i: SupportsIndex) -> CronItem: ...
    def __len__(self) -> int: ...

class CronItem:
    """
    An item which objectifies a single line of a crontab and
    May be considered to be a cron job object.
    """

    cron: CronTab | None
    user: _User
    valid: bool
    enabled: bool
    special: bool
    comment: str
    command: str | None
    last_run: datetime | None
    env: OrderedVariableList[Incomplete, Incomplete]
    pre_comment: bool
    marker: str | None
    stdin: str | None
    slices: CronSlices
    def __init__(self, command: str = ..., comment: str = ..., user: _User = ..., pre_comment: bool = ...) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    @classmethod
    def from_line(cls, line: str, user: str | None = ..., cron: Incomplete | None = ...) -> Self:
        """Generate CronItem from a cron-line and parse out command and comment"""

    def delete(self) -> None:
        """Delete this item and remove it from it's parent"""

    def set_command(self, cmd: str, parse_stdin: bool = ...) -> None:
        """Set the command and filter as needed"""

    def set_comment(self, cmt: str, pre_comment: bool = ...) -> None:
        """Set the comment and don't filter, pre_comment indicates comment appears
        before the cron, otherwise it appears ont he same line after the command.
        """

    def parse(self, line: str) -> None:
        """Parse a cron line string and save the info as the objects."""

    def enable(self, enabled: bool = ...) -> bool:
        """Set if this cron job is enabled or not"""

    def is_enabled(self) -> bool:
        """Return true if this job is enabled (not commented out)"""

    def is_valid(self) -> bool:
        """Return true if this job is valid"""

    def render(self) -> str:
        """Render this set cron-job to a string"""

    def every_reboot(self) -> None:
        """Set to every reboot instead of a time pattern: @reboot"""

    def every(self, unit: int = ...) -> Every:
        """
        Replace existing time pattern with a single unit, setting all lower
        units to first value in valid range.

        For instance job.every(3).days() will be `0 0 */3 * *`
        while job.day().every(3) would be `* * */3 * *`

        Many of these patterns exist as special tokens on Linux, such as
        `@midnight` and `@hourly`
        """

    def setall(self, *args: Any) -> None:
        """Replace existing time pattern with these five values given as args:

        job.setall("1 2 * * *")
        job.setall(1, 2) == '1 2 * * *'
        job.setall(0, 0, None, '>', 'SUN') == '0 0 * 12 SUN'
        """

    def clear(self) -> None:
        """Clear the special and set values"""

    def frequency(self, year: int | None = ...) -> int:
        """Returns the number of times this item will execute in a given year
        (defaults to this year)
        """

    def frequency_per_year(self, year: int | None = ...) -> int:
        """Returns the number of /days/ this item will execute on in a year
        (defaults to this year)
        """

    def frequency_per_day(self) -> int:
        """Returns the number of time this item will execute in any day"""

    def frequency_per_hour(self) -> int:
        """Returns the number of times this item will execute in any hour"""

    def frequency_at_year(self, year: int | None = None) -> int:
        """Returns the number of times this item will execute in a given year
        (defaults to this year)
        """

    @overload
    def frequency_at_month(self, year: int, month: int) -> int:
        """Returns the number of times this item will execute in a given month
        (defaults to this month)
        """

    @overload
    def frequency_at_month(self, year: None = None, month: None = None) -> int: ...
    @overload
    def frequency_at_day(self, year: int, month: int, day: int) -> int:
        """Returns the number of times this item will execute in a given day
        (defaults to today)
        """

    @overload
    def frequency_at_day(self, year: None = None, month: None = None, day: None = None) -> int: ...
    @overload
    def frequency_at_hour(self, year: int, month: int, day: int, hour: int) -> int:
        """Returns the number of times this item will execute in a given hour
        (defaults to this hour)
        """

    @overload
    def frequency_at_hour(self, year: None = None, month: None = None, day: None = None, hour: None = None) -> int: ...
    def run_pending(self, now: datetime | None = ...) -> int | str:
        """Runs the command if scheduled"""

    def run(self) -> str:
        """Runs the given command as a pipe"""

    def schedule(self, date_from: datetime | None = ...) -> croniter:
        """Return a croniter schedule if available."""

    def description(
        self,
        *,
        options: _Options | None = None,
        casing_type: Literal[1, 2, 3] = 2,
        verbose: bool = False,
        day_of_week_start_index_zero: bool = True,
        use_24hour_time_format: bool = ...,
        locale_location: StrPath | None = None,
        locale_code: str | None = ...,
    ) -> str | None:
        """
        Returns a description of the crontab's schedule (if available)

        **kw - Keyword arguments to pass to cron_descriptor (see docs)
        """

    @property
    def log(self) -> CronLog:
        """Return a cron log specific for this job only"""

    @property
    def minute(self) -> int | str:
        """Return the minute slice"""

    @property
    def minutes(self) -> int | str:
        """Same as minute"""

    @property
    def hour(self) -> int | str:
        """Return the hour slice"""

    @property
    def hours(self) -> int | str:
        """Same as hour"""

    @property
    def day(self) -> int | str:
        """Return the day slice"""

    @property
    def dom(self) -> int | str:
        """Return the day-of-the month slice"""

    @property
    def month(self) -> int | str:
        """Return the month slice"""

    @property
    def months(self) -> int | str:
        """Same as month"""

    @property
    def dow(self) -> int | str:
        """Return the day of the week slice"""

    def __len__(self) -> int: ...
    def __getitem__(self, key: int | str) -> int | str: ...
    def __lt__(self, value: object) -> bool: ...
    def __gt__(self, value: object) -> bool: ...

class Every:
    """Provide an interface to the job.every() method:
     Available Calls:
       minute, minutes, hour, hours, dom, doms, month, months, dow, dows

    Once run all units will be cleared (set to *) then proceeding units
    will be set to '0' and the target unit will be set as every x units.
    """

    slices: CronSlices
    unit: int
    # TODO: add generated attributes
    def __init__(self, item: CronSlices, units: int) -> None: ...
    def set_attr(self, target: int) -> Callable[[], None]:
        """Inner set target, returns function"""

    def year(self) -> None:
        """Special every year target"""

class CronSlices(list[CronSlice]):
    """Controls a list of five time 'slices' which reprisent:
    minute frequency, hour frequency, day of month frequency,
    month requency and finally day of the week frequency.
    """

    special: bool | None
    def __init__(self, *args: Any) -> None: ...
    def is_self_valid(self, *args: Any) -> bool:
        """Object version of is_valid"""

    @classmethod
    def is_valid(cls, *args: Any) -> bool:
        """Returns true if the arguments are valid cron pattern"""

    def setall(self, *slices: str) -> None:
        """Parses the various ways date/time frequency can be specified"""

    def clean_render(self) -> str:
        """Return just numbered parts of this crontab"""

    def render(self) -> str:
        """Return just the first part of a cron job (the numbers or special)"""

    def clear(self) -> None:
        """Clear the special and set values"""

    def frequency(self, year: int | None = ...) -> int:
        """Return frequence per year times frequency per day"""

    def frequency_per_year(self, year: int | None = ...) -> int:
        """Returns the number of times this item will execute
        in a given year (default is this year)
        """

    def frequency_per_day(self) -> int:
        """Returns the number of times this item will execute in any day"""

    def frequency_per_hour(self) -> int:
        """Returns the number of times this item will execute in any hour"""

    def frequency_at_year(self, year: int | None = None) -> int:
        """Returns the number of /days/ this item will execute
        in a given year (default is this year)
        """

    @overload
    def frequency_at_month(self, year: int, month: int) -> int:
        """Returns the number of times this item will execute in given month
        (default: current month)
        """

    @overload
    def frequency_at_month(self, year: None = None, month: None = None) -> int: ...
    @overload
    def frequency_at_day(self, year: int, month: int, day: int) -> int:
        """Returns the number of times this item will execute in a day
        (default: any executed day)
        """

    @overload
    def frequency_at_day(self, year: None = None, month: None = None, day: None = None) -> int: ...
    @overload
    def frequency_at_hour(self, year: int, month: int, day: int, hour: int) -> int:
        """Returns the number of times this item will execute in a hour
        (default: any executed hour)
        """

    @overload
    def frequency_at_hour(self, year: None = None, month: None = None, day: None = None, hour: None = None) -> int: ...
    def __eq__(self, arg: object) -> bool: ...

class SundayError(KeyError):
    """Sunday was specified as 7 instead of 0"""

class Also:
    """Link range values together (appending instead of replacing)"""

    obj: CronSlice
    def __init__(self, obj: CronSlice) -> None: ...
    # These method actually use `*args`, but pass them to `CronSlice` methods,
    # this is why they are typed as `Any`.
    def every(self, *a: Any) -> _Part:
        """Also every one of these"""

    def on(self, *a: Any) -> list[_Part]:
        """Also on these"""

    def during(self, *a: Any) -> _Part:
        """Also during these"""

_Part: TypeAlias = int | CronValue | CronRange

class CronSlice:
    """Cron slice object which shows a time pattern"""

    min: int | None
    max: int | None
    name: str | None
    enum: list[str | None] | None
    parts: list[_Part]
    def __init__(self, info: int | dict[str, Any], value: str | None = ...) -> None: ...
    def __hash__(self) -> int: ...
    def parse(self, value: str | None) -> None:
        """Set values into the slice."""

    def render(self, resolve: bool = False) -> str:
        """Return the slice rendered as a crontab.

        resolve - return integer values instead of enums (default False)

        """

    def __eq__(self, arg: object) -> bool: ...
    def every(self, n_value: int, also: bool = ...) -> _Part:
        """Set the every X units value"""
    # The only known kwarg, others are unused,
    # `*args`` are passed to `parse_value`, so they are `Any`
    def on(self, *n_value: Any, also: bool = ...) -> list[_Part]:
        """Set the time values to the specified placements."""

    def during(self, vfrom: int | str, vto: int | str, also: bool = ...) -> _Part:
        """Set the During value, which sets a range"""

    @property
    def also(self) -> Also:
        """Appends rather than replaces the new values"""

    def clear(self) -> None:
        """clear the slice ready for new vaues"""

    def get_range(self, *vrange: int | str | CronValue) -> list[int | CronRange]:
        """Return a cron range for this slice"""

    def __iter__(self) -> Iterator[int]:
        """Return the entire element as an iterable"""

    def __len__(self) -> int:
        """Returns the number of times this slice happens in it's range"""

    def parse_value(self, val: str, sunday: int | None = ...) -> int | CronValue:
        """Parse the value of the cron slice and raise any errors needed"""

    def test_value(self, value: str, sunday: int | None = None) -> str:
        """Test the value is within range for this slice"""

def get_cronvalue(value: int, enums: list[str]) -> int | CronValue:
    """Returns a value as int (pass-through) or a special enum value"""

class CronValue:
    """Represent a special value in the cron line"""

    text: str
    value: int
    def __init__(self, value: str, enums: list[str]) -> None: ...
    def __lt__(self, value: object) -> bool: ...
    def __int__(self) -> int: ...

class CronRange:
    """A range between one value and another for a time range."""

    dangling: int | None
    slice: str
    cron: CronTab | None
    seq: int
    def __init__(self, vslice: str, *vrange: int | str | CronValue) -> None: ...
    # Are not set in `__init__`:
    vfrom: int | CronValue
    vto: int | CronValue
    def parse(self, value: str) -> None:
        """Parse a ranged value in a cronjob"""

    def all(self) -> None:
        """Set this slice to all units between the miniumum and maximum"""

    def render(self, resolve: bool = ...) -> str:
        """Render the ranged value for a cronjob"""

    def range(self) -> _range:
        """Returns the range of this cron slice as a iterable list"""

    def every(self, value: int | str) -> None:
        """Set the sequence value for this range."""

    def __lt__(self, value: object) -> bool: ...
    def __gt__(self, value: object) -> bool: ...
    def __int__(self) -> int: ...

class OrderedVariableList(OrderedDict[_K, _V]):
    """An ordered dictionary with a linked list containing
    the previous OrderedVariableList which this list depends.

    Duplicates in this list are weeded out in favour of the previous
    list in the chain.

    This is all in aid of the ENV variables list which must exist one
    per job in the chain.
    """

    job: CronItem | None
    # You cannot actually pass `*args`, it will raise an exception,
    # also known kwargs are added:
    def __init__(self, *, job: CronItem | None = None, **kw: _V) -> None: ...
    @property
    def previous(self) -> Self | None:
        """Returns the previous env in the list of jobs in the cron"""

    def all(self) -> Self:
        """
        Returns the full dictionary, everything from this dictionary
        plus all those in the chain above us.
        """

    def __getitem__(self, key: _K) -> _V: ...
