"""
Define a modified ModuleGraph that can return its contents as a TOC and in other ways act like the old ImpTracker.
TODO: This class, along with TOC and Tree, should be in a separate module.

For reference, the ModuleGraph node types and their contents:

 nodetype         identifier        filename

 Script           full path to .py  full path to .py
 SourceModule     basename          full path to .py
 BuiltinModule    basename          None
 CompiledModule   basename          full path to .pyc
 Extension        basename          full path to .so
 MissingModule    basename          None
 Package          basename          full path to __init__.py
        packagepath is ['path to package']
        globalnames is set of global names __init__.py defines
 ExtensionPackage basename          full path to __init__.{so,dll}
        packagepath is ['path to package']

The main extension here over ModuleGraph is a method to extract nodes from the flattened graph and return them as a
TOC, or added to a TOC. Other added methods look up nodes by identifier and return facts about them, replacing what
the old ImpTracker list could do.
"""

# https://pyinstaller.org/en/stable/hooks.html#the-pre-safe-import-module-psim-api-method

# The documentation explicitly mentions that "Normally you do not need to know about the module-graph."
# However, some PyiModuleGraph typed class attributes are still documented as existing in imphookapi.
from _typeshed import Incomplete, StrPath, SupportsKeysAndGetItem
from collections.abc import Iterable
from typing_extensions import TypeAlias

from PyInstaller.lib.modulegraph.modulegraph import Alias, Node

_LazyNode: TypeAlias = Iterable[Node] | Iterable[str] | Alias | None
# from altgraph.Graph import Graph
_Graph: TypeAlias = Incomplete

class PyiModuleGraph:  # incomplete
    """
    Directed graph whose nodes represent modules and edges represent dependencies between these modules.

    This high-level subclass wraps the lower-level `ModuleGraph` class with support for graph and runtime hooks.
    While each instance of `ModuleGraph` represents a set of disconnected trees, each instance of this class *only*
    represents a single connected tree whose root node is the Python script originally passed by the user on the
    command line. For that reason, while there may (and typically do) exist more than one `ModuleGraph` instance,
    there typically exists only a singleton instance of this class.

    Attributes
    ----------
    _hooks : ModuleHookCache
        Dictionary mapping the fully-qualified names of all modules with normal (post-graph) hooks to the absolute paths
        of such hooks. See the the `_find_module_path()` method for details.
    _hooks_pre_find_module_path : ModuleHookCache
        Dictionary mapping the fully-qualified names of all modules with pre-find module path hooks to the absolute
        paths of such hooks. See the the `_find_module_path()` method for details.
    _hooks_pre_safe_import_module : ModuleHookCache
        Dictionary mapping the fully-qualified names of all modules with pre-safe import module hooks to the absolute
        paths of such hooks. See the `_safe_import_module()` method for details.
    _user_hook_dirs : list
        List of the absolute paths of all directories containing user-defined hooks for the current application.
    _excludes : list
        List of module names to be excluded when searching for dependencies.
    _additional_files_cache : AdditionalFilesCache
        Cache of all external dependencies (e.g., binaries, datas) listed in hook scripts for imported modules.
    _module_collection_mode : dict
        A dictionary of module/package collection mode settings set by hook scripts for their modules.
    _bindepend_symlink_suppression : set
        A set of paths or path patterns corresponding to shared libraries for which binary dependency analysis should
        not create symbolic links into top-level application directory.
    _base_modules: list
        Dependencies for `base_library.zip` (which remain the same for every executable).
    """

    def __init__(
        self,
        pyi_homepath: str,
        user_hook_dirs: Iterable[StrPath] = (),
        excludes: Iterable[str] = (),
        *,
        path: Iterable[str] | None = None,
        replace_paths: Iterable[tuple[StrPath, StrPath]] = ...,
        implies: SupportsKeysAndGetItem[str, _LazyNode] | Iterable[tuple[str, _LazyNode]] = ...,
        graph: _Graph | None = None,
        debug: bool = False,
    ) -> None: ...
