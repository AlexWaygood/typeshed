def format_timezone(utcoffset: int) -> str:
    """
    Return a string representing the timezone offset.
    Remaining seconds are rounded to the nearest minute.

    >>> format_timezone(3600)
    '+01:00'
    >>> format_timezone(5400)
    '+01:30'
    >>> format_timezone(-28800)
    '-08:00'

    """
