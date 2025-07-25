from typing import Any
from typing_extensions import Self

__tracebackhide__: bool

class DictMixin:
    """Dict assertions mixin."""

    def contains_key(self, *keys: Any) -> Self:
        """Asserts the val is a dict and contains the given key or keys.  Alias for :meth:`~assertpy.contains.ContainsMixin.contains`.

        Checks if the dict contains the given key or keys using ``in`` operator.

        Args:
            *keys: the key or keys expected to be contained

        Examples:
            Usage::

                assert_that({'a': 1, 'b': 2}).contains_key('a')
                assert_that({'a': 1, 'b': 2}).contains_key('a', 'b')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain the key or keys
        """

    def does_not_contain_key(self, *keys: Any) -> Self:
        """Asserts the val is a dict and does not contain the given key or keys.  Alias for :meth:`~assertpy.contains.ContainsMixin.does_not_contain`.

        Checks if the dict excludes the given key or keys using ``in`` operator.

        Args:
            *keys: the key or keys expected to be excluded

        Examples:
            Usage::

                assert_that({'a': 1, 'b': 2}).does_not_contain_key('x')
                assert_that({'a': 1, 'b': 2}).does_not_contain_key('x', 'y')

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** contain the key or keys
        """

    def contains_value(self, *values: Any) -> Self:
        """Asserts that val is a dict and contains the given value or values.

        Checks if the dict contains the given value or values in *any* key.

        Args:
            *values: the value or values expected to be contained

        Examples:
            Usage::

                assert_that({'a': 1, 'b': 2}).contains_value(1)
                assert_that({'a': 1, 'b': 2}).contains_value(1, 2)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain the value or values
        """

    def does_not_contain_value(self, *values: Any) -> Self:
        """Asserts that val is a dict and does not contain the given value or values.

        Checks if the dict excludes the given value or values across *all* keys.

        Args:
            *values: the value or values expected to be excluded

        Examples:
            Usage::

                assert_that({'a': 1, 'b': 2}).does_not_contain_value(3)
                assert_that({'a': 1, 'b': 2}).does_not_contain_value(3, 4)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** contain the value or values
        """

    def contains_entry(self, *args: Any, **kwargs: dict[str, Any]) -> Self:
        """Asserts that val is a dict and contains the given entry or entries.

        Checks if the dict contains the given key-value pair or pairs.

        Args:
            *args: the entry or entries expected to be contained (as ``{k: v}`` args)
            **kwargs: the entry or entries expected to be contained (as ``k=v`` kwargs)

        Examples:
            Usage::

                # using args
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry({'a': 1})
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry({'a': 1}, {'b': 2})
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry({'a': 1}, {'b': 2}, {'c': 3})

                # using kwargs
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry(a=1)
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry(a=1, b=2)
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry(a=1, b=2, c=3)

                # or args and kwargs
                assert_that({'a': 1, 'b': 2, 'c': 3}).contains_entry({'c': 3}, a=1, b=2)


        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val does **not** contain the entry or entries
        """

    def does_not_contain_entry(self, *args: Any, **kwargs: dict[str, Any]) -> Self:
        """Asserts that val is a dict and does not contain the given entry or entries.

        Checks if the dict excludes the given key-value pair or pairs.

        Args:
            *args: the entry or entries expected to be excluded (as ``{k: v}`` args)
            **kwargs: the entry or entries expected to be excluded (as ``k=v`` kwargs)

        Examples:
            Usage::

                # using args
                assert_that({'a': 1, 'b': 2, 'c': 3}).does_not_contain_entry({'a': 2})
                assert_that({'a': 1, 'b': 2, 'c': 3}).does_not_contain_entry({'a': 2}, {'x': 4})

                # using kwargs
                assert_that({'a': 1, 'b': 2, 'c': 3}).does_not_contain_entry(a=2)
                assert_that({'a': 1, 'b': 2, 'c': 3}).does_not_contain_entry(a=2, x=4)

        Returns:
            AssertionBuilder: returns this instance to chain to the next assertion

        Raises:
            AssertionError: if val **does** contain the entry or entries
        """
