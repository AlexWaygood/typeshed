"""Functions for computing rich-club coefficients."""

from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable
from numpy.random import RandomState

__all__ = ["rich_club_coefficient"]

@_dispatchable
def rich_club_coefficient(
    G: Graph[_Node], normalized: bool = True, Q: float = 100, seed: int | RandomState | None = None
) -> dict[Incomplete, Incomplete]:
    """Returns the rich-club coefficient of the graph `G`.

    For each degree *k*, the *rich-club coefficient* is the ratio of the
    number of actual to the number of potential edges for nodes with
    degree greater than *k*:

    .. math::

        \\phi(k) = \\frac{2 E_k}{N_k (N_k - 1)}

    where `N_k` is the number of nodes with degree larger than *k*, and
    `E_k` is the number of edges among those nodes.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph with neither parallel edges nor self-loops.
    normalized : bool (optional)
        Normalize using randomized network as in [1]_
    Q : float (optional, default=100)
        If `normalized` is True, perform `Q * m` double-edge
        swaps, where `m` is the number of edges in `G`, to use as a
        null-model for normalization.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    rc : dictionary
       A dictionary, keyed by degree, with rich-club coefficient values.

    Raises
    ------
    NetworkXError
        If `G` has fewer than four nodes and ``normalized=True``.
        A randomly sampled graph for normalization cannot be generated in this case.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (4, 5)])
    >>> rc = nx.rich_club_coefficient(G, normalized=False, seed=42)
    >>> rc[0]
    0.4

    Notes
    -----
    The rich club definition and algorithm are found in [1]_.  This
    algorithm ignores any edge weights and is not defined for directed
    graphs or graphs with parallel edges or self loops.

    Normalization is done by computing the rich club coefficient for a randomly
    sampled graph with the same degree distribution as `G` by
    repeatedly swapping the endpoints of existing edges. For graphs with fewer than 4
    nodes, it is not possible to generate a random graph with a prescribed
    degree distribution, as the degree distribution fully determines the graph
    (hence making the coefficients trivially normalized to 1).
    This function raises an exception in this case.

    Estimates for appropriate values of `Q` are found in [2]_.

    References
    ----------
    .. [1] Julian J. McAuley, Luciano da Fontoura Costa,
       and Tibério S. Caetano,
       "The rich-club phenomenon across complex network hierarchies",
       Applied Physics Letters Vol 91 Issue 8, August 2007.
       https://arxiv.org/abs/physics/0701290
    .. [2] R. Milo, N. Kashtan, S. Itzkovitz, M. E. J. Newman, U. Alon,
       "Uniform generation of random graphs with arbitrary degree
       sequences", 2006. https://arxiv.org/abs/cond-mat/0312028
    """
