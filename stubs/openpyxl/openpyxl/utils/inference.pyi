"""
Type inference functions
"""

from re import Pattern
from typing import Final

PERCENT_REGEX: Final[Pattern[str]]
TIME_REGEX: Final[Pattern[str]]
NUMBER_REGEX: Final[Pattern[str]]

def cast_numeric(value):
    """Explicitly convert a string to a numeric value"""

def cast_percentage(value):
    """Explicitly convert a string to numeric value and format as a
    percentage
    """

def cast_time(value):
    """Explicitly convert a string to a number and format as datetime or
    time
    """
