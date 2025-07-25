from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = ["randomized_partitioning", "one_exchange"]

@_dispatchable
def randomized_partitioning(G: Graph[_Node], seed: int | RandomState | None = None, p: float = 0.5, weight: str | None = None):
    """Compute a random partitioning of the graph nodes and its cut value.

    A partitioning is calculated by observing each node
    and deciding to add it to the partition with probability `p`,
    returning a random cut and its corresponding value (the
    sum of weights of edges connecting different partitions).

    Parameters
    ----------
    G : NetworkX graph

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    p : scalar
        Probability for each node to be part of the first partition.
        Should be in [0,1]

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    cut_size : scalar
        Value of the minimum cut.

    partition : pair of node sets
        A partitioning of the nodes that defines a minimum cut.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> cut_size, partition = nx.approximation.randomized_partitioning(G, seed=1)
    >>> cut_size
    6
    >>> partition
    ({0, 3, 4}, {1, 2})

    Raises
    ------
    NetworkXNotImplemented
        If the graph is directed or is a multigraph.
    """

@_dispatchable
def one_exchange(
    G: Graph[_Node], initial_cut: set[Incomplete] | None = None, seed: int | RandomState | None = None, weight: str | None = None
):
    """Compute a partitioning of the graphs nodes and the corresponding cut value.

    Use a greedy one exchange strategy to find a locally maximal cut
    and its value, it works by finding the best node (one that gives
    the highest gain to the cut value) to add to the current cut
    and repeats this process until no improvement can be made.

    Parameters
    ----------
    G : networkx Graph
        Graph to find a maximum cut for.

    initial_cut : set
        Cut to use as a starting point. If not supplied the algorithm
        starts with an empty cut.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    cut_value : scalar
        Value of the maximum cut.

    partition : pair of node sets
        A partitioning of the nodes that defines a maximum cut.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> curr_cut_size, partition = nx.approximation.one_exchange(G, seed=1)
    >>> curr_cut_size
    6
    >>> partition
    ({0, 2}, {1, 3, 4})

    Raises
    ------
    NetworkXNotImplemented
        If the graph is directed or is a multigraph.
    """
