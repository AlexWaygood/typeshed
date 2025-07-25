"""Laplacian matrix of graphs.

All calculations here are done using the out-degree. For Laplacians using
in-degree, use `G.reverse(copy=False)` instead of `G` and take the transpose.

The `laplacian_matrix` function provides an unnormalized matrix,
while `normalized_laplacian_matrix`, `directed_laplacian_matrix`,
and `directed_combinatorial_laplacian_matrix` are all normalized.
"""

from _typeshed import Incomplete
from collections.abc import Collection

from networkx.utils.backends import _dispatchable

__all__ = [
    "laplacian_matrix",
    "normalized_laplacian_matrix",
    "directed_laplacian_matrix",
    "directed_combinatorial_laplacian_matrix",
]

@_dispatchable
def laplacian_matrix(G, nodelist: Collection[Incomplete] | None = None, weight: str = "weight"):
    """Returns the Laplacian matrix of G.

    The graph Laplacian is the matrix L = D - A, where
    A is the adjacency matrix and D is the diagonal matrix of node degrees.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    Returns
    -------
    L : SciPy sparse array
      The Laplacian matrix of G.

    Notes
    -----
    For MultiGraph, the edges weights are summed.

    This returns an unnormalized matrix. For a normalized output,
    use `normalized_laplacian_matrix`, `directed_laplacian_matrix`,
    or `directed_combinatorial_laplacian_matrix`.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    See Also
    --------
    :func:`~networkx.convert_matrix.to_numpy_array`
    normalized_laplacian_matrix
    directed_laplacian_matrix
    directed_combinatorial_laplacian_matrix
    :func:`~networkx.linalg.spectrum.laplacian_spectrum`

    Examples
    --------
    For graphs with multiple connected components, L is permutation-similar
    to a block diagonal matrix where each block is the respective Laplacian
    matrix for each component.

    >>> G = nx.Graph([(1, 2), (2, 3), (4, 5)])
    >>> print(nx.laplacian_matrix(G).toarray())
    [[ 1 -1  0  0  0]
     [-1  2 -1  0  0]
     [ 0 -1  1  0  0]
     [ 0  0  0  1 -1]
     [ 0  0  0 -1  1]]

    >>> edges = [
    ...     (1, 2),
    ...     (2, 1),
    ...     (2, 4),
    ...     (4, 3),
    ...     (3, 4),
    ... ]
    >>> DiG = nx.DiGraph(edges)
    >>> print(nx.laplacian_matrix(DiG).toarray())
    [[ 1 -1  0  0]
     [-1  2 -1  0]
     [ 0  0  1 -1]
     [ 0  0 -1  1]]

    Notice that node 4 is represented by the third column and row. This is because
    by default the row/column order is the order of `G.nodes` (i.e. the node added
    order -- in the edgelist, 4 first appears in (2, 4), before node 3 in edge (4, 3).)
    To control the node order of the matrix, use the `nodelist` argument.

    >>> print(nx.laplacian_matrix(DiG, nodelist=[1, 2, 3, 4]).toarray())
    [[ 1 -1  0  0]
     [-1  2  0 -1]
     [ 0  0  1 -1]
     [ 0  0 -1  1]]

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    >>> print(nx.laplacian_matrix(DiG.reverse(copy=False)).toarray().T)
    [[ 1 -1  0  0]
     [-1  1 -1  0]
     [ 0  0  2 -1]
     [ 0  0 -1  1]]

    References
    ----------
    .. [1] Langville, Amy N., and Carl D. Meyer. Google’s PageRank and Beyond:
       The Science of Search Engine Rankings. Princeton University Press, 2006.

    """

@_dispatchable
def normalized_laplacian_matrix(G, nodelist: Collection[Incomplete] | None = None, weight: str = "weight"):
    """Returns the normalized Laplacian matrix of G.

    The normalized graph Laplacian is the matrix

    .. math::

        N = D^{-1/2} L D^{-1/2}

    where `L` is the graph Laplacian and `D` is the diagonal matrix of
    node degrees [1]_.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    Returns
    -------
    N : SciPy sparse array
      The normalized Laplacian matrix of G.

    Notes
    -----
    For MultiGraph, the edges weights are summed.
    See :func:`to_numpy_array` for other options.

    If the Graph contains selfloops, D is defined as ``diag(sum(A, 1))``, where A is
    the adjacency matrix [2]_.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    For an unnormalized output, use `laplacian_matrix`.

    Examples
    --------

    >>> import numpy as np
    >>> edges = [
    ...     (1, 2),
    ...     (2, 1),
    ...     (2, 4),
    ...     (4, 3),
    ...     (3, 4),
    ... ]
    >>> DiG = nx.DiGraph(edges)
    >>> print(nx.normalized_laplacian_matrix(DiG).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.         -0.70710678  0.        ]
     [ 0.          0.          1.         -1.        ]
     [ 0.          0.         -1.          1.        ]]

    Notice that node 4 is represented by the third column and row. This is because
    by default the row/column order is the order of `G.nodes` (i.e. the node added
    order -- in the edgelist, 4 first appears in (2, 4), before node 3 in edge (4, 3).)
    To control the node order of the matrix, use the `nodelist` argument.

    >>> print(nx.normalized_laplacian_matrix(DiG, nodelist=[1, 2, 3, 4]).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.          0.         -0.70710678]
     [ 0.          0.          1.         -1.        ]
     [ 0.          0.         -1.          1.        ]]
    >>> G = nx.Graph(edges)
    >>> print(nx.normalized_laplacian_matrix(G).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.         -0.5         0.        ]
     [ 0.         -0.5         1.         -0.70710678]
     [ 0.          0.         -0.70710678  1.        ]]

    See Also
    --------
    laplacian_matrix
    normalized_laplacian_spectrum
    directed_laplacian_matrix
    directed_combinatorial_laplacian_matrix

    References
    ----------
    .. [1] Fan Chung-Graham, Spectral Graph Theory,
       CBMS Regional Conference Series in Mathematics, Number 92, 1997.
    .. [2] Steve Butler, Interlacing For Weighted Graphs Using The Normalized
       Laplacian, Electronic Journal of Linear Algebra, Volume 16, pp. 90-98,
       March 2007.
    .. [3] Langville, Amy N., and Carl D. Meyer. Google’s PageRank and Beyond:
       The Science of Search Engine Rankings. Princeton University Press, 2006.
    """

@_dispatchable
def directed_laplacian_matrix(
    G, nodelist: Collection[Incomplete] | None = None, weight: str = "weight", walk_type=None, alpha: float = 0.95
):
    """Returns the directed Laplacian matrix of G.

    The graph directed Laplacian is the matrix

    .. math::

        L = I - \\frac{1}{2} \\left (\\Phi^{1/2} P \\Phi^{-1/2} + \\Phi^{-1/2} P^T \\Phi^{1/2} \\right )

    where `I` is the identity matrix, `P` is the transition matrix of the
    graph, and `\\Phi` a matrix with the Perron vector of `P` in the diagonal and
    zeros elsewhere [1]_.

    Depending on the value of walk_type, `P` can be the transition matrix
    induced by a random walk, a lazy random walk, or a random walk with
    teleportation (PageRank).

    Parameters
    ----------
    G : DiGraph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    walk_type : string or None, optional (default=None)
       One of ``"random"``, ``"lazy"``, or ``"pagerank"``. If ``walk_type=None``
       (the default), then a value is selected according to the properties of `G`:
       - ``walk_type="random"`` if `G` is strongly connected and aperiodic
       - ``walk_type="lazy"`` if `G` is strongly connected but not aperiodic
       - ``walk_type="pagerank"`` for all other cases.

    alpha : real
       (1 - alpha) is the teleportation probability used with pagerank

    Returns
    -------
    L : NumPy matrix
      Normalized Laplacian of G.

    Notes
    -----
    Only implemented for DiGraphs

    The result is always a symmetric matrix.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    See Also
    --------
    laplacian_matrix
    normalized_laplacian_matrix
    directed_combinatorial_laplacian_matrix

    References
    ----------
    .. [1] Fan Chung (2005).
       Laplacians and the Cheeger inequality for directed graphs.
       Annals of Combinatorics, 9(1), 2005
    """

@_dispatchable
def directed_combinatorial_laplacian_matrix(
    G, nodelist: Collection[Incomplete] | None = None, weight: str = "weight", walk_type=None, alpha: float = 0.95
):
    """Return the directed combinatorial Laplacian matrix of G.

    The graph directed combinatorial Laplacian is the matrix

    .. math::

        L = \\Phi - \\frac{1}{2} \\left (\\Phi P + P^T \\Phi \\right)

    where `P` is the transition matrix of the graph and `\\Phi` a matrix
    with the Perron vector of `P` in the diagonal and zeros elsewhere [1]_.

    Depending on the value of walk_type, `P` can be the transition matrix
    induced by a random walk, a lazy random walk, or a random walk with
    teleportation (PageRank).

    Parameters
    ----------
    G : DiGraph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    walk_type : string or None, optional (default=None)
        One of ``"random"``, ``"lazy"``, or ``"pagerank"``. If ``walk_type=None``
        (the default), then a value is selected according to the properties of `G`:
        - ``walk_type="random"`` if `G` is strongly connected and aperiodic
        - ``walk_type="lazy"`` if `G` is strongly connected but not aperiodic
        - ``walk_type="pagerank"`` for all other cases.

    alpha : real
       (1 - alpha) is the teleportation probability used with pagerank

    Returns
    -------
    L : NumPy matrix
      Combinatorial Laplacian of G.

    Notes
    -----
    Only implemented for DiGraphs

    The result is always a symmetric matrix.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    See Also
    --------
    laplacian_matrix
    normalized_laplacian_matrix
    directed_laplacian_matrix

    References
    ----------
    .. [1] Fan Chung (2005).
       Laplacians and the Cheeger inequality for directed graphs.
       Annals of Combinatorics, 9(1), 2005
    """
