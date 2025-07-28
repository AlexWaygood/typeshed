"""
Threshold Graphs - Creation, manipulation and identification.
"""

from collections.abc import Sequence

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = ["is_threshold_graph", "find_threshold_graph"]

@_dispatchable
def is_threshold_graph(G: Graph[_Node]) -> bool:
    """
    Returns `True` if `G` is a threshold graph.

    Parameters
    ----------
    G : NetworkX graph instance
        An instance of `Graph`, `DiGraph`, `MultiGraph` or `MultiDiGraph`

    Returns
    -------
    bool
        `True` if `G` is a threshold graph, `False` otherwise.

    Examples
    --------
    >>> from networkx.algorithms.threshold import is_threshold_graph
    >>> G = nx.path_graph(3)
    >>> is_threshold_graph(G)
    True
    >>> G = nx.barbell_graph(3, 3)
    >>> is_threshold_graph(G)
    False

    References
    ----------
    .. [1] Threshold graphs: https://en.wikipedia.org/wiki/Threshold_graph
    """

def is_threshold_sequence(degree_sequence: Sequence[list[int]]) -> bool:
    """
    Returns True if the sequence is a threshold degree sequence.

    Uses the property that a threshold graph must be constructed by
    adding either dominating or isolated nodes. Thus, it can be
    deconstructed iteratively by removing a node of degree zero or a
    node that connects to the remaining nodes.  If this deconstruction
    fails then the sequence is not a threshold sequence.
    """

def creation_sequence(degree_sequence, with_labels=False, compact=False):
    """
    Determines the creation sequence for the given threshold degree sequence.

    The creation sequence is a list of single characters 'd'
    or 'i': 'd' for dominating or 'i' for isolated vertices.
    Dominating vertices are connected to all vertices present when it
    is added.  The first node added is by convention 'd'.
    This list can be converted to a string if desired using "".join(cs)

    If with_labels==True:
    Returns a list of 2-tuples containing the vertex number
    and a character 'd' or 'i' which describes the type of vertex.

    If compact==True:
    Returns the creation sequence in a compact form that is the number
    of 'i's and 'd's alternating.
    Examples:
    [1,2,2,3] represents d,i,i,d,d,i,i,i
    [3,1,2] represents d,d,d,i,d,d

    Notice that the first number is the first vertex to be used for
    construction and so is always 'd'.

    with_labels and compact cannot both be True.

    Returns None if the sequence is not a threshold sequence
    """

def make_compact(creation_sequence):
    """
    Returns the creation sequence in a compact form
    that is the number of 'i's and 'd's alternating.

    Examples
    --------
    >>> from networkx.algorithms.threshold import make_compact
    >>> make_compact(["d", "i", "i", "d", "d", "i", "i", "i"])
    [1, 2, 2, 3]
    >>> make_compact(["d", "d", "d", "i", "d", "d"])
    [3, 1, 2]

    Notice that the first number is the first vertex
    to be used for construction and so is always 'd'.

    Labeled creation sequences lose their labels in the
    compact representation.

    >>> make_compact([3, 1, 2])
    [3, 1, 2]
    """

def uncompact(creation_sequence):
    """
    Converts a compact creation sequence for a threshold
    graph to a standard creation sequence (unlabeled).
    If the creation_sequence is already standard, return it.
    See creation_sequence.
    """

def creation_sequence_to_weights(creation_sequence):
    """
    Returns a list of node weights which create the threshold
    graph designated by the creation sequence.  The weights
    are scaled so that the threshold is 1.0.  The order of the
    nodes is the same as that in the creation sequence.
    """

def weights_to_creation_sequence(weights, threshold=1, with_labels=False, compact=False):
    """
    Returns a creation sequence for a threshold graph
    determined by the weights and threshold given as input.
    If the sum of two node weights is greater than the
    threshold value, an edge is created between these nodes.

    The creation sequence is a list of single characters 'd'
    or 'i': 'd' for dominating or 'i' for isolated vertices.
    Dominating vertices are connected to all vertices present
    when it is added.  The first node added is by convention 'd'.

    If with_labels==True:
    Returns a list of 2-tuples containing the vertex number
    and a character 'd' or 'i' which describes the type of vertex.

    If compact==True:
    Returns the creation sequence in a compact form that is the number
    of 'i's and 'd's alternating.
    Examples:
    [1,2,2,3] represents d,i,i,d,d,i,i,i
    [3,1,2] represents d,d,d,i,d,d

    Notice that the first number is the first vertex to be used for
    construction and so is always 'd'.

    with_labels and compact cannot both be True.
    """

@_dispatchable
def threshold_graph(creation_sequence, create_using=None):
    """
    Create a threshold graph from the creation sequence or compact
    creation_sequence.

    The input sequence can be a

    creation sequence (e.g. ['d','i','d','d','d','i'])
    labeled creation sequence (e.g. [(0,'d'),(2,'d'),(1,'i')])
    compact creation sequence (e.g. [2,1,1,2,0])

    Use cs=creation_sequence(degree_sequence,labeled=True)
    to convert a degree sequence to a creation sequence.

    Returns None if the sequence is not valid
    """

@_dispatchable
def find_alternating_4_cycle(G: Graph[_Node]):
    """
    Returns False if there aren't any alternating 4 cycles.
    Otherwise returns the cycle as [a,b,c,d] where (a,b)
    and (c,d) are edges and (a,c) and (b,d) are not.
    """

@_dispatchable
def find_threshold_graph(G: Graph[_Node], create_using: Graph[_Node] | None = None):
    """
    Returns a threshold subgraph that is close to largest in `G`.

    The threshold graph will contain the largest degree node in G.

    Parameters
    ----------
    G : NetworkX graph instance
        An instance of `Graph`, or `MultiDiGraph`
    create_using : NetworkX graph class or `None` (default), optional
        Type of graph to use when constructing the threshold graph.
        If `None`, infer the appropriate graph type from the input.

    Returns
    -------
    graph :
        A graph instance representing the threshold graph

    Examples
    --------
    >>> from networkx.algorithms.threshold import find_threshold_graph
    >>> G = nx.barbell_graph(3, 3)
    >>> T = find_threshold_graph(G)
    >>> T.nodes  # may vary
    NodeView((7, 8, 5, 6))

    References
    ----------
    .. [1] Threshold graphs: https://en.wikipedia.org/wiki/Threshold_graph
    """

@_dispatchable
def find_creation_sequence(G: Graph[_Node]):
    """
    Find a threshold subgraph that is close to largest in G.
    Returns the labeled creation sequence of that threshold graph.
    """

def triangles(creation_sequence):
    """
    Compute number of triangles in the threshold graph with the
    given creation sequence.
    """

def triangle_sequence(creation_sequence):
    """
    Return triangle sequence for the given threshold graph creation sequence.

    """

def cluster_sequence(creation_sequence):
    """
    Return cluster sequence for the given threshold graph creation sequence.
    """

def degree_sequence(creation_sequence):
    """
    Return degree sequence for the threshold graph with the given
    creation sequence
    """

def density(creation_sequence):
    """
    Return the density of the graph with this creation_sequence.
    The density is the fraction of possible edges present.
    """

def degree_correlation(creation_sequence):
    """
    Return the degree-degree correlation over all edges.
    """

def shortest_path(creation_sequence, u, v):
    """
    Find the shortest path between u and v in a
    threshold graph G with the given creation_sequence.

    For an unlabeled creation_sequence, the vertices
    u and v must be integers in (0,len(sequence)) referring
    to the position of the desired vertices in the sequence.

    For a labeled creation_sequence, u and v are labels of vertices.

    Use cs=creation_sequence(degree_sequence,with_labels=True)
    to convert a degree sequence to a creation sequence.

    Returns a list of vertices from u to v.
    Example: if they are neighbors, it returns [u,v]
    """

def shortest_path_length(creation_sequence, i):
    """
    Return the shortest path length from indicated node to
    every other node for the threshold graph with the given
    creation sequence.
    Node is indicated by index i in creation_sequence unless
    creation_sequence is labeled in which case, i is taken to
    be the label of the node.

    Paths lengths in threshold graphs are at most 2.
    Length to unreachable nodes is set to -1.
    """

def betweenness_sequence(creation_sequence, normalized=True):
    """
    Return betweenness for the threshold graph with the given creation
    sequence.  The result is unscaled.  To scale the values
    to the interval [0,1] divide by (n-1)*(n-2).
    """

def eigenvectors(creation_sequence):
    """
    Return a 2-tuple of Laplacian eigenvalues and eigenvectors
    for the threshold network with creation_sequence.
    The first value is a list of eigenvalues.
    The second value is a list of eigenvectors.
    The lists are in the same order so corresponding eigenvectors
    and eigenvalues are in the same position in the two lists.

    Notice that the order of the eigenvalues returned by eigenvalues(cs)
    may not correspond to the order of these eigenvectors.
    """

def spectral_projection(u, eigenpairs):
    """
    Returns the coefficients of each eigenvector
    in a projection of the vector u onto the normalized
    eigenvectors which are contained in eigenpairs.

    eigenpairs should be a list of two objects.  The
    first is a list of eigenvalues and the second a list
    of eigenvectors.  The eigenvectors should be lists.

    There's not a lot of error checking on lengths of
    arrays, etc. so be careful.
    """

def eigenvalues(creation_sequence):
    """
    Return sequence of eigenvalues of the Laplacian of the threshold
    graph for the given creation_sequence.

    Based on the Ferrer's diagram method.  The spectrum is integral
    and is the conjugate of the degree sequence.

    See::

      @Article{degree-merris-1994,
       author = {Russel Merris},
       title = {Degree maximal graphs are Laplacian integral},
       journal = {Linear Algebra Appl.},
       year = {1994},
       volume = {199},
       pages = {381--389},
      }

    """

def random_threshold_sequence(n, p, seed: int | RandomState | None = None):
    """
    Create a random threshold sequence of size n.
    A creation sequence is built by randomly choosing d's with
    probability p and i's with probability 1-p.

    s=nx.random_threshold_sequence(10,0.5)

    returns a threshold sequence of length 10 with equal
    probably of an i or a d at each position.

    A "random" threshold graph can be built with

    G=nx.threshold_graph(s)

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """

def right_d_threshold_sequence(n: int, m: int) -> list[str]:
    """
    Returns a "right-dominated" threshold sequence with `n` vertices and `m` edges.

    Each vertex in the sequence is either dominant or isolated.
    In the "right-dominated" version, once the basic sequence is formed,
    isolated vertices may be flipped to dominant from the right in order
    to reach the target number of edges.

    Parameters
    ----------
    n : int
        Number of vertices.
    m : int
        Number of edges.

    Returns
    -------
    A list of 'd' (dominant) and 'i' (isolated) forming a right-dominated threshold sequence.

    Raises
    ------
    ValueError
        If `m` exceeds the maximum number of edges.

    Examples
    --------
    >>> from networkx.algorithms.threshold import right_d_threshold_sequence
    >>> right_d_threshold_sequence(5, 3)
    ['d', 'i', 'i', 'd', 'i']
    """

def left_d_threshold_sequence(n: int, m: int) -> list[str]:
    """
    Returns a "left-dominated" threshold sequence with `n` vertices and `m` edges.

    Each vertex in the sequence is either dominant or isolated.
    In the "left-dominated" version, once the basic sequence is formed,
    isolated vertices may be flipped to dominant from the left in order
    to reach the target number of edges.

    Parameters
    ----------
    n : int
        Number of vertices.
    m : int
        Number of edges.

    Returns
    -------
    A list of 'd' (dominant) and 'i' (isolated) forming a left-dominated threshold sequence.

    Raises
    ------
    ValueError
        If `m` exceeds the maximum number of edges.

    Examples
    --------
    For certain small cases, both left and right dominated versions produce
    the same sequence. However, for larger values of `m`, the difference in
    flipping order becomes evident. For instance, compare the sequences for
    ``n=6, m=8``:

    >>> from networkx.algorithms.threshold import left_d_threshold_sequence
    >>> seq = left_d_threshold_sequence(6, 8)
    >>> seq
    ['d', 'd', 'd', 'i', 'i', 'd']

    In contrast, the right-dominated version yields:

    >>> from networkx.algorithms.threshold import right_d_threshold_sequence
    >>> right_seq = right_d_threshold_sequence(6, 8)
    >>> right_seq
    ['d', 'i', 'i', 'd', 'i', 'd']
    """

def swap_d(cs, p_split=1.0, p_combine=1.0, seed: int | RandomState | None = None):
    """
    Perform a "swap" operation on a threshold sequence.

    The swap preserves the number of nodes and edges
    in the graph for the given sequence.
    The resulting sequence is still a threshold sequence.

    Perform one split and one combine operation on the
    'd's of a creation sequence for a threshold graph.
    This operation maintains the number of nodes and edges
    in the graph, but shifts the edges from node to node
    maintaining the threshold quality of the graph.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    """
