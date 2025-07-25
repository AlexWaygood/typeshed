"""
Mixing matrices for node attributes and degree.
"""

from _typeshed import Incomplete, SupportsGetItem
from collections.abc import Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["attribute_mixing_matrix", "attribute_mixing_dict", "degree_mixing_matrix", "degree_mixing_dict", "mixing_dict"]

@_dispatchable
def attribute_mixing_dict(
    G: Graph[_Node], attribute: str, nodes: Iterable[Incomplete] | None = None, normalized: bool = False
) -> dict[Incomplete, Incomplete]:
    """Returns dictionary representation of mixing matrix for attribute.

    Parameters
    ----------
    G : graph
       NetworkX graph object.

    attribute : string
       Node attribute key.

    nodes: list or iterable (optional)
        Unse nodes in container to build the dict. The default is all nodes.

    normalized : bool (default=False)
       Return counts if False or probabilities if True.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_nodes_from([0, 1], color="red")
    >>> G.add_nodes_from([2, 3], color="blue")
    >>> G.add_edge(1, 3)
    >>> d = nx.attribute_mixing_dict(G, "color")
    >>> print(d["red"]["blue"])
    1
    >>> print(d["blue"]["red"])  # d symmetric for undirected graphs
    1

    Returns
    -------
    d : dictionary
       Counts or joint probability of occurrence of attribute pairs.
    """

@_dispatchable
def attribute_mixing_matrix(
    G: Graph[_Node],
    attribute: str,
    nodes: Iterable[Incomplete] | None = None,
    mapping: SupportsGetItem[Incomplete, Incomplete] | None = None,
    normalized: bool = True,
):
    """Returns mixing matrix for attribute.

    Parameters
    ----------
    G : graph
       NetworkX graph object.

    attribute : string
       Node attribute key.

    nodes: list or iterable (optional)
        Use only nodes in container to build the matrix. The default is
        all nodes.

    mapping : dictionary, optional
       Mapping from node attribute to integer index in matrix.
       If not specified, an arbitrary ordering will be used.

    normalized : bool (default=True)
       Return counts if False or probabilities if True.

    Returns
    -------
    m: numpy array
       Counts or joint probability of occurrence of attribute pairs.

    Notes
    -----
    If each node has a unique attribute value, the unnormalized mixing matrix
    will be equal to the adjacency matrix. To get a denser mixing matrix,
    the rounding can be performed to form groups of nodes with equal values.
    For example, the exact height of persons in cm (180.79155222, 163.9080892,
    163.30095355, 167.99016217, 168.21590163, ...) can be rounded to (180, 163,
    163, 168, 168, ...).

    Definitions of attribute mixing matrix vary on whether the matrix
    should include rows for attribute values that don't arise. Here we
    do not include such empty-rows. But you can force them to appear
    by inputting a `mapping` that includes those values.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> gender = {0: "male", 1: "female", 2: "female"}
    >>> nx.set_node_attributes(G, gender, "gender")
    >>> mapping = {"male": 0, "female": 1}
    >>> mix_mat = nx.attribute_mixing_matrix(G, "gender", mapping=mapping)
    >>> mix_mat
    array([[0.  , 0.25],
           [0.25, 0.5 ]])
    """

@_dispatchable
def degree_mixing_dict(
    G: Graph[_Node], x: str = "out", y: str = "in", weight: str | None = None, nodes=None, normalized: bool = False
) -> dict[Incomplete, Incomplete]:
    """Returns dictionary representation of mixing matrix for degree.

    Parameters
    ----------
    G : graph
        NetworkX graph object.

    x: string ('in','out')
       The degree type for source node (directed graphs only).

    y: string ('in','out')
       The degree type for target node (directed graphs only).

    weight: string or None, optional (default=None)
       The edge attribute that holds the numerical value used
       as a weight.  If None, then each edge has weight 1.
       The degree is the sum of the edge weights adjacent to the node.

    normalized : bool (default=False)
        Return counts if False or probabilities if True.

    Returns
    -------
    d: dictionary
       Counts or joint probability of occurrence of degree pairs.
    """

@_dispatchable
def degree_mixing_matrix(
    G: Graph[_Node],
    x: str = "out",
    y: str = "in",
    weight: str | None = None,
    nodes: Iterable[Incomplete] | None = None,
    normalized: bool = True,
    mapping: SupportsGetItem[Incomplete, Incomplete] | None = None,
):
    """Returns mixing matrix for attribute.

    Parameters
    ----------
    G : graph
       NetworkX graph object.

    x: string ('in','out')
       The degree type for source node (directed graphs only).

    y: string ('in','out')
       The degree type for target node (directed graphs only).

    nodes: list or iterable (optional)
        Build the matrix using only nodes in container.
        The default is all nodes.

    weight: string or None, optional (default=None)
       The edge attribute that holds the numerical value used
       as a weight.  If None, then each edge has weight 1.
       The degree is the sum of the edge weights adjacent to the node.

    normalized : bool (default=True)
       Return counts if False or probabilities if True.

    mapping : dictionary, optional
       Mapping from node degree to integer index in matrix.
       If not specified, an arbitrary ordering will be used.

    Returns
    -------
    m: numpy array
       Counts, or joint probability, of occurrence of node degree.

    Notes
    -----
    Definitions of degree mixing matrix vary on whether the matrix
    should include rows for degree values that don't arise. Here we
    do not include such empty-rows. But you can force them to appear
    by inputting a `mapping` that includes those values. See examples.

    Examples
    --------
    >>> G = nx.star_graph(3)
    >>> mix_mat = nx.degree_mixing_matrix(G)
    >>> mix_mat
    array([[0. , 0.5],
           [0.5, 0. ]])

    If you want every possible degree to appear as a row, even if no nodes
    have that degree, use `mapping` as follows,

    >>> max_degree = max(deg for n, deg in G.degree)
    >>> mapping = {x: x for x in range(max_degree + 1)}  # identity mapping
    >>> mix_mat = nx.degree_mixing_matrix(G, mapping=mapping)
    >>> mix_mat
    array([[0. , 0. , 0. , 0. ],
           [0. , 0. , 0. , 0.5],
           [0. , 0. , 0. , 0. ],
           [0. , 0.5, 0. , 0. ]])
    """

@_dispatchable
def mixing_dict(xy, normalized: bool = False) -> dict[Incomplete, Incomplete]:
    """Returns a dictionary representation of mixing matrix.

    Parameters
    ----------
    xy : list or container of two-tuples
       Pairs of (x,y) items.

    attribute : string
       Node attribute key

    normalized : bool (default=False)
       Return counts if False or probabilities if True.

    Returns
    -------
    d: dictionary
       Counts or Joint probability of occurrence of values in xy.
    """
