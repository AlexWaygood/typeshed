from datetime import date
from typing_extensions import Self

__tracebackhide__: bool

class DateMixin:
    """Date and time assertions mixin."""

    def is_before(self, other: date) -> Self:
        """Asserts that val is a date and is before other date.

        Args:
            other: the other date, expected to be after val

        Examples:
            Usage::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(yesterday).is_before(today)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** before the given date
        """

    def is_after(self, other: date) -> Self:
        """Asserts that val is a date and is after other date.

        Args:
            other: the other date, expected to be before val

        Examples:
            Usage::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(today).is_after(yesterday)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** after the given date
        """

    def is_equal_to_ignoring_milliseconds(self, other: date) -> Self:
        """Asserts that val is a date and is equal to other date to the second.

        Args:
            other: the other date, expected to be equal to the second

        Examples:
            Usage::

                import datetime

                d1 = datetime.datetime(2020, 1, 2, 3, 4, 5, 6)       # 2020-01-02 03:04:05.000006
                d2 = datetime.datetime(2020, 1, 2, 3, 4, 5, 777777)  # 2020-01-02 03:04:05.777777

                assert_that(d1).is_equal_to_ignoring_milliseconds(d2)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** equal to the given date to the second
        """

    def is_equal_to_ignoring_seconds(self, other: date) -> Self:
        """Asserts that val is a date and is equal to other date to the minute.

        Args:
            other: the other date, expected to be equal to the minute

        Examples:
            Usage::

                import datetime

                d1 = datetime.datetime(2020, 1, 2, 3, 4, 5)   # 2020-01-02 03:04:05
                d2 = datetime.datetime(2020, 1, 2, 3, 4, 55)  # 2020-01-02 03:04:55

                assert_that(d1).is_equal_to_ignoring_seconds(d2)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** equal to the given date to the minute
        """

    def is_equal_to_ignoring_time(self, other: date) -> Self:
        """Asserts that val is a date and is equal to other date ignoring time.

        Args:
            other: the other date, expected to be equal ignoring time

        Examples:
            Usage::

                import datetime

                d1 = datetime.datetime(2020, 1, 2, 3, 4, 5)     # 2020-01-02 03:04:05
                d2 = datetime.datetime(2020, 1, 2, 13, 44, 55)  # 2020-01-02 13:44:55

                assert_that(d1).is_equal_to_ignoring_time(d2)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** equal to the given date ignoring time
        """
