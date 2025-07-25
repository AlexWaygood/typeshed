from typing import Any, overload

class Singleton(type):
    """
    Singleton metaclass
    Based on Python Cookbook 3rd Edition Recipe 9.13
    Only one instance of a class can exist. Does not work with __slots__
    """

    @overload
    def __init__(self, o: object, /) -> None: ...
    @overload
    def __init__(self, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any) -> None: ...
    def __call__(self, *args: Any, **kwds: Any) -> Any: ...

class Cached(type):
    """
    Caching metaclass
    Child classes will only create new instances of themselves if
    one doesn't already exist. Does not work with __slots__
    """

    @overload
    def __init__(self, o: object, /) -> None: ...
    @overload
    def __init__(self, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any) -> None: ...
    def __call__(self, *args: Any) -> Any: ...
