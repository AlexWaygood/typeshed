"""
Functions for identifying isolate (degree zero) nodes.
"""

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["is_isolate", "isolates", "number_of_isolates"]

@_dispatchable
def is_isolate(G: Graph[_Node], n: _Node) -> bool:
    """Determines whether a node is an isolate.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    n : node
        A node in `G`.

    Returns
    -------
    is_isolate : bool
       True if and only if `n` has no neighbors.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_edge(1, 2)
    >>> G.add_node(3)
    >>> nx.is_isolate(G, 2)
    False
    >>> nx.is_isolate(G, 3)
    True
    """

@_dispatchable
def isolates(G: Graph[_Node]):
    """Iterator over isolates in the graph.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    iterator
        An iterator over the isolates of `G`.

    Examples
    --------
    To get a list of all isolates of a graph, use the :class:`list`
    constructor::

        >>> G = nx.Graph()
        >>> G.add_edge(1, 2)
        >>> G.add_node(3)
        >>> list(nx.isolates(G))
        [3]

    To remove all isolates in the graph, first create a list of the
    isolates, then use :meth:`Graph.remove_nodes_from`::

        >>> G.remove_nodes_from(list(nx.isolates(G)))
        >>> list(G)
        [1, 2]

    For digraphs, isolates have zero in-degree and zero out_degre::

        >>> G = nx.DiGraph([(0, 1), (1, 2)])
        >>> G.add_node(3)
        >>> list(nx.isolates(G))
        [3]

    """

@_dispatchable
def number_of_isolates(G: Graph[_Node]) -> int:
    """Returns the number of isolates in the graph.

    An *isolate* is a node with no neighbors (that is, with degree
    zero). For directed graphs, this means no in-neighbors and no
    out-neighbors.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    int
        The number of degree zero nodes in the graph `G`.

    """
