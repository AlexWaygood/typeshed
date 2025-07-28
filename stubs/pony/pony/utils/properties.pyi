from _typeshed import Incomplete

class cached_property:
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """

    func: Incomplete
    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls): ...

class class_property:
    """
    Read-only class property
    """

    func: Incomplete
    def __init__(self, func) -> None: ...
    def __get__(self, instance, cls): ...

class class_cached_property:
    func: Incomplete
    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls): ...
