from collections.abc import Callable
from typing_extensions import Self

__tracebackhide__: bool

class DynamicMixin:
    """Dynamic assertions mixin.

    When testing attributes of an object (or the contents of a dict), the
    :meth:`~assertpy.base.BaseMixin.is_equal_to` assertion can be a bit verbose::

        fred = Person('Fred', 'Smith')

        assert_that(fred.first_name).is_equal_to('Fred')
        assert_that(fred.name).is_equal_to('Fred Smith')
        assert_that(fred.say_hello()).is_equal_to('Hello, Fred!')

    Instead, use dynamic assertions in the form of ``has_<name>()`` where ``<name>`` is the name of
    any attribute, property, or zero-argument method on the given object. Dynamic equality
    assertions test if actual is equal to expected using the ``==`` operator. Using dynamic
    assertions, we can rewrite the above example as::

        assert_that(fred).has_first_name('Fred')
        assert_that(fred).has_name('Fred Smith')
        assert_that(fred).has_say_hello('Hello, Fred!')

    Similarly, dynamic assertions also work on any *dict-like* object::

        fred = {
            'first_name': 'Fred',
            'last_name': 'Smith',
            'shoe_size': 12
        }

        assert_that(fred).has_first_name('Fred')
        assert_that(fred).has_last_name('Smith')
        assert_that(fred).has_shoe_size(12)
    """

    def __getattr__(self, attr: str) -> Callable[..., Self]:
        """Asserts that val has attribute attr and that its value is equal to other via a dynamic
        assertion of the form ``has_<attr>()``.
        """
