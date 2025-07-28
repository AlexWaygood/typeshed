"""Generators of x-y pairs of node data."""

from _typeshed import Incomplete
from collections.abc import Generator, Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["node_attribute_xy", "node_degree_xy"]

@_dispatchable
def node_attribute_xy(G: Graph[_Node], attribute, nodes: Iterable[Incomplete] | None = None) -> Generator[Incomplete, None, None]:
    """Yields 2-tuples of node attribute values for all edges in `G`.

    This generator yields, for each edge in `G` incident to a node in `nodes`,
    a 2-tuple of form ``(attribute value,  attribute value)`` for the parameter
    specified node-attribute.

    Parameters
    ----------
    G: NetworkX graph

    attribute: key
        The node attribute key.

    nodes: list or iterable (optional)
        Use only edges that are incident to specified nodes.
        The default is all nodes.

    Yields
    ------
    (x, y): 2-tuple
        Generates 2-tuple of (attribute, attribute) values.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_node(1, color="red")
    >>> G.add_node(2, color="blue")
    >>> G.add_node(3, color="green")
    >>> G.add_edge(1, 2)
    >>> list(nx.node_attribute_xy(G, "color"))
    [('red', 'blue')]

    Notes
    -----
    For undirected graphs, each edge is produced twice, once for each edge
    representation (u, v) and (v, u), with the exception of self-loop edges
    which only appear once.
    """

@_dispatchable
def node_degree_xy(
    G: Graph[_Node], x: str = "out", y: str = "in", weight: str | None = None, nodes: Iterable[Incomplete] | None = None
) -> Generator[Incomplete, None, None]:
    """Yields 2-tuples of ``(degree, degree)`` values for edges in `G`.

    This generator yields, for each edge in `G` incident to a node in `nodes`,
    a 2-tuple of form ``(degree, degree)``. The node degrees are weighted
    when a `weight` attribute is specified.

    Parameters
    ----------
    G: NetworkX graph

    x: string ('in','out')
       The degree type for source node (directed graphs only).

    y: string ('in','out')
       The degree type for target node (directed graphs only).

    weight: string or None, optional (default=None)
       The edge attribute that holds the numerical value used
       as a weight.  If None, then each edge has weight 1.
       The degree is the sum of the edge weights adjacent to the node.

    nodes: list or iterable (optional)
        Use only edges that are adjacency to specified nodes.
        The default is all nodes.

    Yields
    ------
    (x, y): 2-tuple
        Generates 2-tuple of (degree, degree) values.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2)
    >>> list(nx.node_degree_xy(G, x="out", y="in"))
    [(1, 1)]
    >>> list(nx.node_degree_xy(G, x="in", y="out"))
    [(0, 0)]

    Notes
    -----
    For undirected graphs, each edge is produced twice, once for each edge
    representation (u, v) and (v, u), with the exception of self-loop edges
    which only appear once.
    """
