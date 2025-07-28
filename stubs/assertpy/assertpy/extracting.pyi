from collections.abc import Callable, Iterable as _Iterable, Mapping
from typing import Any
from typing_extensions import Self

__tracebackhide__: bool

class ExtractingMixin:
    """Collection flattening mixin.

    It is often necessary to test collections of objects.  Use the ``extracting()`` helper to
    reduce the collection on a given attribute.  Reduce a list of objects::

        alice = Person('Alice', 'Alpha')
        bob = Person('Bob', 'Bravo')
        people = [alice, bob]

        assert_that(people).extracting('first_name').is_equal_to(['Alice', 'Bob'])
        assert_that(people).extracting('first_name').contains('Alice', 'Bob')
        assert_that(people).extracting('first_name').does_not_contain('Charlie')

    Additionally, the ``extracting()`` helper can accept a list of attributes to be extracted, and
    will flatten them into a list of tuples.  Reduce a list of objects on multiple attributes::

        assert_that(people).extracting('first_name', 'last_name').contains(('Alice', 'Alpha'), ('Bob', 'Bravo'))

    Also, ``extracting()`` works on not just attributes, but also properties, and even
    zero-argument methods.  Reduce a list of object on properties and zero-arg methods::

        assert_that(people).extracting('name').contains('Alice Alpha', 'Bob Bravo')
        assert_that(people).extracting('say_hello').contains('Hello, Alice!', 'Hello, Bob!')

    And ``extracting()`` even works on *dict-like* objects.  Reduce a list of dicts on key::

        alice = {'first_name': 'Alice', 'last_name': 'Alpha'}
        bob = {'first_name': 'Bob', 'last_name': 'Bravo'}
        people = [alice, bob]

        assert_that(people).extracting('first_name').contains('Alice', 'Bob')

    **Filtering**

    The ``extracting()`` helper can include a *filter* to keep only those items for which the given
    *filter* is truthy.  For example::

        users = [
            {'user': 'Alice', 'age': 36, 'active': True},
            {'user': 'Bob', 'age': 40, 'active': False},
            {'user': 'Charlie', 'age': 13, 'active': True}
        ]

        # filter the active users
        assert_that(users).extracting('user', filter='active').is_equal_to(['Alice', 'Charlie'])

    The *filter* can be a *dict-like* object and the extracted items are kept if and only if all
    corresponding key-value pairs are equal::

        assert_that(users).extracting('user', filter={'active': False}).is_equal_to(['Bob'])
        assert_that(users).extracting('user', filter={'age': 36, 'active': True}).is_equal_to(['Alice'])

    Or a *filter* can be any function (including an in-line ``lambda``) that accepts as its single
    argument each item in the collection, and the extracted items are kept if the function
    evaluates to ``True``::

        assert_that(users).extracting('user', filter=lambda x: x['age'] > 20)
            .is_equal_to(['Alice', 'Bob'])

    **Sorting**

    The ``extracting()`` helper can include a *sort* to enforce order on the extracted items.

    The *sort* can be the name of a key (or attribute, or property, or zero-argument method) and
    the extracted items are ordered by the corresponding values::

        assert_that(users).extracting('user', sort='age').is_equal_to(['Charlie', 'Alice', 'Bob'])

    The *sort* can be an ``iterable`` of names and the extracted items are ordered by
    corresponding value of the first name, ties are broken by the corresponding values of the
    second name, and so on::

        assert_that(users).extracting('user', sort=['active', 'age']).is_equal_to(['Bob', 'Charlie', 'Alice'])

    The *sort* can be any function (including an in-line ``lambda``) that accepts as its single
    argument each item in the collection, and the extracted items are ordered by the corresponding
    function return values::

        assert_that(users).extracting('user', sort=lambda x: -x['age']).is_equal_to(['Bob', 'Alice', 'Charlie'])
    """

    def extracting(
        self,
        *names: str,
        filter: str | Mapping[str, Any] | Callable[[Any], bool] = ...,
        sort: str | _Iterable[str] | Callable[[Any], Any] = ...,
    ) -> Self:
        """Asserts that val is iterable, then extracts the named attributes, properties, or
        zero-arg methods into a list (or list of tuples if multiple names are given).

        Args:
            *names: the attribute to be extracted (or property or zero-arg method)
            **kwargs: see below

        Keyword Args:
            filter: extract only those items where filter is truthy
            sort: order the extracted items by the sort key

        Examples:
            Usage::

                alice = User('Alice', 20, True)
                bob = User('Bob', 30, False)
                charlie = User('Charlie', 10, True)
                users = [alice, bob, charlie]

                assert_that(users).extracting('user').contains('Alice', 'Bob', 'Charlie')

            Works with *dict-like* objects too::

                users = [
                    {'user': 'Alice', 'age': 20, 'active': True},
                    {'user': 'Bob', 'age': 30, 'active': False},
                    {'user': 'Charlie', 'age': 10, 'active': True}
                ]

                assert_that(people).extracting('user').contains('Alice', 'Bob', 'Charlie')

            Filter::

                assert_that(users).extracting('user', filter='active').is_equal_to(['Alice', 'Charlie'])

            Sort::

                assert_that(users).extracting('user', sort='age').is_equal_to(['Charlie', 'Alice', 'Bob'])

        Returns:
            AssertionBuilder: returns a new instance (now with the extracted list as the val) to chain to the next assertion
        """
