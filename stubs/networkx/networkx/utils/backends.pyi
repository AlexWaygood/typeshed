from _typeshed import Incomplete
from collections.abc import Callable, Mapping
from typing import Any, Final, Generic, TypeVar, overload
from typing_extensions import ParamSpec, Self

_P = ParamSpec("_P")
_R = TypeVar("_R")
__all__ = ["_dispatchable"]
FAILED_TO_CONVERT: Final[str]

class _dispatchable(Generic[_P, _R]):
    __defaults__: Incomplete
    __kwdefaults__: Incomplete
    __module__: Incomplete
    __qualname__: Incomplete
    __wrapped__: Incomplete
    orig_func: Callable[_P, _R] | None
    name: str
    edge_attrs: dict[str, Any] | None
    node_attrs: dict[str, Any] | None
    preserve_edge_attrs: bool
    preserve_node_attrs: bool
    preserve_graph_attrs: bool
    mutates_input: bool
    optional_graphs: Incomplete
    list_graphs: Incomplete
    graphs: dict[str, int]
    backends: dict[str, Incomplete]
    # Incomplete: Ignoring the case where func=None returns a partial,
    # we only care about `_dispatchable` used as a static-typing decorator
    def __new__(
        cls,
        func: Callable[_P, _R] | None = None,
        *,
        name: str | None = None,
        graphs: str | None | Mapping[str, int] = "G",
        edge_attrs: str | dict[str, Any] | None = None,
        node_attrs: str | dict[str, Any] | None = None,
        preserve_edge_attrs: bool = False,
        preserve_node_attrs: bool = False,
        preserve_graph_attrs: bool = False,
        preserve_all_attrs: bool = False,
        mutates_input: bool = False,
        returns_graph: bool = False,
        implemented_by_nx: bool = True,
    ) -> Self:
        """A decorator function that is used to redirect the execution of ``func``
        function to its backend implementation.

        This decorator allows the function to dispatch to different backend
        implementations based on the input graph types, and also manages the
        extra keywords ``backend`` and ``**backend_kwargs``.
        Usage can be any of the following decorator forms:

        - ``@_dispatchable``
        - ``@_dispatchable()``
        - ``@_dispatchable(name="override_name")``
        - ``@_dispatchable(graphs="graph_var_name")``
        - ``@_dispatchable(edge_attrs="weight")``
        - ``@_dispatchable(graphs={"G": 0, "H": 1}, edge_attrs={"weight": "default"})``
            with 0 and 1 giving the position in the signature function for graph
            objects. When ``edge_attrs`` is a dict, keys are keyword names and values
            are defaults.

        Parameters
        ----------
        func : callable, optional (default: None)
            The function to be decorated. If None, ``_dispatchable`` returns a
            partial object that can be used to decorate a function later. If ``func``
            is a callable, returns a new callable object that dispatches to a backend
            function based on input graph types.

        name : str, optional (default: name of `func`)
            The name for the function as used for dispatching. If not provided,
            the name of ``func`` will be used. ``name`` is useful to avoid name
            conflicts, as all dispatched functions live in a single namespace.
            For example, ``nx.tournament.is_strongly_connected`` had a name
            conflict with the standard ``nx.is_strongly_connected``, so we used
            ``@_dispatchable(name="tournament_is_strongly_connected")``.

        graphs : str or dict or None, optional (default: "G")
            If a string, the parameter name of the graph, which must be the first
            argument of the wrapped function. If more than one graph is required
            for the function (or if the graph is not the first argument), provide
            a dict keyed by graph parameter name to the value parameter position.
            A question mark in the name indicates an optional argument.
            For example, ``@_dispatchable(graphs={"G": 0, "auxiliary?": 4})``
            indicates the 0th parameter ``G`` of the function is a required graph,
            and the 4th parameter ``auxiliary?`` is an optional graph.
            To indicate that an argument is a list of graphs, do ``"[graphs]"``.
            Use ``graphs=None``, if *no* arguments are NetworkX graphs such as for
            graph generators, readers, and conversion functions.

        edge_attrs : str or dict, optional (default: None)
            ``edge_attrs`` holds information about edge attribute arguments
            and default values for those edge attributes.
            If a string, ``edge_attrs`` holds the function argument name that
            indicates a single edge attribute to include in the converted graph.
            The default value for this attribute is 1. To indicate that an argument
            is a list of attributes (all with default value 1), use e.g. ``"[attrs]"``.
            If a dict, ``edge_attrs`` holds a dict keyed by argument names, with
            values that are either the default value or, if a string, the argument
            name that indicates the default value.
            If None, function does not use edge attributes.

        node_attrs : str or dict, optional
            Like ``edge_attrs``, but for node attributes.

        preserve_edge_attrs : bool or str or dict, optional (default: False)
            If bool, whether to preserve all edge attributes.
            If a string, the parameter name that may indicate (with ``True`` or a
            callable argument) whether all edge attributes should be preserved
            when converting graphs to a backend graph type.
            If a dict of form ``{graph_name: {attr: default}}``, indicate
            pre-determined edge attributes (and defaults) to preserve for the
            indicated input graph.

        preserve_node_attrs : bool or str or dict, optional (default: False)
            Like ``preserve_edge_attrs``, but for node attributes.

        preserve_graph_attrs : bool or set, optional (default: False)
            If bool, whether to preserve all graph attributes.
            If set, which input graph arguments to preserve graph attributes.

        preserve_all_attrs : bool, optional (default: False)
            Whether to preserve all edge, node and graph attributes.
            If True, this overrides all the other preserve_*_attrs.

        mutates_input : bool or dict, optional (default: False)
            If bool, whether the function mutates an input graph argument.
            If dict of ``{arg_name: arg_pos}``, name and position of bool arguments
            that indicate whether an input graph will be mutated, and ``arg_name``
            may begin with ``"not "`` to negate the logic (for example, ``"not copy"``
            means we mutate the input graph when the ``copy`` argument is False).
            By default, dispatching doesn't convert input graphs to a different
            backend for functions that mutate input graphs.

        returns_graph : bool, optional (default: False)
            Whether the function can return or yield a graph object. By default,
            dispatching doesn't convert input graphs to a different backend for
            functions that return graphs.

        implemented_by_nx : bool, optional (default: True)
            Whether the function is implemented by NetworkX. If it is not, then the
            function is included in NetworkX only as an API to dispatch to backends.
            Default is True.
        """

    @property
    def __doc__(self):
        """If the cached documentation exists, it is returned.
        Otherwise, the documentation is generated using _make_doc() method,
        cached, and then returned.
        """

    @__doc__.setter
    def __doc__(self, val) -> None: ...
    @property
    def __signature__(self):
        """Return the signature of the original function, with the addition of
        the `backend` and `backend_kwargs` parameters.
        """
    # Type system limitations doesn't allow us to define this as it truly should.
    # But specifying backend with backend_kwargs isn't a common usecase anyway
    # and specifying backend as explicitely None is possible but not intended.
    # If this ever changes, update stubs/networkx/@tests/test_cases/check_dispatch_decorator.py
    @overload
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        """Returns the result of the original function (no backends installed)."""

    @overload
    def __call__(self, *args: Any, backend: str, **backend_kwargs: Any) -> _R: ...
    # @overload
    # def __call__(self, *args: _P.args, backend: None = None, **kwargs: _P.kwargs) -> _R: ...
    # @overload
    # def __call__(self, *args: _P.args, backend: str, **kwargs: _P.kwargs, **backend_kwargs: Any) -> _R: ...
    def __reduce__(self):
        """Allow this object to be serialized with pickle.

        This uses the global registry `_registered_algorithms` to deserialize.
        """
