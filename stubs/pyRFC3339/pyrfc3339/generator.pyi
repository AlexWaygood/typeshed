from datetime import datetime

def generate(dt: datetime, utc: bool = True, accept_naive: bool = False, microseconds: bool = False) -> str:
    """
    Generate an :RFC:`3339`-formatted timestamp from a
    :class:`datetime.datetime`.

    >>> from datetime import datetime, timezone
    >>> from zoneinfo import ZoneInfo
    >>> generate(datetime(2009, 1, 1, 12, 59, 59, 0, timezone.utc))
    '2009-01-01T12:59:59Z'

    The timestamp will use UTC unless `utc=False` is specified, in which case
    it will use the timezone from the :class:`datetime.datetime`'s
    :attr:`tzinfo` parameter.

    >>> eastern = ZoneInfo('US/Eastern')
    >>> dt = datetime(2009, 1, 1, 12, 59, 59, tzinfo=eastern)
    >>> generate(dt)
    '2009-01-01T17:59:59Z'
    >>> generate(dt, utc=False)
    '2009-01-01T12:59:59-05:00'

    Unless `accept_naive=True` is specified, the `datetime` must not be naive.

    >>> generate(datetime(2009, 1, 1, 12, 59, 59, 0))
    Traceback (most recent call last):
    ...
    ValueError: naive datetime and accept_naive is False

    >>> generate(datetime(2009, 1, 1, 12, 59, 59, 0), accept_naive=True)
    '2009-01-01T12:59:59Z'

    If `accept_naive=True` is specified, the `datetime` is assumed to be UTC.
    Attempting to generate a local timestamp from a naive datetime will result
    in an error.

    >>> generate(datetime(2009, 1, 1, 12, 59, 59, 0), accept_naive=True, utc=False)
    Traceback (most recent call last):
    ...
    ValueError: cannot generate a local timestamp from a naive datetime

    """
