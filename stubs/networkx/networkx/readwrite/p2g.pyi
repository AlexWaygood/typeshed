"""
This module provides the following: read and write of p2g format
used in metabolic pathway studies.

See:
<https://web.archive.org/web/20080626113807/http://www.cs.purdue.edu/homes/koyuturk/pathway/>
for a description.

The summary is included here:

A file that describes a uniquely labeled graph (with extension ".gr")
format looks like the following:


name
3 4
a
1 2
b

c
0 2

"name" is simply a description of what the graph corresponds to. The
second line displays the number of nodes and number of edges,
respectively. This sample graph contains three nodes labeled "a", "b",
and "c". The rest of the graph contains two lines for each node. The
first line for a node contains the node label. After the declaration
of the node label, the out-edges of that node in the graph are
provided. For instance, "a" is linked to nodes 1 and 2, which are
labeled "b" and "c", while the node labeled "b" has no outgoing
edges. Observe that node labeled "c" has an outgoing edge to
itself. Indeed, self-loops are allowed. Node index starts from 0.

"""

from _typeshed import Incomplete

from networkx.utils.backends import _dispatchable

from ..classes.multidigraph import MultiDiGraph

def write_p2g(G, path, encoding: str = "utf-8") -> None:
    """Write NetworkX graph in p2g format.

    Notes
    -----
    This format is meant to be used with directed graphs with
    possible self loops.
    """

@_dispatchable
def read_p2g(path, encoding: str = "utf-8") -> MultiDiGraph[Incomplete]:
    """Read graph in p2g format from path.

    Parameters
    ----------
    path : string or file
       Filename or file handle to read.
       Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    MultiDiGraph

    Notes
    -----
    If you want a DiGraph (with no self loops allowed and no edge data)
    use D=nx.DiGraph(read_p2g(path))
    """

@_dispatchable
def parse_p2g(lines) -> MultiDiGraph[Incomplete]:
    """Parse p2g format graph from string or iterable.

    Returns
    -------
    MultiDiGraph
    """
