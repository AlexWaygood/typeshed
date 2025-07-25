"""A collection of modules for iterating through different kinds of
tree, generating tokens identical to those produced by the tokenizer
module.

To create a tree walker for a new type of tree, you need to
implement a tree walker object (called TreeWalker by convention) that
implements a 'serialize' method which takes a tree as sole argument and
returns an iterator which generates tokens.
"""

from types import ModuleType

__all__ = ["getTreeWalker", "pprint"]

def getTreeWalker(treeType: str, implementation: ModuleType | None = None, **kwargs):
    """Get a TreeWalker class for various types of tree with built-in support

    :arg str treeType: the name of the tree type required (case-insensitive).
        Supported values are:

        * "dom": The xml.dom.minidom DOM implementation
        * "etree": A generic walker for tree implementations exposing an
          elementtree-like interface (known to work with ElementTree,
          cElementTree and lxml.etree).
        * "lxml": Optimized walker for lxml.etree
        * "genshi": a Genshi stream

    :arg implementation: A module implementing the tree type e.g.
        xml.etree.ElementTree or cElementTree (Currently applies to the "etree"
        tree type only).

    :arg kwargs: keyword arguments passed to the etree walker--for other
        walkers, this has no effect

    :returns: a TreeWalker class

    """

def concatenateCharacterTokens(tokens): ...
def pprint(walker) -> str:
    """Pretty printer for tree walkers

    Takes a TreeWalker instance and pretty prints the output of walking the tree.

    :arg walker: a TreeWalker instance

    """
