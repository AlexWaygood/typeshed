"""Tree adapters let you convert from one tree structure to another

Example:

.. code-block:: python

   import html5lib
   from html5lib.treeadapters import genshi

   doc = '<html><body>Hi!</body></html>'
   treebuilder = html5lib.getTreeBuilder('etree')
   parser = html5lib.HTMLParser(tree=treebuilder)
   tree = parser.parse(doc)
   TreeWalker = html5lib.getTreeWalker('etree')

   genshi_tree = genshi.to_genshi(TreeWalker(tree))

"""

from . import genshi as genshi, sax as sax

__all__ = ["sax", "genshi"]
