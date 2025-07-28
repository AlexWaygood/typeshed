from typing_extensions import Self

unicode = str
__tracebackhide__: bool

class StringMixin:
    """String assertions mixin."""

    def is_equal_to_ignoring_case(self, other: str) -> Self:
        """Asserts that val is a string and is case-insensitive equal to other.

        Checks actual is equal to expected using the ``==`` operator and ``str.lower()``.

        Args:
            other: the expected value

        Examples:
            Usage::

                assert_that('foo').is_equal_to_ignoring_case('FOO')
                assert_that('FOO').is_equal_to_ignoring_case('foo')
                assert_that('fOo').is_equal_to_ignoring_case('FoO')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if actual is **not** case-insensitive equal to expected
        """

    def contains_ignoring_case(self, *items: str) -> Self:
        """Asserts that val is string and contains the given item or items.

        Walks val and checks for item or items using the ``==`` operator and ``str.lower()``.

        Args:
            *items: the item or items expected to be contained

        Examples:
            Usage::

                assert_that('foo').contains_ignoring_case('F', 'oO')
                assert_that(['a', 'B']).contains_ignoring_case('A', 'b')
                assert_that({'a': 1, 'B': 2}).contains_ignoring_case('A', 'b')
                assert_that({'a', 'B'}).contains_ignoring_case('A', 'b')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain the case-insensitive item or items
        """

    def starts_with(self, prefix: str) -> Self:
        """Asserts that val is string or iterable and starts with prefix.

        Args:
            prefix: the prefix

        Examples:
            Usage::

                assert_that('foo').starts_with('fo')
                assert_that(['a', 'b', 'c']).starts_with('a')
                assert_that((1, 2, 3)).starts_with(1)
                assert_that(((1, 2), (3, 4), (5, 6))).starts_with((1, 2))

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** start with prefix
        """

    def ends_with(self, suffix: str) -> Self:
        """Asserts that val is string or iterable and ends with suffix.

        Args:
            suffix: the suffix

        Examples:
            Usage::

                assert_that('foo').ends_with('oo')
                assert_that(['a', 'b', 'c']).ends_with('c')
                assert_that((1, 2, 3)).ends_with(3)
                assert_that(((1, 2), (3, 4), (5, 6))).ends_with((5, 6))

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** end with suffix
        """

    def matches(self, pattern: str) -> Self:
        """Asserts that val is string and matches the given regex pattern.

        Args:
            pattern (str): the regular expression pattern, as raw string (aka prefixed with ``r``)

        Examples:
            Usage::

                assert_that('foo').matches(r'\\w')
                assert_that('123-456-7890').matches(r'\\d{3}-\\d{3}-\\d{4}')

            Match is partial unless anchored, so these assertion pass::

                assert_that('foo').matches(r'\\w')
                assert_that('foo').matches(r'oo')
                assert_that('foo').matches(r'\\w{2}')

            To match the entire string, just use an anchored regex pattern where ``^`` and ``$``
            match the start and end of line and ``\\A`` and ``\\Z`` match the start and end of string::

                assert_that('foo').matches(r'^\\w{3}$')
                assert_that('foo').matches(r'\\A\\w{3}\\Z')

            And regex flags, such as ``re.MULTILINE`` and ``re.DOTALL``, can only be applied via
            *inline modifiers*, such as ``(?m)`` and ``(?s)``::

                s = '''bar
                foo
                baz'''

                # using multiline (?m)
                assert_that(s).matches(r'(?m)^foo$')

                # using dotall (?s)
                assert_that(s).matches(r'(?s)b(.*)z')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** match pattern

        Tip:
            Regular expressions are tricky.  Be sure to use raw strings (aka prefixed with ``r``).
            Also, note that the :meth:`matches` assertion passes for partial matches (as does the
            underlying ``re.match`` method).  So, if you need to match the entire string, you must
            include anchors in the regex pattern.
        """

    def does_not_match(self, pattern: str) -> Self:
        """Asserts that val is string and does not match the given regex pattern.

        Args:
            pattern (str): the regular expression pattern, as raw string (aka prefixed with ``r``)

        Examples:
            Usage::

                assert_that('foo').does_not_match(r'\\d+')
                assert_that('123').does_not_match(r'\\w+')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** match pattern

        See Also:
            :meth:`matches` - for more about regex patterns
        """

    def is_alpha(self) -> Self:
        """Asserts that val is non-empty string and all characters are alphabetic (using ``str.isalpha()``).

        Examples:
            Usage::

                assert_that('foo').is_lower()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** lowercase
        """

    def is_digit(self) -> Self:
        """Asserts that val is non-empty string and all characters are digits (using ``str.isdigit()``).

        Examples:
            Usage::

                assert_that('1234567890').is_digit()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** digits
        """

    def is_lower(self) -> Self:
        """Asserts that val is non-empty string and all characters are lowercase (using ``str.lower()``).

        Examples:
            Usage::

                assert_that('foo').is_lower()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** lowercase
        """

    def is_upper(self) -> Self:
        """Asserts that val is non-empty string and all characters are uppercase (using ``str.upper()``).

        Examples:
            Usage::

                assert_that('FOO').is_upper()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** uppercase
        """

    def is_unicode(self) -> Self:
        """Asserts that val is a unicode string.

        Examples:
            Usage::

                assert_that(u'foo').is_unicode()  # python 2
                assert_that('foo').is_unicode()   # python 3

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** a unicode string
        """
