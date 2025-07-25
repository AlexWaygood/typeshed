"""Fast algorithms for the densest subgraph problem"""

from collections.abc import Callable, Hashable
from typing import Literal
from typing_extensions import TypeAlias

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

_Algorithm: TypeAlias = Literal["greedy++", "fista"]

__all__ = ["densest_subgraph"]

ALGORITHMS: dict[_Algorithm, Callable[[Graph[Hashable], int], tuple[float, set[int]]]]

@_dispatchable
def densest_subgraph(G: Graph[_Node], iterations: int = 1, *, method: _Algorithm = "fista") -> tuple[float, set[int]]:
    """Returns an approximate densest subgraph for a graph `G`.

    This function runs an iterative algorithm to find the densest subgraph,
    and returns both the density and the subgraph. For a discussion on the
    notion of density used and the different algorithms available on
    networkx, please see the Notes section below.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph.

    iterations : int, optional (default=1)
        Number of iterations to use for the iterative algorithm. Can be
        specified positionally or as a keyword argument.

    method : string, optional (default='fista')
        The algorithm to use to approximate the densest subgraph. Supported
        options: 'greedy++' by Boob et al. [2]_ and 'fista' by Harb et al. [3]_.
        Must be specified as a keyword argument. Other inputs produce a
        ValueError.

    Returns
    -------
    d : float
        The density of the approximate subgraph found.

    S : set
        The subset of nodes defining the approximate densest subgraph.

    Examples
    --------
    >>> G = nx.star_graph(4)
    >>> nx.approximation.densest_subgraph(G, iterations=1)
    (0.8, {0, 1, 2, 3, 4})

    Notes
    -----
    **Problem Definition:**
    The densest subgraph problem (DSG) asks to find the subgraph
    $S \\subseteq V(G)$ with maximum density. For a subset of the nodes of
    $G$, $S \\subseteq V(G)$, define $E(S) = \\{ (u,v) : (u,v)\\in E(G),
    u\\in S, v\\in S \\}$ as the set of edges with both endpoints in $S$.
    The density of $S$ is defined as $|E(S)|/|S|$, the ratio between the
    edges in the subgraph $G[S]$ and the number of nodes in that subgraph.
    Note that this is different from the standard graph theoretic definition
    of density, defined as $\\frac{2|E(S)|}{|S|(|S|-1)}$, for historical
    reasons.

    **Exact Algorithms:**
    The densest subgraph problem is polynomial time solvable using maximum
    flow, commonly referred to as Goldberg's algorithm. However, the
    algorithm is quite involved. It first binary searches on the optimal
    density, $d^\\ast$. For a guess of the density $d$, it sets up a flow
    network $G'$ with size $O(m)$. The maximum flow solution either
    informs the algorithm that no subgraph with density $d$ exists, or it
    provides a subgraph with density at least $d$. However, this is
    inherently bottlenecked by the maximum flow algorithm. For example, [2]_
    notes that Goldberg’s algorithm was not feasible on many large graphs
    even though they used a highly optimized maximum flow library.

    **Charikar's Greedy Peeling:**
    While exact solution algorithms are quite involved, there are several
    known approximation algorithms for the densest subgraph problem.

    Charikar [1]_ described a very simple 1/2-approximation algorithm for DSG
    known as the greedy "peeling" algorithm. The algorithm creates an
    ordering of the nodes as follows. The first node $v_1$ is the one with
    the smallest degree in $G$ (ties broken arbitrarily). It selects
    $v_2$ to be the smallest degree node in $G \\setminus v_1$. Letting
    $G_i$ be the graph after removing $v_1, ..., v_i$ (with $G_0=G$),
    the algorithm returns the graph among $G_0, ..., G_n$ with the highest
    density.

    **Greedy++:**
    Boob et al. [2]_ generalized this algorithm into Greedy++, an iterative
    algorithm that runs several rounds of "peeling". In fact, Greedy++ with 1
    iteration is precisely Charikar's algorithm. The algorithm converges to a
    $(1-\\epsilon)$ approximate densest subgraph in $O(\\Delta(G)\\log
    n/\\epsilon^2)$ iterations, where $\\Delta(G)$ is the maximum degree,
    and $n$ is the number of nodes in $G$. The algorithm also has other
    desirable properties as shown by [4]_ and [5]_.

    **FISTA Algorithm:**
    Harb et al. [3]_ gave a faster and more scalable algorithm using ideas
    from quadratic programming for the densest subgraph, which is based on a
    fast iterative shrinkage-thresholding algorithm (FISTA) algorithm. It is
    known that computing the densest subgraph can be formulated as the
    following convex optimization problem:

    Minimize $\\sum_{u \\in V(G)} b_u^2$

    Subject to:

    $b_u = \\sum_{v: \\{u,v\\} \\in E(G)} x_{uv}$ for all $u \\in V(G)$

    $x_{uv} + x_{vu} = 1.0$ for all $\\{u,v\\} \\in E(G)$

    $x_{uv} \\geq 0, x_{vu} \\geq 0$ for all $\\{u,v\\} \\in E(G)$

    Here, $x_{uv}$ represents the fraction of edge $\\{u,v\\}$ assigned to
    $u$, and $x_{vu}$ to $v$.

    The FISTA algorithm efficiently solves this convex program using gradient
    descent with projections. For a learning rate $\\alpha$, the algorithm
    does:

    1. **Initialization**: Set $x^{(0)}_{uv} = x^{(0)}_{vu} = 0.5$ for all
    edges as a feasible solution.

    2. **Gradient Update**: For iteration $k\\geq 1$, set
    $x^{(k+1)}_{uv} = x^{(k)}_{uv} - 2 \\alpha \\sum_{v: \\{u,v\\} \\in E(G)}
    x^{(k)}_{uv}$. However, now $x^{(k+1)}_{uv}$ might be infeasible!
    To ensure feasibility, we project $x^{(k+1)}_{uv}$.

    3. **Projection to the Feasible Set**: Compute
    $b^{(k+1)}_u = \\sum_{v: \\{u,v\\} \\in E(G)} x^{(k)}_{uv}$ for all
    nodes $u$. Define $z^{(k+1)}_{uv} = x^{(k+1)}_{uv} - 2 \\alpha
    b^{(k+1)}_u$. Update $x^{(k+1)}_{uv} =
    CLAMP((z^{(k+1)}_{uv} - z^{(k+1)}_{vu} + 1.0) / 2.0)$, where
    $CLAMP(x) = \\max(0, \\min(1, x))$.

    With a learning rate of $\\alpha=1/\\Delta(G)$, where $\\Delta(G)$ is
    the maximum degree, the algorithm converges to the optimum solution of
    the convex program.

    **Fractional Peeling:**
    To obtain a **discrete** subgraph, we use fractional peeling, an
    adaptation of the standard peeling algorithm which peels the minimum
    degree vertex in each iteration, and returns the densest subgraph found
    along the way. Here, we instead peel the vertex with the smallest
    induced load $b_u$:

    1. Compute $b_u$ and $x_{uv}$.

    2. Iteratively remove the vertex with the smallest $b_u$, updating its
    neighbors' load by $x_{vu}$.

    Fractional peeling transforms the approximately optimal fractional
    values $b_u, x_{uv}$ into a discrete subgraph. Unlike traditional
    peeling, which removes the lowest-degree node, this method accounts for
    fractional edge contributions from the convex program.

    This approach is both scalable and theoretically sound, ensuring a quick
    approximation of the densest subgraph while leveraging fractional load
    balancing.

    References
    ----------
    .. [1] Charikar, Moses. "Greedy approximation algorithms for finding dense
       components in a graph." In International workshop on approximation
       algorithms for combinatorial optimization, pp. 84-95. Berlin, Heidelberg:
       Springer Berlin Heidelberg, 2000.

    .. [2] Boob, Digvijay, Yu Gao, Richard Peng, Saurabh Sawlani, Charalampos
       Tsourakakis, Di Wang, and Junxing Wang. "Flowless: Extracting densest
       subgraphs without flow computations." In Proceedings of The Web Conference
       2020, pp. 573-583. 2020.

    .. [3] Harb, Elfarouk, Kent Quanrud, and Chandra Chekuri. "Faster and scalable
       algorithms for densest subgraph and decomposition." Advances in Neural
       Information Processing Systems 35 (2022): 26966-26979.

    .. [4] Harb, Elfarouk, Kent Quanrud, and Chandra Chekuri. "Convergence to
       lexicographically optimal base in a (contra) polymatroid and applications
       to densest subgraph and tree packing." arXiv preprint arXiv:2305.02987
       (2023).

    .. [5] Chekuri, Chandra, Kent Quanrud, and Manuel R. Torres. "Densest
       subgraph: Supermodularity, iterative peeling, and flow." In Proceedings of
       the 2022 Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), pp.
       1531-1555. Society for Industrial and Applied Mathematics, 2022.
    """
