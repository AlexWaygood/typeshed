"""Test sequences for graphiness."""

from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Literal

from networkx.utils.backends import _dispatchable

__all__ = [
    "is_graphical",
    "is_multigraphical",
    "is_pseudographical",
    "is_digraphical",
    "is_valid_degree_sequence_erdos_gallai",
    "is_valid_degree_sequence_havel_hakimi",
]

@_dispatchable
def is_graphical(sequence: Iterable[Incomplete], method: Literal["eg", "hh"] = "eg") -> bool:
    """Returns True if sequence is a valid degree sequence.

    A degree sequence is valid if some graph can realize it.

    Parameters
    ----------
    sequence : list or iterable container
        A sequence of integer node degrees

    method : "eg" | "hh"  (default: 'eg')
        The method used to validate the degree sequence.
        "eg" corresponds to the Erdős-Gallai algorithm
        [EG1960]_, [choudum1986]_, and
        "hh" to the Havel-Hakimi algorithm
        [havel1955]_, [hakimi1962]_, [CL1996]_.

    Returns
    -------
    valid : bool
        True if the sequence is a valid degree sequence and False if not.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> sequence = (d for n, d in G.degree())
    >>> nx.is_graphical(sequence)
    True

    To test a non-graphical sequence:
    >>> sequence_list = [d for n, d in G.degree()]
    >>> sequence_list[-1] += 1
    >>> nx.is_graphical(sequence_list)
    False

    References
    ----------
    .. [EG1960] Erdős and Gallai, Mat. Lapok 11 264, 1960.
    .. [choudum1986] S.A. Choudum. "A simple proof of the Erdős-Gallai theorem on
       graph sequences." Bulletin of the Australian Mathematical Society, 33,
       pp 67-70, 1986. https://doi.org/10.1017/S0004972700002872
    .. [havel1955] Havel, V. "A Remark on the Existence of Finite Graphs"
       Casopis Pest. Mat. 80, 477-480, 1955.
    .. [hakimi1962] Hakimi, S. "On the Realizability of a Set of Integers as
       Degrees of the Vertices of a Graph." SIAM J. Appl. Math. 10, 496-506, 1962.
    .. [CL1996] G. Chartrand and L. Lesniak, "Graphs and Digraphs",
       Chapman and Hall/CRC, 1996.
    """

@_dispatchable
def is_valid_degree_sequence_havel_hakimi(deg_sequence: Iterable[Incomplete]) -> bool:
    """Returns True if deg_sequence can be realized by a simple graph.

    The validation proceeds using the Havel-Hakimi theorem
    [havel1955]_, [hakimi1962]_, [CL1996]_.
    Worst-case run time is $O(s)$ where $s$ is the sum of the sequence.

    Parameters
    ----------
    deg_sequence : list
        A list of integers where each element specifies the degree of a node
        in a graph.

    Returns
    -------
    valid : bool
        True if deg_sequence is graphical and False if not.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 1), (5, 4)])
    >>> sequence = (d for _, d in G.degree())
    >>> nx.is_valid_degree_sequence_havel_hakimi(sequence)
    True

    To test a non-valid sequence:
    >>> sequence_list = [d for _, d in G.degree()]
    >>> sequence_list[-1] += 1
    >>> nx.is_valid_degree_sequence_havel_hakimi(sequence_list)
    False

    Notes
    -----
    The ZZ condition says that for the sequence d if

    .. math::
        |d| >= \\frac{(\\max(d) + \\min(d) + 1)^2}{4*\\min(d)}

    then d is graphical.  This was shown in Theorem 6 in [1]_.

    References
    ----------
    .. [1] I.E. Zverovich and V.E. Zverovich. "Contributions to the theory
       of graphic sequences", Discrete Mathematics, 105, pp. 292-303 (1992).
    .. [havel1955] Havel, V. "A Remark on the Existence of Finite Graphs"
       Casopis Pest. Mat. 80, 477-480, 1955.
    .. [hakimi1962] Hakimi, S. "On the Realizability of a Set of Integers as
       Degrees of the Vertices of a Graph." SIAM J. Appl. Math. 10, 496-506, 1962.
    .. [CL1996] G. Chartrand and L. Lesniak, "Graphs and Digraphs",
       Chapman and Hall/CRC, 1996.
    """

@_dispatchable
def is_valid_degree_sequence_erdos_gallai(deg_sequence: Iterable[Incomplete]) -> bool:
    """Returns True if deg_sequence can be realized by a simple graph.

    The validation is done using the Erdős-Gallai theorem [EG1960]_.

    Parameters
    ----------
    deg_sequence : list
        A list of integers

    Returns
    -------
    valid : bool
        True if deg_sequence is graphical and False if not.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 1), (5, 4)])
    >>> sequence = (d for _, d in G.degree())
    >>> nx.is_valid_degree_sequence_erdos_gallai(sequence)
    True

    To test a non-valid sequence:
    >>> sequence_list = [d for _, d in G.degree()]
    >>> sequence_list[-1] += 1
    >>> nx.is_valid_degree_sequence_erdos_gallai(sequence_list)
    False

    Notes
    -----

    This implementation uses an equivalent form of the Erdős-Gallai criterion.
    Worst-case run time is $O(n)$ where $n$ is the length of the sequence.

    Specifically, a sequence d is graphical if and only if the
    sum of the sequence is even and for all strong indices k in the sequence,

     .. math::

       \\sum_{i=1}^{k} d_i \\leq k(k-1) + \\sum_{j=k+1}^{n} \\min(d_i,k)
             = k(n-1) - ( k \\sum_{j=0}^{k-1} n_j - \\sum_{j=0}^{k-1} j n_j )

    A strong index k is any index where d_k >= k and the value n_j is the
    number of occurrences of j in d.  The maximal strong index is called the
    Durfee index.

    This particular rearrangement comes from the proof of Theorem 3 in [2]_.

    The ZZ condition says that for the sequence d if

    .. math::
        |d| >= \\frac{(\\max(d) + \\min(d) + 1)^2}{4*\\min(d)}

    then d is graphical.  This was shown in Theorem 6 in [2]_.

    References
    ----------
    .. [1] A. Tripathi and S. Vijay. "A note on a theorem of Erdős & Gallai",
       Discrete Mathematics, 265, pp. 417-420 (2003).
    .. [2] I.E. Zverovich and V.E. Zverovich. "Contributions to the theory
       of graphic sequences", Discrete Mathematics, 105, pp. 292-303 (1992).
    .. [EG1960] Erdős and Gallai, Mat. Lapok 11 264, 1960.
    """

@_dispatchable
def is_multigraphical(sequence: Iterable[Incomplete]) -> bool:
    """Returns True if some multigraph can realize the sequence.

    Parameters
    ----------
    sequence : list
        A list of integers

    Returns
    -------
    valid : bool
        True if deg_sequence is a multigraphic degree sequence and False if not.

    Examples
    --------
    >>> G = nx.MultiGraph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 1), (5, 4)])
    >>> sequence = (d for _, d in G.degree())
    >>> nx.is_multigraphical(sequence)
    True

    To test a non-multigraphical sequence:
    >>> sequence_list = [d for _, d in G.degree()]
    >>> sequence_list[-1] += 1
    >>> nx.is_multigraphical(sequence_list)
    False

    Notes
    -----
    The worst-case run time is $O(n)$ where $n$ is the length of the sequence.

    References
    ----------
    .. [1] S. L. Hakimi. "On the realizability of a set of integers as
       degrees of the vertices of a linear graph", J. SIAM, 10, pp. 496-506
       (1962).
    """

@_dispatchable
def is_pseudographical(sequence: Iterable[Incomplete]) -> bool:
    """Returns True if some pseudograph can realize the sequence.

    Every nonnegative integer sequence with an even sum is pseudographical
    (see [1]_).

    Parameters
    ----------
    sequence : list or iterable container
        A sequence of integer node degrees

    Returns
    -------
    valid : bool
      True if the sequence is a pseudographic degree sequence and False if not.

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 1), (5, 4)])
    >>> sequence = (d for _, d in G.degree())
    >>> nx.is_pseudographical(sequence)
    True

    To test a non-pseudographical sequence:
    >>> sequence_list = [d for _, d in G.degree()]
    >>> sequence_list[-1] += 1
    >>> nx.is_pseudographical(sequence_list)
    False

    Notes
    -----
    The worst-case run time is $O(n)$ where n is the length of the sequence.

    References
    ----------
    .. [1] F. Boesch and F. Harary. "Line removal algorithms for graphs
       and their degree lists", IEEE Trans. Circuits and Systems, CAS-23(12),
       pp. 778-782 (1976).
    """

@_dispatchable
def is_digraphical(in_sequence: Iterable[Incomplete], out_sequence: Iterable[Incomplete]) -> bool:
    """Returns True if some directed graph can realize the in- and out-degree
    sequences.

    Parameters
    ----------
    in_sequence : list or iterable container
        A sequence of integer node in-degrees

    out_sequence : list or iterable container
        A sequence of integer node out-degrees

    Returns
    -------
    valid : bool
      True if in and out-sequences are digraphic False if not.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (1, 3), (2, 3), (3, 4), (4, 2), (5, 1), (5, 4)])
    >>> in_seq = (d for n, d in G.in_degree())
    >>> out_seq = (d for n, d in G.out_degree())
    >>> nx.is_digraphical(in_seq, out_seq)
    True

    To test a non-digraphical scenario:
    >>> in_seq_list = [d for n, d in G.in_degree()]
    >>> in_seq_list[-1] += 1
    >>> nx.is_digraphical(in_seq_list, out_seq)
    False

    Notes
    -----
    This algorithm is from Kleitman and Wang [1]_.
    The worst case runtime is $O(s \\times \\log n)$ where $s$ and $n$ are the
    sum and length of the sequences respectively.

    References
    ----------
    .. [1] D.J. Kleitman and D.L. Wang
       Algorithms for Constructing Graphs and Digraphs with Given Valences
       and Factors, Discrete Mathematics, 6(1), pp. 79-88 (1973)
    """
