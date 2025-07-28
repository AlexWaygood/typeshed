from datetime import date
from typing_extensions import Self, TypeAlias

__tracebackhide__: bool

_Numeric: TypeAlias = date | int | float

class NumericMixin:
    """Numeric assertions mixin."""

    def is_zero(self) -> Self:
        """Asserts that val is numeric and is zero.

        Examples:
            Usage::

                assert_that(0).is_zero()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** zero
        """

    def is_not_zero(self) -> Self:
        """Asserts that val is numeric and is *not* zero.

        Examples:
            Usage::

                assert_that(1).is_not_zero()
                assert_that(123.4).is_not_zero()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** zero
        """

    def is_nan(self) -> Self:
        """Asserts that val is real number and is ``NaN`` (not a number).

        Examples:
            Usage::

                assert_that(float('nan')).is_nan()
                assert_that(float('inf') * 0).is_nan()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** NaN
        """

    def is_not_nan(self) -> Self:
        """Asserts that val is real number and is *not* ``NaN`` (not a number).

        Examples:
            Usage::

                assert_that(0).is_not_nan()
                assert_that(123.4).is_not_nan()
                assert_that(float('inf')).is_not_nan()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** NaN
        """

    def is_inf(self) -> Self:
        """Asserts that val is real number and is ``Inf`` (infinity).

        Examples:
            Usage::

                assert_that(float('inf')).is_inf()
                assert_that(float('inf') * 1).is_inf()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** Inf
        """

    def is_not_inf(self) -> Self:
        """Asserts that val is real number and is *not* ``Inf`` (infinity).

        Examples:
            Usage::

                assert_that(0).is_not_inf()
                assert_that(123.4).is_not_inf()
                assert_that(float('nan')).is_not_inf()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** Inf
        """

    def is_greater_than(self, other: _Numeric) -> Self:
        """Asserts that val is numeric and is greater than other.

        Args:
            other: the other date, expected to be less than val

        Examples:
            Usage::

                assert_that(1).is_greater_than(0)
                assert_that(123.4).is_greater_than(111.1)

            For dates, behavior is identical to :meth:`~assertpy.date.DateMixin.is_after`::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(today).is_greater_than(yesterday)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** greater than other
        """

    def is_greater_than_or_equal_to(self, other: _Numeric) -> Self:
        """Asserts that val is numeric and is greater than or equal to other.

        Args:
            other: the other date, expected to be less than or equal to val

        Examples:
            Usage::

                assert_that(1).is_greater_than_or_equal_to(0)
                assert_that(1).is_greater_than_or_equal_to(1)
                assert_that(123.4).is_greater_than_or_equal_to(111.1)

            For dates, behavior is identical to :meth:`~assertpy.date.DateMixin.is_after` *except* when equal::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(today).is_greater_than_or_equal_to(yesterday)
                assert_that(today).is_greater_than_or_equal_to(today)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** greater than or equal to other
        """

    def is_less_than(self, other: _Numeric) -> Self:
        """Asserts that val is numeric and is less than other.

        Args:
            other: the other date, expected to be greater than val

        Examples:
            Usage::

                assert_that(0).is_less_than(1)
                assert_that(123.4).is_less_than(555.5)

            For dates, behavior is identical to :meth:`~assertpy.date.DateMixin.is_before`::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(yesterday).is_less_than(today)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** less than other
        """

    def is_less_than_or_equal_to(self, other: _Numeric) -> Self:
        """Asserts that val is numeric and is less than or equal to other.

        Args:
            other: the other date, expected to be greater than or equal to val

        Examples:
            Usage::

                assert_that(1).is_less_than_or_equal_to(0)
                assert_that(1).is_less_than_or_equal_to(1)
                assert_that(123.4).is_less_than_or_equal_to(100.0)

            For dates, behavior is identical to :meth:`~assertpy.date.DateMixin.is_before` *except* when equal::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(yesterday).is_less_than_or_equal_to(today)
                assert_that(today).is_less_than_or_equal_to(today)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** less than or equal to other
        """

    def is_positive(self) -> Self:
        """Asserts that val is numeric and is greater than zero.

        Examples:
            Usage::

                assert_that(1).is_positive()
                assert_that(123.4).is_positive()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** positive
        """

    def is_negative(self) -> Self:
        """Asserts that val is numeric and is less than zero.

        Examples:
            Usage::

                assert_that(-1).is_negative()
                assert_that(-123.4).is_negative()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** negative
        """

    def is_between(self, low: _Numeric, high: _Numeric) -> Self:
        """Asserts that val is numeric and is between low and high.

        Args:
            low: the low value
            high: the high value

        Examples:
            Usage::

                assert_that(1).is_between(0, 2)
                assert_that(123.4).is_between(111.1, 222.2)

            For dates, works as expected::

                import datetime

                today = datetime.datetime.now()
                middle = today - datetime.timedelta(hours=12)
                yesterday = today - datetime.timedelta(days=1)

                assert_that(middle).is_between(yesterday, today)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** between low and high
        """

    def is_not_between(self, low: _Numeric, high: _Numeric) -> Self:
        """Asserts that val is numeric and is *not* between low and high.

        Args:
            low: the low value
            high: the high value

        Examples:
            Usage::

                assert_that(1).is_not_between(2, 3)
                assert_that(1.1).is_not_between(2.2, 3.3)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** between low and high
        """

    def is_close_to(self, other: _Numeric, tolerance: _Numeric) -> Self:
        """Asserts that val is numeric and is close to other within tolerance.

        Args:
            other: the other value, expected to be close to val within tolerance
            tolerance: the tolerance

        Examples:
            Usage::

                assert_that(123).is_close_to(100, 25)
                assert_that(123.4).is_close_to(123, 0.5)

            For dates, works as expected::

                import datetime

                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)

                assert_that(today).is_close_to(yesterday, datetime.timedelta(hours=36))

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** close to other within tolerance
        """

    def is_not_close_to(self, other: _Numeric, tolerance: _Numeric) -> Self:
        """Asserts that val is numeric and is *not* close to other within tolerance.

        Args:
            other: the other value
            tolerance: the tolerance

        Examples:
            Usage::

                assert_that(123).is_not_close_to(100, 22)
                assert_that(123.4).is_not_close_to(123, 0.1)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** close to other within tolerance
        """
