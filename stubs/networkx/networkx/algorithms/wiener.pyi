"""Functions related to the Wiener Index of a graph.

The Wiener Index is a topological measure of a graph
related to the distance between nodes and their degree.
The Schultz Index and Gutman Index are similar measures.
They are used categorize molecules via the network of
atoms connected by chemical bonds. The indices are
correlated with functional aspects of the molecules.

References
----------
.. [1] `Wikipedia: Wiener Index <https://en.wikipedia.org/wiki/Wiener_index>`_
.. [2] M.V. Diudeaa and I. Gutman, Wiener-Type Topological Indices,
       Croatica Chemica Acta, 71 (1998), 21-51.
       https://hrcak.srce.hr/132323
"""

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["wiener_index", "schultz_index", "gutman_index"]

@_dispatchable
def wiener_index(G: Graph[_Node], weight: str | None = None) -> float:
    """Returns the Wiener index of the given graph.

    The *Wiener index* of a graph is the sum of the shortest-path
    (weighted) distances between each pair of reachable nodes.
    For pairs of nodes in undirected graphs, only one orientation
    of the pair is counted.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or None, optional (default: None)
        If None, every edge has weight 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        The edge weights are used to computing shortest-path distances.

    Returns
    -------
    number
        The Wiener index of the graph `G`.

    Raises
    ------
    NetworkXError
        If the graph `G` is not connected.

    Notes
    -----
    If a pair of nodes is not reachable, the distance is assumed to be
    infinity. This means that for graphs that are not
    strongly-connected, this function returns ``inf``.

    The Wiener index is not usually defined for directed graphs, however
    this function uses the natural generalization of the Wiener index to
    directed graphs.

    Examples
    --------
    The Wiener index of the (unweighted) complete graph on *n* nodes
    equals the number of pairs of the *n* nodes, since each pair of
    nodes is at distance one::

        >>> n = 10
        >>> G = nx.complete_graph(n)
        >>> nx.wiener_index(G) == n * (n - 1) / 2
        True

    Graphs that are not strongly-connected have infinite Wiener index::

        >>> G = nx.empty_graph(2)
        >>> nx.wiener_index(G)
        inf

    References
    ----------
    .. [1] `Wikipedia: Wiener Index <https://en.wikipedia.org/wiki/Wiener_index>`_
    """

@_dispatchable
def schultz_index(G, weight=None) -> float:
    """Returns the Schultz Index (of the first kind) of `G`

    The *Schultz Index* [3]_ of a graph is the sum over all node pairs of
    distances times the sum of degrees. Consider an undirected graph `G`.
    For each node pair ``(u, v)`` compute ``dist(u, v) * (deg(u) + deg(v)``
    where ``dist`` is the shortest path length between two nodes and ``deg``
    is the degree of a node.

    The Schultz Index is the sum of these quantities over all (unordered)
    pairs of nodes.

    Parameters
    ----------
    G : NetworkX graph
        The undirected graph of interest.
    weight : string or None, optional (default: None)
        If None, every edge has weight 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        The edge weights are used to computing shortest-path distances.

    Returns
    -------
    number
        The first kind of Schultz Index of the graph `G`.

    Examples
    --------
    The Schultz Index of the (unweighted) complete graph on *n* nodes
    equals the number of pairs of the *n* nodes times ``2 * (n - 1)``,
    since each pair of nodes is at distance one and the sum of degree
    of two nodes is ``2 * (n - 1)``.

    >>> n = 10
    >>> G = nx.complete_graph(n)
    >>> nx.schultz_index(G) == (n * (n - 1) / 2) * (2 * (n - 1))
    True

    Graph that is disconnected

    >>> nx.schultz_index(nx.empty_graph(2))
    inf

    References
    ----------
    .. [1] I. Gutman, Selected properties of the Schultz molecular topological index,
           J. Chem. Inf. Comput. Sci. 34 (1994), 1087–1089.
           https://doi.org/10.1021/ci00021a009
    .. [2] M.V. Diudeaa and I. Gutman, Wiener-Type Topological Indices,
           Croatica Chemica Acta, 71 (1998), 21-51.
           https://hrcak.srce.hr/132323
    .. [3] H. P. Schultz, Topological organic chemistry. 1.
           Graph theory and topological indices of alkanes,i
           J. Chem. Inf. Comput. Sci. 29 (1989), 239–257.

    """

@_dispatchable
def gutman_index(G, weight=None) -> float:
    """Returns the Gutman Index for the graph `G`.

    The *Gutman Index* measures the topology of networks, especially for molecule
    networks of atoms connected by bonds [1]_. It is also called the Schultz Index
    of the second kind [2]_.

    Consider an undirected graph `G` with node set ``V``.
    The Gutman Index of a graph is the sum over all (unordered) pairs of nodes
    of nodes ``(u, v)``, with distance ``dist(u, v)`` and degrees ``deg(u)``
    and ``deg(v)``, of ``dist(u, v) * deg(u) * deg(v)``

    Parameters
    ----------
    G : NetworkX graph

    weight : string or None, optional (default: None)
        If None, every edge has weight 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        The edge weights are used to computing shortest-path distances.

    Returns
    -------
    number
        The Gutman Index of the graph `G`.

    Examples
    --------
    The Gutman Index of the (unweighted) complete graph on *n* nodes
    equals the number of pairs of the *n* nodes times ``(n - 1) * (n - 1)``,
    since each pair of nodes is at distance one and the product of degree of two
    vertices is ``(n - 1) * (n - 1)``.

    >>> n = 10
    >>> G = nx.complete_graph(n)
    >>> nx.gutman_index(G) == (n * (n - 1) / 2) * ((n - 1) * (n - 1))
    True

    Graphs that are disconnected

    >>> G = nx.empty_graph(2)
    >>> nx.gutman_index(G)
    inf

    References
    ----------
    .. [1] M.V. Diudeaa and I. Gutman, Wiener-Type Topological Indices,
           Croatica Chemica Acta, 71 (1998), 21-51.
           https://hrcak.srce.hr/132323
    .. [2] I. Gutman, Selected properties of the Schultz molecular topological index,
           J. Chem. Inf. Comput. Sci. 34 (1994), 1087–1089.
           https://doi.org/10.1021/ci00021a009

    """
