from collections.abc import Callable
from typing import Any
from typing_extensions import Self

__tracebackhide__: bool

class CollectionMixin:
    """Collection assertions mixin."""

    def is_iterable(self) -> Self:
        """Asserts that val is iterable collection.

        Examples:
            Usage::

                assert_that('foo').is_iterable()
                assert_that(['a', 'b']).is_iterable()
                assert_that((1, 2, 3)).is_iterable()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** iterable
        """

    def is_not_iterable(self) -> Self:
        """Asserts that val is not iterable collection.

        Examples:
            Usage::

                assert_that(1).is_not_iterable()
                assert_that(123.4).is_not_iterable()
                assert_that(True).is_not_iterable()
                assert_that(None).is_not_iterable()

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **is** iterable
        """

    def is_subset_of(self, *supersets: Any) -> Self:
        """Asserts that val is iterable and a subset of the given superset (or supersets).

        Args:
            *supersets: the expected superset (or supersets)

        Examples:
            Usage::

                assert_that('foo').is_subset_of('abcdefghijklmnopqrstuvwxyz')
                assert_that(['a', 'b']).is_subset_of(['a', 'b', 'c'])
                assert_that((1, 2, 3)).is_subset_of([1, 2, 3, 4])
                assert_that({'a': 1, 'b': 2}).is_subset_of({'a': 1, 'b': 2, 'c': 3})
                assert_that({'a', 'b'}).is_subset_of({'a', 'b', 'c'})

                # or multiple supersets (as comma-separated args)
                assert_that('aBc').is_subset_of('abc', 'ABC')
                assert_that((1, 2, 3)).is_subset_of([1, 3, 5], [2, 4, 6])

                assert_that({'a': 1, 'b': 2}).is_subset_of({'a': 1, 'c': 3})  # fails
                # Expected <{'a': 1, 'b': 2}> to be subset of <{'a': 1, 'c': 3}>, but <{'b': 2}> was missing.

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** subset of given superset (or supersets)
        """

    def is_sorted(self, key: Callable[[Any], Any] = ..., reverse: bool = False) -> Self:
        """Asserts that val is iterable and is sorted.

        Args:
            key (function): the one-arg function to extract the sort comparison key.  Defaults to
                ``lambda x: x`` to just compare items directly.
            reverse (bool): if ``True``, then comparison key is reversed.  Defaults to ``False``.

        Examples:
            Usage::

                assert_that(['a', 'b', 'c']).is_sorted()
                assert_that((1, 2, 3)).is_sorted()

                # with a key function
                assert_that('aBc').is_sorted(key=str.lower)

                # reverse order
                assert_that(['c', 'b', 'a']).is_sorted(reverse=True)
                assert_that((3, 2, 1)).is_sorted(reverse=True)

                assert_that((1, 2, 3, 4, -5, 6)).is_sorted()  # fails
                # Expected <(1, 2, 3, 4, -5, 6)> to be sorted, but subset <4, -5> at index 3 is not.

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val is **not** sorted
        """
