from datetime import datetime

def parse(timestamp: str, utc: bool = False, produce_naive: bool = False) -> datetime:
    """
    Parse an :RFC:`3339`-formatted timestamp and return a
    :class:`datetime.datetime`.

    If the timestamp is presented in UTC, then the `tzinfo` parameter of the
    returned `datetime` will be set to :attr:`datetime.timezone.utc`.

    >>> parse('2009-01-01T10:01:02Z')
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    Otherwise, a :class:`datetime.timezone` instance is created with the appropriate offset, and
    the `tzinfo` parameter of the returned `datetime` is set to that value.

    >>> parse('2009-01-01T14:01:02-04:00')
    datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000), '<UTC-04:00>'))

    However, if `parse()`  is called with `utc=True`, then the returned
    `datetime` will be normalized to UTC (and its tzinfo parameter set to
    `datetime.timezone.utc`), regardless of the input timezone.

    >>> parse('2009-01-01T06:01:02-04:00', utc=True)
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    The input is strictly required to conform to :RFC:`3339`, and appropriate
    exceptions are thrown for invalid input.

    >>> parse('2009-01-01T06:01:02')
    Traceback (most recent call last):
    ...
    ValueError: timestamp does not conform to RFC 3339

    >>> parse('2009-01-01T25:01:02Z')
    Traceback (most recent call last):
    ...
    ValueError: hour must be in 0..23

    """
