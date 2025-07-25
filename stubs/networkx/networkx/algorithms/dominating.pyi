"""Functions for computing dominating sets in a graph."""

from collections.abc import Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["dominating_set", "is_dominating_set", "connected_dominating_set", "is_connected_dominating_set"]

@_dispatchable
def dominating_set(G: Graph[_Node], start_with: _Node | None = None) -> set[_Node]:
    """Finds a dominating set for the graph G.

    A *dominating set* for a graph with node set *V* is a subset *D* of
    *V* such that every node not in *D* is adjacent to at least one
    member of *D* [1]_.

    Parameters
    ----------
    G : NetworkX graph

    start_with : node (default=None)
        Node to use as a starting point for the algorithm.

    Returns
    -------
    D : set
        A dominating set for G.

    Notes
    -----
    This function is an implementation of algorithm 7 in [2]_ which
    finds some dominating set, not necessarily the smallest one.

    See also
    --------
    is_dominating_set

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dominating_set

    .. [2] Abdol-Hossein Esfahanian. Connectivity Algorithms.
        http://www.cse.msu.edu/~cse835/Papers/Graph_connectivity_revised.pdf

    """

@_dispatchable
def is_dominating_set(G: Graph[_Node], nbunch: Iterable[_Node]) -> bool:
    """Checks if `nbunch` is a dominating set for `G`.

    A *dominating set* for a graph with node set *V* is a subset *D* of
    *V* such that every node not in *D* is adjacent to at least one
    member of *D* [1]_.

    Parameters
    ----------
    G : NetworkX graph

    nbunch : iterable
        An iterable of nodes in the graph `G`.

    Returns
    -------
    dominating : bool
        True if `nbunch` is a dominating set of `G`, false otherwise.

    See also
    --------
    dominating_set

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dominating_set

    """

@_dispatchable
def connected_dominating_set(G: Graph[_Node]) -> set[_Node]:
    """Returns a connected dominating set.

    A *dominating set* for a graph *G* with node set *V* is a subset *D* of *V*
    such that every node not in *D* is adjacent to at least one member of *D*
    [1]_. A *connected dominating set* is a dominating set *C* that induces a
    connected subgraph of *G* [2]_.
    Note that connected dominating sets are not unique in general and that there
    may be other connected dominating sets.

    Parameters
    ----------
    G : NewtorkX graph
        Undirected connected graph.

    Returns
    -------
    connected_dominating_set : set
        A dominating set of nodes which induces a connected subgraph of G.

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    NetworkXError
        If G is disconnected.

    Examples
    ________
    >>> G = nx.Graph(
    ...     [
    ...         (1, 2),
    ...         (1, 3),
    ...         (1, 4),
    ...         (1, 5),
    ...         (1, 6),
    ...         (2, 7),
    ...         (3, 8),
    ...         (4, 9),
    ...         (5, 10),
    ...         (6, 11),
    ...         (7, 12),
    ...         (8, 12),
    ...         (9, 12),
    ...         (10, 12),
    ...         (11, 12),
    ...     ]
    ... )
    >>> nx.connected_dominating_set(G)
    {1, 2, 3, 4, 5, 6, 7}

    Notes
    -----
    This function implements Algorithm I in its basic version as described
    in [3]_. The idea behind the algorithm is the following: grow a tree *T*,
    starting from a node with maximum degree. Throughout the growing process,
    nonleaf nodes in *T* are our connected dominating set (CDS), leaf nodes in
    *T* are marked as "seen" and nodes in G that are not yet in *T* are marked as
    "unseen". We maintain a max-heap of all "seen" nodes, and track the number
    of "unseen" neighbors for each node. At each step we pop the heap top -- a
    "seen" (leaf) node with maximal number of "unseen" neighbors, add it to the
    CDS and mark all its "unseen" neighbors as "seen". For each one of the newly
    created "seen" nodes, we also decrement the number of "unseen" neighbors for
    all its neighbors. The algorithm terminates when there are no more "unseen"
    nodes.
    Runtime complexity of this implementation is $O(|E|*log|V|)$ (amortized).

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dominating_set
    .. [2] https://en.wikipedia.org/wiki/Connected_dominating_set
    .. [3] Guha, S. and Khuller, S.
           *Approximation Algorithms for Connected Dominating Sets*,
           Algorithmica, 20, 374-387, 1998.

    """

@_dispatchable
def is_connected_dominating_set(G: Graph[_Node], nbunch: Iterable[_Node]) -> bool:
    """Checks if `nbunch` is a connected dominating set for `G`.

    A *dominating set* for a graph *G* with node set *V* is a subset *D* of
    *V* such that every node not in *D* is adjacent to at least one
    member of *D* [1]_. A *connected dominating set* is a dominating
    set *C* that induces a connected subgraph of *G* [2]_.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph.

    nbunch : iterable
        An iterable of nodes in the graph `G`.

    Returns
    -------
    connected_dominating : bool
        True if `nbunch` is connected dominating set of `G`, false otherwise.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dominating_set
    .. [2] https://en.wikipedia.org/wiki/Connected_dominating_set

    """
