from typing import Any
from typing_extensions import Self

__tracebackhide__: bool

class ContainsMixin:
    """Containment assertions mixin."""

    def contains(self, *items: Any) -> Self:
        """Asserts that val contains the given item or items.

        Checks if the collection contains the given item or items using ``in`` operator.

        Args:
            *items: the item or items expected to be contained

        Examples:
            Usage::

                assert_that('foo').contains('f')
                assert_that('foo').contains('f', 'oo')
                assert_that(['a', 'b']).contains('b', 'a')
                assert_that((1, 2, 3)).contains(3, 2, 1)
                assert_that({'a': 1, 'b': 2}).contains('b', 'a')  # checks keys
                assert_that({'a', 'b'}).contains('b', 'a')
                assert_that([1, 2, 3]).is_type_of(list).contains(1, 2).does_not_contain(4, 5)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain the item or items

        Tip:
            Use the :meth:`~assertpy.dict.DictMixin.contains_key` alias when working with
            *dict-like* objects to be self-documenting.

        See Also:
            :meth:`~assertpy.string.StringMixin.contains_ignoring_case` - for case-insensitive string contains
        """

    def does_not_contain(self, *items: Any) -> Self:
        """Asserts that val does not contain the given item or items.

        Checks if the collection excludes the given item or items using ``in`` operator.

        Args:
            *items: the item or items expected to be excluded

        Examples:
            Usage::

                assert_that('foo').does_not_contain('x')
                assert_that(['a', 'b']).does_not_contain('x', 'y')
                assert_that((1, 2, 3)).does_not_contain(4, 5)
                assert_that({'a': 1, 'b': 2}).does_not_contain('x', 'y')  # checks keys
                assert_that({'a', 'b'}).does_not_contain('x', 'y')
                assert_that([1, 2, 3]).is_type_of(list).contains(1, 2).does_not_contain(4, 5)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** contain the item or items

        Tip:
            Use the :meth:`~assertpy.dict.DictMixin.does_not_contain_key` alias when working with
            *dict-like* objects to be self-documenting.
        """

    def contains_only(self, *items: Any) -> Self:
        """Asserts that val contains *only* the given item or items.

        Checks if the collection contains only the given item or items using ``in`` operator.

        Args:
            *items: the *only* item or items expected to be contained

        Examples:
            Usage::

                assert_that('foo').contains_only('f', 'o')
                assert_that(['a', 'a', 'b']).contains_only('a', 'b')
                assert_that((1, 1, 2)).contains_only(1, 2)
                assert_that({'a': 1, 'a': 2, 'b': 3}).contains_only('a', 'b')
                assert_that({'a', 'a', 'b'}).contains_only('a', 'b')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val contains anything **not** item or items
        """

    def contains_sequence(self, *items: Any) -> Self:
        """Asserts that val contains the given ordered sequence of items.

        Checks if the collection contains the given sequence of items using ``in`` operator.

        Args:
            *items: the sequence of items expected to be contained

        Examples:
            Usage::

                assert_that('foo').contains_sequence('f', 'o')
                assert_that('foo').contains_sequence('o', 'o')
                assert_that(['a', 'b', 'c']).contains_sequence('b', 'c')
                assert_that((1, 2, 3)).contains_sequence(1, 2)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contains the given sequence of items
        """

    def contains_duplicates(self) -> Self:
        """Asserts that val is iterable and *does* contain duplicates.

        Examples:
            Usage::

                assert_that('foo').contains_duplicates()
                assert_that(['a', 'a', 'b']).contains_duplicates()
                assert_that((1, 1, 2)).contains_duplicates()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain any duplicates
        """

    def does_not_contain_duplicates(self) -> Self:
        """Asserts that val is iterable and *does not* contain any duplicates.

        Examples:
            Usage::

                assert_that('fox').does_not_contain_duplicates()
                assert_that(['a', 'b', 'c']).does_not_contain_duplicates()
                assert_that((1, 2, 3)).does_not_contain_duplicates()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** contain duplicates
        """

    def is_empty(self) -> Self:
        """Asserts that val is empty.

        Examples:
            Usage::

                assert_that('').is_empty()
                assert_that([]).is_empty()
                assert_that(()).is_empty()
                assert_that({}).is_empty()
                assert_that(set()).is_empty()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** empty
        """

    def is_not_empty(self) -> Self:
        """Asserts that val is *not* empty.

        Examples:
            Usage::

                assert_that('foo').is_not_empty()
                assert_that(['a', 'b']).is_not_empty()
                assert_that((1, 2, 3)).is_not_empty()
                assert_that({'a': 1, 'b': 2}).is_not_empty()
                assert_that({'a', 'b'}).is_not_empty()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** empty
        """

    def is_in(self, *items: Any) -> Self:
        """Asserts that val is equal to one of the given items.

        Args:
            *items: the items expected to contain val

        Examples:
            Usage::

                assert_that('foo').is_in('foo', 'bar', 'baz')
                assert_that(1).is_in(0, 1, 2, 3)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** in the given items
        """

    def is_not_in(self, *items: Any) -> Self:
        """Asserts that val is not equal to one of the given items.

        Args:
            *items: the items expected to exclude val

        Examples:
            Usage::

                assert_that('foo').is_not_in('bar', 'baz', 'box')
                assert_that(1).is_not_in(-1, -2, -3)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** in the given items
        """
