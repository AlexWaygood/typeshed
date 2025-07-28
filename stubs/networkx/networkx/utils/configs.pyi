import sys
from _typeshed import Incomplete
from collections.abc import Callable, ItemsView, Iterable, Iterator, KeysView, ValuesView
from dataclasses import dataclass
from types import TracebackType
from typing_extensions import Self

__all__ = ["Config"]

# TODO: Our pyright test doesn't understand `requires_python` in METADATA.toml
# https://github.com/python/typeshed/issues/14025
if sys.version_info >= (3, 10):
    @dataclass(init=False, eq=False, slots=True, kw_only=True, match_args=False)
    class Config:
        """The base class for NetworkX configuration.

        There are two ways to use this to create configurations. The recommended way
        is to subclass ``Config`` with docs and annotations.

        >>> class MyConfig(Config):
        ...     '''Breakfast!'''
        ...
        ...     eggs: int
        ...     spam: int
        ...
        ...     def _on_setattr(self, key, value):
        ...         assert isinstance(value, int) and value >= 0
        ...         return value
        >>> cfg = MyConfig(eggs=1, spam=5)

        Another way is to simply pass the initial configuration as keyword arguments to
        the ``Config`` instance:

        >>> cfg1 = Config(eggs=1, spam=5)
        >>> cfg1
        Config(eggs=1, spam=5)

        Once defined, config items may be modified, but can't be added or deleted by default.
        ``Config`` is a ``Mapping``, and can get and set configs via attributes or brackets:

        >>> cfg.eggs = 2
        >>> cfg.eggs
        2
        >>> cfg["spam"] = 42
        >>> cfg["spam"]
        42

        For convenience, it can also set configs within a context with the "with" statement:

        >>> with cfg(spam=3):
        ...     print("spam (in context):", cfg.spam)
        spam (in context): 3
        >>> print("spam (after context):", cfg.spam)
        spam (after context): 42

        Subclasses may also define ``_on_setattr`` (as done in the example above)
        to ensure the value being assigned is valid:

        >>> cfg.spam = -1
        Traceback (most recent call last):
            ...
        AssertionError

        If a more flexible configuration object is needed that allows adding and deleting
        configurations, then pass ``strict=False`` when defining the subclass:

        >>> class FlexibleConfig(Config, strict=False):
        ...     default_greeting: str = "Hello"
        >>> flexcfg = FlexibleConfig()
        >>> flexcfg.name = "Mr. Anderson"
        >>> flexcfg
        FlexibleConfig(default_greeting='Hello', name='Mr. Anderson')
        """

        def __init_subclass__(cls, strict: bool = True) -> None: ...
        def __new__(cls, **kwargs) -> Self: ...
        def __dir__(self) -> Iterable[str]: ...
        def __setattr__(self, name: str, value) -> None: ...
        def __delattr__(self, name: str) -> None: ...
        def __contains__(self, key: object) -> bool: ...
        def __iter__(self) -> Iterator[str]: ...
        def __len__(self) -> int: ...
        def __reversed__(self) -> Iterator[str]: ...
        def __getitem__(self, key: str): ...
        def __setitem__(self, key: str, value) -> None: ...
        def __delitem__(self, key: str) -> None: ...
        def get(self, key: str, default=None): ...
        def items(self) -> ItemsView[str, Incomplete]: ...
        def keys(self) -> KeysView[str]: ...
        def values(self) -> ValuesView[Incomplete]: ...
        def __reduce__(self) -> tuple[Callable[..., Self], tuple[type[Self], dict[Incomplete, Incomplete]]]: ...
        def __call__(self, **kwargs) -> Self: ...
        def __enter__(self) -> Self: ...
        def __exit__(
            self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
        ) -> None: ...

else:
    @dataclass(init=False, eq=False)
    class Config:
        def __init_subclass__(cls, strict: bool = True) -> None: ...
        def __new__(cls, **kwargs) -> Self: ...
        def __dir__(self) -> Iterable[str]: ...
        def __setattr__(self, name: str, value) -> None: ...
        def __delattr__(self, name: str) -> None: ...
        def __contains__(self, key: object) -> bool: ...
        def __iter__(self) -> Iterator[str]: ...
        def __len__(self) -> int: ...
        def __reversed__(self) -> Iterator[str]: ...
        def __getitem__(self, key: str): ...
        def __setitem__(self, key: str, value) -> None: ...
        def __delitem__(self, key: str) -> None: ...
        def get(self, key: str, default=None): ...
        def items(self) -> ItemsView[str, Incomplete]: ...
        def keys(self) -> KeysView[str]: ...
        def values(self) -> ValuesView[Incomplete]: ...
        def __reduce__(self) -> tuple[Callable[..., Self], tuple[type[Self], dict[Incomplete, Incomplete]]]: ...
        def __call__(self, **kwargs) -> Self: ...
        def __enter__(self) -> Self: ...
        def __exit__(
            self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
        ) -> None: ...

class NetworkXConfig(Config):
    """Configuration for NetworkX that controls behaviors such as how to use backends.

    Attribute and bracket notation are supported for getting and setting configurations::

        >>> nx.config.backend_priority == nx.config["backend_priority"]
        True

    Parameters
    ----------
    backend_priority : list of backend names or dict or BackendPriorities
        Enable automatic conversion of graphs to backend graphs for functions
        implemented by the backend. Priority is given to backends listed earlier.
        This is a nested configuration with keys ``algos``, ``generators``, and,
        optionally, function names. Setting this value to a list of backend names
        will set ``nx.config.backend_priority.algos``. For more information, see
        ``help(nx.config.backend_priority)``. Default is empty list.

    backends : Config mapping of backend names to backend Config
        The keys of the Config mapping are names of all installed NetworkX backends,
        and the values are their configurations as Config mappings.

    cache_converted_graphs : bool
        If True, then save converted graphs to the cache of the input graph. Graph
        conversion may occur when automatically using a backend from `backend_priority`
        or when using the `backend=` keyword argument to a function call. Caching can
        improve performance by avoiding repeated conversions, but it uses more memory.
        Care should be taken to not manually mutate a graph that has cached graphs; for
        example, ``G[u][v][k] = val`` changes the graph, but does not clear the cache.
        Using methods such as ``G.add_edge(u, v, weight=val)`` will clear the cache to
        keep it consistent. ``G.__networkx_cache__.clear()`` manually clears the cache.
        Default is True.

    fallback_to_nx : bool
        If True, then "fall back" and run with the default "networkx" implementation
        for dispatchable functions not implemented by backends of input graphs. When a
        backend graph is passed to a dispatchable function, the default behavior is to
        use the implementation from that backend if possible and raise if not. Enabling
        ``fallback_to_nx`` makes the networkx implementation the fallback to use instead
        of raising, and will convert the backend graph to a networkx-compatible graph.
        Default is False.

    warnings_to_ignore : set of strings
        Control which warnings from NetworkX are not emitted. Valid elements:

        - `"cache"`: when a cached value is used from ``G.__networkx_cache__``.

    Notes
    -----
    Environment variables may be used to control some default configurations:

    - ``NETWORKX_BACKEND_PRIORITY``: set ``backend_priority.algos`` from comma-separated names.
    - ``NETWORKX_CACHE_CONVERTED_GRAPHS``: set ``cache_converted_graphs`` to True if nonempty.
    - ``NETWORKX_FALLBACK_TO_NX``: set ``fallback_to_nx`` to True if nonempty.
    - ``NETWORKX_WARNINGS_TO_IGNORE``: set `warnings_to_ignore` from comma-separated names.

    and can be used for finer control of ``backend_priority`` such as:

    - ``NETWORKX_BACKEND_PRIORITY_ALGOS``: same as ``NETWORKX_BACKEND_PRIORITY``
      to set ``backend_priority.algos``.

    This is a global configuration. Use with caution when using from multiple threads.
    """

    backend_priority: list[str]
    backends: Config
    cache_converted_graphs: bool
    fallback_to_nx: bool
    warnings_to_ignore: set[str]
    def __init__(
        self,
        *,
        backend_priority: list[str],
        backends: Config,
        cache_converted_graphs: bool,
        fallback_to_nx: bool,
        warnings_to_ignore: set[str],
    ) -> None: ...
    def __new__(
        cls,
        *,
        backend_priority: list[str],
        backends: Config,
        cache_converted_graphs: bool,
        fallback_to_nx: bool,
        warnings_to_ignore: set[str],
    ) -> Self: ...

config: NetworkXConfig
