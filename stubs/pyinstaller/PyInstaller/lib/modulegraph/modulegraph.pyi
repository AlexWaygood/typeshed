"""
Find modules used by a script, using bytecode analysis.

Based on the stdlib modulefinder by Thomas Heller and Just van Rossum,
but uses a graph data structure and 2.3 features

XXX: Verify all calls to _import_hook (and variants) to ensure that
imports are done in the right way.
"""

# Partial typing of the vendored modulegraph package.
# We reference the vendored package rather than depending on the original untyped module.
# Anything not referenced in the PyInstaller stubs doesn't need to be added here.

from types import CodeType
from typing import Protocol

class _SupportsGraphident(Protocol):
    graphident: str

# code, filename and packagepath are always initialized to None. But they can be given a value later.
class Node:
    """
    Abstract base class (ABC) of all objects added to a `ModuleGraph`.

    Attributes
    ----------
    code : codeobject
        Code object of the pure-Python module corresponding to this graph node
        if any _or_ `None` otherwise.
    graphident : str
        Synonym of `identifier` required by the `ObjectGraph` superclass of the
        `ModuleGraph` class. For readability, the `identifier` attribute should
        typically be used instead.
    filename : str
        Absolute path of this graph node's corresponding module, package, or C
        extension if any _or_ `None` otherwise.
    identifier : str
        Fully-qualified name of this graph node's corresponding module,
        package, or C extension.
    packagepath : str
        List of the absolute paths of all directories comprising this graph
        node's corresponding package. If this is a:
        * Non-namespace package, this list contains exactly one path.
        * Namespace package, this list contains one or more paths.
    _deferred_imports : list
        List of all target modules imported by the source module corresponding
        to this graph node whole importations have been deferred for subsequent
        processing in between calls to the `_ModuleGraph._scan_code()` and
        `_ModuleGraph._process_imports()` methods for this source module _or_
        `None` otherwise. Each element of this list is a 3-tuple
        `(have_star, _safe_import_hook_args, _safe_import_hook_kwargs)`
        collecting the importation of a target module from this source module
        for subsequent processing, where:
        * `have_star` is a boolean `True` only if this is a `from`-style star
          import (e.g., resembling `from {target_module_name} import *`).
        * `_safe_import_hook_args` is a (typically non-empty) sequence of all
          positional arguments to be passed to the `_safe_import_hook()` method
          to add this importation to the graph.
        * `_safe_import_hook_kwargs` is a (typically empty) dictionary of all
          keyword arguments to be passed to the `_safe_import_hook()` method
          to add this importation to the graph.
        Unlike functional languages, Python imposes a maximum depth on the
        interpreter stack (and hence recursion). On breaching this depth,
        Python raises a fatal `RuntimeError` exception. Since `ModuleGraph`
        parses imports recursively rather than iteratively, this depth _was_
        commonly breached before the introduction of this list. Python
        environments installing a large number of modules (e.g., Anaconda) were
        particularly susceptible. Why? Because `ModuleGraph` concurrently
        descended through both the abstract syntax trees (ASTs) of all source
        modules being parsed _and_ the graph of all target modules imported by
        these source modules being built. The stack thus consisted of
        alternating layers of AST and graph traversal. To unwind such
        alternation and effectively halve the stack depth, `ModuleGraph` now
        descends through the abstract syntax tree (AST) of each source module
        being parsed and adds all importations originating within this module
        to this list _before_ descending into the graph of these importations.
        See pyinstaller/pyinstaller/#1289 for further details.
    _global_attr_names : set
        Set of the unqualified names of all global attributes (e.g., classes,
        variables) defined in the pure-Python module corresponding to this
        graph node if any _or_ the empty set otherwise. This includes the names
        of all attributes imported via `from`-style star imports from other
        existing modules (e.g., `from {target_module_name} import *`). This
        set is principally used to differentiate the non-ignorable importation
        of non-existent submodules in a package from the ignorable importation
        of existing global attributes defined in that package's pure-Python
        `__init__` submodule in `from`-style imports (e.g., `bar` in
        `from foo import bar`, which may be either a submodule or attribute of
        `foo`), as such imports ambiguously allow both. This set is _not_ used
        to differentiate submodules from attributes in `import`-style imports
        (e.g., `bar` in `import foo.bar`, which _must_ be a submodule of
        `foo`), as such imports unambiguously allow only submodules.
    _starimported_ignored_module_names : set
        Set of the fully-qualified names of all existing unparsable modules
        that the existing parsable module corresponding to this graph node
        attempted to perform one or more "star imports" from. If this module
        either does _not_ exist or does but is unparsable, this is the empty
        set. Equivalently, this set contains each fully-qualified name
        `{trg_module_name}` for which:
        * This module contains an import statement of the form
          `from {trg_module_name} import *`.
        * The module whose name is `{trg_module_name}` exists but is _not_
          parsable by `ModuleGraph` (e.g., due to _not_ being pure-Python).
        **This set is currently defined but otherwise ignored.**
    _submodule_basename_to_node : dict
        Dictionary mapping from the unqualified name of each submodule
        contained by the parent module corresponding to this graph node to that
        submodule's graph node. If this dictionary is non-empty, this parent
        module is typically but _not_ always a package (e.g., the non-package
        `os` module containing the `os.path` submodule).
    """

    # Compiled code. See stdlib.builtins.compile
    code: CodeType | None
    filename: str | None
    graphident: str
    identifier: str
    packagepath: str | None
    def __init__(self, identifier: str) -> None:
        """
        Initialize this graph node.

        Parameters
        ----------
        identifier : str
            Fully-qualified name of this graph node's corresponding module,
            package, or C extension.
        """

    def is_global_attr(self, attr_name: str) -> bool:
        """
        `True` only if the pure-Python module corresponding to this graph node
        defines a global attribute (e.g., class, variable) with the passed
        name.

        If this module is actually a package, this method instead returns
        `True` only if this package's pure-Python `__init__` submodule defines
        such a global attribute. In this case, note that this package may still
        contain an importable submodule of the same name. Callers should
        attempt to import this attribute as a submodule of this package
        _before_ assuming this attribute to be an ignorable global. See
        "Examples" below for further details.

        Parameters
        ----------
        attr_name : str
            Unqualified name of the attribute to be tested.

        Returns
        ----------
        bool
            `True` only if this module defines this global attribute.

        Examples
        ----------
        Consider a hypothetical module `foo` containing submodules `bar` and
        `__init__` where the latter assigns `bar` to be a global variable
        (possibly star-exported via the special `__all__` global variable):

        >>> # In "foo.__init__":
        >>> bar = 3.1415

        Python 2 and 3 both permissively permit this. This method returns
        `True` in this case (i.e., when called on the `foo` package's graph
        node, passed the attribute name `bar`) despite the importability of the
        `foo.bar` submodule.
        """

    def is_submodule(self, submodule_basename: str) -> bool:
        """
        `True` only if the parent module corresponding to this graph node
        contains the submodule with the passed name.

        If `True`, this parent module is typically but _not_ always a package
        (e.g., the non-package `os` module containing the `os.path` submodule).

        Parameters
        ----------
        submodule_basename : str
            Unqualified name of the submodule to be tested.

        Returns
        ----------
        bool
            `True` only if this parent module contains this submodule.
        """

    def add_global_attr(self, attr_name: str) -> None:
        """
        Record the global attribute (e.g., class, variable) with the passed
        name to be defined by the pure-Python module corresponding to this
        graph node.

        If this module is actually a package, this method instead records this
        attribute to be defined by this package's pure-Python `__init__`
        submodule.

        Parameters
        ----------
        attr_name : str
            Unqualified name of the attribute to be added.
        """

    def add_global_attrs_from_module(self, target_module: Node) -> None:
        """
        Record all global attributes (e.g., classes, variables) defined by the
        target module corresponding to the passed graph node to also be defined
        by the source module corresponding to this graph node.

        If the source module is actually a package, this method instead records
        these attributes to be defined by this package's pure-Python `__init__`
        submodule.

        Parameters
        ----------
        target_module : Node
            Graph node of the target module to import attributes from.
        """

    def add_submodule(self, submodule_basename: str, submodule_node: Node) -> None:
        """
        Add the submodule with the passed name and previously imported graph
        node to the parent module corresponding to this graph node.

        This parent module is typically but _not_ always a package (e.g., the
        non-package `os` module containing the `os.path` submodule).

        Parameters
        ----------
        submodule_basename : str
            Unqualified name of the submodule to add to this parent module.
        submodule_node : Node
            Graph node of this submodule.
        """

    def get_submodule(self, submodule_basename: str) -> Node:
        """
        Graph node of the submodule with the passed name in the parent module
        corresponding to this graph node.

        If this parent module does _not_ contain this submodule, an exception
        is raised. Else, this parent module is typically but _not_ always a
        package (e.g., the non-package `os` module containing the `os.path`
        submodule).

        Parameters
        ----------
        module_basename : str
            Unqualified name of the submodule to retrieve.

        Returns
        ----------
        Node
            Graph node of this submodule.
        """

    def get_submodule_or_none(self, submodule_basename: str) -> Node | None:
        """
        Graph node of the submodule with the passed unqualified name in the
        parent module corresponding to this graph node if this module contains
        this submodule _or_ `None`.

        This parent module is typically but _not_ always a package (e.g., the
        non-package `os` module containing the `os.path` submodule).

        Parameters
        ----------
        submodule_basename : str
            Unqualified name of the submodule to retrieve.

        Returns
        ----------
        Node
            Graph node of this submodule if this parent module contains this
            submodule _or_ `None`.
        """

    def remove_global_attr_if_found(self, attr_name: str) -> None:
        """
        Record the global attribute (e.g., class, variable) with the passed
        name if previously recorded as defined by the pure-Python module
        corresponding to this graph node to be subsequently undefined by the
        same module.

        If this module is actually a package, this method instead records this
        attribute to be undefined by this package's pure-Python `__init__`
        submodule.

        This method is intended to be called on globals previously defined by
        this module that are subsequently undefined via the `del` built-in by
        this module, thus "forgetting" or "undoing" these globals.

        For safety, there exists no corresponding `remove_global_attr()`
        method. While defining this method is trivial, doing so would invite
        `KeyError` exceptions on scanning valid Python that lexically deletes a
        global in a scope under this module's top level (e.g., in a function)
        _before_ defining this global at this top level. Since `ModuleGraph`
        cannot and should not (re)implement a full-blown Python interpreter,
        ignoring out-of-order deletions is the only sane policy.

        Parameters
        ----------
        attr_name : str
            Unqualified name of the attribute to be removed.
        """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: _SupportsGraphident) -> bool: ...
    def __le__(self, other: _SupportsGraphident) -> bool: ...
    def __gt__(self, other: _SupportsGraphident) -> bool: ...
    def __ge__(self, other: _SupportsGraphident) -> bool: ...
    def infoTuple(self) -> tuple[str]: ...

class Alias(str):
    """
    Placeholder aliasing an existing source module to a non-existent target
    module (i.e., the desired alias).

    For obscure reasons, this class subclasses `str`. Each instance of this
    class is the fully-qualified name of the existing source module being
    aliased. Unlike the related `AliasNode` class, instances of this class are
    _not_ actual nodes and hence _not_ added to the graph; they only facilitate
    communication between the `ModuleGraph.alias_module()` and
    `ModuleGraph.find_node()` methods.
    """

class BaseModule(Node):
    filename: str
    packagepath: str
    def __init__(self, name: str, filename: str | None = None, path: str | None = None) -> None: ...
    # Returns a tuple of length 0, 1, 2, or 3
    def infoTuple(self) -> tuple[str, ...]: ...  # type: ignore[override]

class Package(BaseModule):
    """
    Graph node representing a non-namespace package.
    """
