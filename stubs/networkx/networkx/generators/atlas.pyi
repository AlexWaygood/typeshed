"""
Generators for the small graph atlas.
"""

import sys
from _typeshed import Incomplete
from typing import Final

from networkx.utils.backends import _dispatchable

from ..classes.graph import Graph

if sys.version_info >= (3, 11):
    from importlib.resources.abc import Traversable
else:
    from importlib.abc import Traversable

__all__ = ["graph_atlas", "graph_atlas_g"]

NUM_GRAPHS: Final = 1253
ATLAS_FILE: Final[Traversable]

@_dispatchable
def graph_atlas(i) -> Graph[Incomplete]:
    """Returns graph number `i` from the Graph Atlas.

    For more information, see :func:`.graph_atlas_g`.

    Parameters
    ----------
    i : int
        The index of the graph from the atlas to get. The graph at index
        0 is assumed to be the null graph.

    Returns
    -------
    list
        A list of :class:`~networkx.Graph` objects, the one at index *i*
        corresponding to the graph *i* in the Graph Atlas.

    See also
    --------
    graph_atlas_g

    Notes
    -----
    The time required by this function increases linearly with the
    argument `i`, since it reads a large file sequentially in order to
    generate the graph [1]_.

    References
    ----------
    .. [1] Ronald C. Read and Robin J. Wilson, *An Atlas of Graphs*.
           Oxford University Press, 1998.

    """

@_dispatchable
def graph_atlas_g() -> list[Graph[Incomplete]]:
    """Returns the list of all graphs with up to seven nodes named in the
    Graph Atlas.

    The graphs are listed in increasing order by

    1. number of nodes,
    2. number of edges,
    3. degree sequence (for example 111223 < 112222),
    4. number of automorphisms,

    in that order, with three exceptions as described in the *Notes*
    section below. This causes the list to correspond with the index of
    the graphs in the Graph Atlas [atlas]_, with the first graph,
    ``G[0]``, being the null graph.

    Returns
    -------
    list
        A list of :class:`~networkx.Graph` objects, the one at index *i*
        corresponding to the graph *i* in the Graph Atlas.

    Examples
    --------
    >>> from pprint import pprint
    >>> atlas = nx.graph_atlas_g()

    There are 1253 graphs in the atlas

    >>> len(atlas)
    1253

    The number of graphs with *n* nodes, where *n* ranges from 0 to 7:

    >>> from collections import Counter
    >>> num_nodes_per_graph = [len(G) for G in atlas]
    >>> Counter(num_nodes_per_graph)
    Counter({7: 1044, 6: 156, 5: 34, 4: 11, 3: 4, 2: 2, 0: 1, 1: 1})

    Since the atlas is ordered by the number of nodes in the graph, all graphs
    with *n* nodes can be obtained by slicing the atlas. For example, all
    graphs with 5 nodes:

    >>> G5_list = atlas[19:53]
    >>> all(len(G) == 5 for G in G5_list)
    True

    Or all graphs with at least 3 nodes but fewer than 7 nodes:

    >>> G3_6_list = atlas[4:209]

    More generally, the indices that partition the atlas by the number of nodes
    per graph:

    >>> import itertools
    >>> partition_indices = [0] + list(
    ...     itertools.accumulate(Counter(num_nodes_per_graph).values())  # cumsum
    ... )
    >>> partition_indices
    [0, 1, 2, 4, 8, 19, 53, 209, 1253]
    >>> partition_mapping = dict(enumerate(itertools.pairwise(partition_indices)))
    >>> pprint(partition_mapping)
    {0: (0, 1),
     1: (1, 2),
     2: (2, 4),
     3: (4, 8),
     4: (8, 19),
     5: (19, 53),
     6: (53, 209),
     7: (209, 1253)}

    See also
    --------
    graph_atlas

    Notes
    -----
    This function may be expensive in both time and space, since it
    reads a large file sequentially in order to populate the list.

    Although the NetworkX atlas functions match the order of graphs
    given in the "Atlas of Graphs" book, there are (at least) three
    errors in the ordering described in the book. The following three
    pairs of nodes violate the lexicographically nondecreasing sorted
    degree sequence rule:

    - graphs 55 and 56 with degree sequences 001111 and 000112,
    - graphs 1007 and 1008 with degree sequences 3333444 and 3333336,
    - graphs 1012 and 1213 with degree sequences 1244555 and 1244456.

    References
    ----------
    .. [atlas] Ronald C. Read and Robin J. Wilson,
               *An Atlas of Graphs*.
               Oxford University Press, 1998.

    """
