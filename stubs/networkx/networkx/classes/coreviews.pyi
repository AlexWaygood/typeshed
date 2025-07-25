"""Views of core data structures such as nested Mappings (e.g. dict-of-dicts).
These ``Views`` often restrict element access, with either the entire view or
layers of nested mappings being read-only.
"""

from collections.abc import Callable, Iterator, Mapping
from typing import TypeVar
from typing_extensions import Self

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")

__all__ = [
    "AtlasView",
    "AdjacencyView",
    "MultiAdjacencyView",
    "UnionAtlas",
    "UnionAdjacency",
    "UnionMultiInner",
    "UnionMultiAdjacency",
    "FilterAtlas",
    "FilterAdjacency",
    "FilterMultiInner",
    "FilterMultiAdjacency",
]

class AtlasView(Mapping[_T, dict[_U, _V]]):
    """An AtlasView is a Read-only Mapping of Mappings.

    It is a View into a dict-of-dict data structure.
    The inner level of dict is read-write. But the
    outer level is read-only.

    See Also
    ========
    AdjacencyView: View into dict-of-dict-of-dict
    MultiAdjacencyView: View into dict-of-dict-of-dict-of-dict
    """

    def __getstate__(self) -> dict[str, Mapping[_T, dict[_U, _V]]]: ...
    def __setstate__(self, state: dict[str, Mapping[_T, dict[_U, _V]]]) -> None: ...
    def __init__(self, d: Mapping[_T, dict[_U, _V]]) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, key: _T) -> dict[_U, _V]: ...
    def copy(self) -> dict[_T, dict[_U, _V]]: ...

class AdjacencyView(AtlasView[_T, _U, _V]):
    """An AdjacencyView is a Read-only Map of Maps of Maps.

    It is a View into a dict-of-dict-of-dict data structure.
    The inner level of dict is read-write. But the
    outer levels are read-only.

    See Also
    ========
    AtlasView: View into dict-of-dict
    MultiAdjacencyView: View into dict-of-dict-of-dict-of-dict
    """

class MultiAdjacencyView(AdjacencyView[_T, _U, _V]):
    """An MultiAdjacencyView is a Read-only Map of Maps of Maps of Maps.

    It is a View into a dict-of-dict-of-dict-of-dict data structure.
    The inner level of dict is read-write. But the
    outer levels are read-only.

    See Also
    ========
    AtlasView: View into dict-of-dict
    AdjacencyView: View into dict-of-dict-of-dict
    """

class UnionAtlas(Mapping[_T, dict[_U, _V]]):
    """A read-only union of two atlases (dict-of-dict).

    The two dict-of-dicts represent the inner dict of
    an Adjacency:  `G.succ[node]` and `G.pred[node]`.
    The inner level of dict of both hold attribute key:value
    pairs and is read-write. But the outer level is read-only.

    See Also
    ========
    UnionAdjacency: View into dict-of-dict-of-dict
    UnionMultiAdjacency: View into dict-of-dict-of-dict-of-dict
    """

    def __init__(self, succ: AtlasView[_T, _U, _V], pred: AtlasView[_T, _U, _V]) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, key: _T) -> dict[_U, _V]: ...
    def copy(self) -> Self: ...

class UnionAdjacency(Mapping[_T, dict[_U, _V]]):
    """A read-only union of dict Adjacencies as a Map of Maps of Maps.

    The two input dict-of-dict-of-dicts represent the union of
    `G.succ` and `G.pred`. Return values are UnionAtlas
    The inner level of dict is read-write. But the
    middle and outer levels are read-only.

    succ : a dict-of-dict-of-dict {node: nbrdict}
    pred : a dict-of-dict-of-dict {node: nbrdict}
    The keys for the two dicts should be the same

    See Also
    ========
    UnionAtlas: View into dict-of-dict
    UnionMultiAdjacency: View into dict-of-dict-of-dict-of-dict
    """

    def __init__(self, succ: AdjacencyView[_T, _U, _V], pred: AdjacencyView[_T, _U, _V]) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, key: _T) -> dict[_U, _V]: ...
    def copy(self) -> Self: ...

class UnionMultiInner(UnionAtlas[_T, _U, _V]):
    """A read-only union of two inner dicts of MultiAdjacencies.

    The two input dict-of-dict-of-dicts represent the union of
    `G.succ[node]` and `G.pred[node]` for MultiDiGraphs.
    Return values are UnionAtlas.
    The inner level of dict is read-write. But the outer levels are read-only.

    See Also
    ========
    UnionAtlas: View into dict-of-dict
    UnionAdjacency:  View into dict-of-dict-of-dict
    UnionMultiAdjacency:  View into dict-of-dict-of-dict-of-dict
    """

class UnionMultiAdjacency(UnionAdjacency[_T, _U, _V]):
    """A read-only union of two dict MultiAdjacencies.

    The two input dict-of-dict-of-dict-of-dicts represent the union of
    `G.succ` and `G.pred` for MultiDiGraphs. Return values are UnionAdjacency.
    The inner level of dict is read-write. But the outer levels are read-only.

    See Also
    ========
    UnionAtlas:  View into dict-of-dict
    UnionMultiInner:  View into dict-of-dict-of-dict
    """

class FilterAtlas(Mapping[_T, _U]):
    """A read-only Mapping of Mappings with filtering criteria for nodes.

    It is a view into a dict-of-dict data structure, and it selects only
    nodes that meet the criteria defined by ``NODE_OK``.

    See Also
    ========
    FilterAdjacency
    FilterMultiInner
    FilterMultiAdjacency
    """

    NODE_OK: Callable[[_T], bool]
    def __init__(self, d: Mapping[_T, _U], NODE_OK: Callable[[_T], bool]) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, key: _T) -> _U: ...

class FilterAdjacency(Mapping[_T, Mapping[_U, _V]]):
    """A read-only Mapping of Mappings with filtering criteria for nodes and edges.

    It is a view into a dict-of-dict-of-dict data structure, and it selects nodes
    and edges that satisfy specific criteria defined by ``NODE_OK`` and ``EDGE_OK``,
    respectively.

    See Also
    ========
    FilterAtlas
    FilterMultiInner
    FilterMultiAdjacency
    """

    NODE_OK: Callable[[_T], bool]
    EDGE_OK: Callable[[_T, _T], bool]
    def __init__(
        self, d: Mapping[_T, Mapping[_U, _V]], NODE_OK: Callable[[_T], bool], EDGE_OK: Callable[[_T, _T], bool]
    ) -> None: ...
    def __len__(self): ...
    def __iter__(self): ...
    def __getitem__(self, node: _T) -> FilterAtlas[_U, _V]: ...

class FilterMultiInner(FilterAdjacency[_T, _U, _V]):
    """A read-only Mapping of Mappings with filtering criteria for nodes and edges.

    It is a view into a dict-of-dict-of-dict-of-dict data structure, and it selects nodes
    and edges that meet specific criteria defined by ``NODE_OK`` and ``EDGE_OK``.

    See Also
    ========
    FilterAtlas
    FilterAdjacency
    FilterMultiAdjacency
    """

class FilterMultiAdjacency(FilterAdjacency[_T, _U, _V]):
    """A read-only Mapping of Mappings with filtering criteria
    for nodes and edges.

    It is a view into a dict-of-dict-of-dict-of-dict data structure,
    and it selects nodes and edges that satisfy specific criteria
    defined by ``NODE_OK`` and ``EDGE_OK``, respectively.

    See Also
    ========
    FilterAtlas
    FilterAdjacency
    FilterMultiInner
    """
