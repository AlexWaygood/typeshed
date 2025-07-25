"""
Classes facilitating communication between PyInstaller and import hooks.

PyInstaller passes instances of classes defined by this module to corresponding functions defined by external import
hooks, which commonly modify the contents of these instances before returning. PyInstaller then detects and converts
these modifications into appropriate operations on the current `PyiModuleGraph` instance, thus modifying which
modules will be frozen into the executable.
"""

# https://pyinstaller.org/en/stable/hooks-config.html#adding-an-option-to-the-hook `hook_api` is a PostGraphAPI
# Nothing in this module is meant to be initialized externally.
# Instances are exposed through hooks during build.

from _typeshed import StrOrBytesPath
from collections.abc import Generator, Iterable
from types import CodeType
from typing import Literal

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import TOC
from PyInstaller.depend.analysis import PyiModuleGraph
from PyInstaller.lib.modulegraph.modulegraph import Package

# https://pyinstaller.org/en/stable/hooks.html#the-pre-safe-import-module-psim-api-method
class PreSafeImportModuleAPI:
    """
    Metadata communicating changes made by the current **pre-safe import module hook** (i.e., hook run immediately
    _before_ a call to `ModuleGraph._safe_import_module()` recursively adding the hooked module, package,
    or C extension and all transitive imports thereof to the module graph) back to PyInstaller.

    Pre-safe import module hooks _must_ define a `pre_safe_import_module()` function accepting an instance of this
    class, whose attributes describe the subsequent `ModuleGraph._safe_import_module()` call creating the hooked
    module's graph node.

    Each pre-safe import module hook is run _only_ on the first attempt to create the hooked module's graph node and
    then subsequently ignored. If this hook successfully creates that graph node, the subsequent
    `ModuleGraph._safe_import_module()` call will observe this fact and silently return without attempting to
    recreate that graph node.

    Pre-safe import module hooks are typically used to create graph nodes for **runtime modules** (i.e.,
    modules dynamically defined at runtime). Most modules are physically defined in external `.py`-suffixed scripts.
    Some modules, however, are dynamically defined at runtime (e.g., `six.moves`, dynamically defined by the
    physically defined `six.py` module). However, `ModuleGraph` only parses `import` statements residing in external
    scripts. `ModuleGraph` is _not_ a full-fledged, Turing-complete Python interpreter and hence has no means of
    parsing `import` statements performed by runtime modules existing only in-memory.

    'With great power comes great responsibility.'


    Attributes (Immutable)
    ----------------------------
    The following attributes are **immutable** (i.e., read-only). For safety, any attempts to change these attributes
    _will_ result in a raised exception:

    module_graph : PyiModuleGraph
        Current module graph.
    parent_package : Package
        Graph node for the package providing this module _or_ `None` if this module is a top-level module.

    Attributes (Mutable)
    -----------------------------
    The following attributes are editable.

    module_basename : str
        Unqualified name of the module to be imported (e.g., `text`).
    module_name : str
        Fully-qualified name of this module (e.g., `email.mime.text`).
    """

    module_basename: str
    module_name: str
    def __init__(
        self, module_graph: PyiModuleGraph, module_basename: str, module_name: str, parent_package: Package | None
    ) -> None: ...
    @property
    def module_graph(self) -> PyiModuleGraph:
        """
        Current module graph.
        """

    @property
    def parent_package(self) -> Package | None:
        """
        Parent Package of this node.
        """

    def add_runtime_module(self, module_name: str) -> None:
        """
        Add a graph node representing a non-package Python module with the passed name dynamically defined at runtime.

        Most modules are statically defined on-disk as standard Python files. Some modules, however, are dynamically
        defined in-memory at runtime (e.g., `gi.repository.Gst`, dynamically defined by the statically defined
        `gi.repository.__init__` module).

        This method adds a graph node representing such a runtime module. Since this module is _not_ a package,
        all attempts to import submodules from this module in `from`-style import statements (e.g., the `queue`
        submodule in `from six.moves import queue`) will be silently ignored. To circumvent this, simply call
        `add_runtime_package()` instead.

        Parameters
        ----------
        module_name : str
            Fully-qualified name of this module (e.g., `gi.repository.Gst`).

        Examples
        ----------
        This method is typically called by `pre_safe_import_module()` hooks, e.g.:

            def pre_safe_import_module(api):
                api.add_runtime_module(api.module_name)
        """

    def add_runtime_package(self, package_name: str) -> None:
        """
        Add a graph node representing a non-namespace Python package with the passed name dynamically defined at
        runtime.

        Most packages are statically defined on-disk as standard subdirectories containing `__init__.py` files. Some
        packages, however, are dynamically defined in-memory at runtime (e.g., `six.moves`, dynamically defined by
        the statically defined `six` module).

        This method adds a graph node representing such a runtime package. All attributes imported from this package
        in `from`-style import statements that are submodules of this package (e.g., the `queue` submodule in `from
        six.moves import queue`) will be imported rather than ignored.

        Parameters
        ----------
        package_name : str
            Fully-qualified name of this package (e.g., `six.moves`).

        Examples
        ----------
        This method is typically called by `pre_safe_import_module()` hooks, e.g.:

            def pre_safe_import_module(api):
                api.add_runtime_package(api.module_name)
        """

    def add_alias_module(self, real_module_name: str, alias_module_name: str) -> None:
        """
        Alias the source module to the target module with the passed names.

        This method ensures that the next call to findNode() given the target module name will resolve this alias.
        This includes importing and adding a graph node for the source module if needed as well as adding a reference
        from the target to the source module.

        Parameters
        ----------
        real_module_name : str
            Fully-qualified name of the **existing module** (i.e., the module being aliased).
        alias_module_name : str
            Fully-qualified name of the **non-existent module** (i.e., the alias to be created).
        """

    def append_package_path(self, directory: str) -> None:
        """
        Modulegraph does a good job at simulating Python's, but it cannot handle packagepath `__path__` modifications
        packages make at runtime.

        Therefore there is a mechanism whereby you can register extra paths in this map for a package, and it will be
        honored.

        Parameters
        ----------
        directory : str
            Absolute or relative path of the directory to be appended to this package's `__path__` attribute.
        """

# https://pyinstaller.org/en/stable/hooks.html#the-pre-find-module-path-pfmp-api-method
class PreFindModulePathAPI:
    """
    Metadata communicating changes made by the current **pre-find module path hook** (i.e., hook run immediately
    _before_ a call to `ModuleGraph._find_module_path()` finding the hooked module's absolute path) back to PyInstaller.

    Pre-find module path hooks _must_ define a `pre_find_module_path()` function accepting an instance of this class,
    whose attributes describe the subsequent `ModuleGraph._find_module_path()` call to be performed.

    Pre-find module path hooks are typically used to change the absolute path from which a module will be
    subsequently imported and thus frozen into the executable. To do so, hooks may overwrite the default
    `search_dirs` list of the absolute paths of all directories to be searched for that module: e.g.,

        def pre_find_module_path(api):
            api.search_dirs = ['/the/one/true/package/providing/this/module']

    Each pre-find module path hook is run _only_ on the first call to `ModuleGraph._find_module_path()` for the
    corresponding module.

    Attributes
    ----------
    The following attributes are **mutable** (i.e., modifiable). All changes to these attributes will be immediately
    respected by PyInstaller:

    search_dirs : list
        List of the absolute paths of all directories to be searched for this module (in order). Searching will halt
        at the first directory containing this module.

    Attributes (Immutable)
    ----------
    The following attributes are **immutable** (i.e., read-only). For safety, any attempts to change these attributes
    _will_ result in a raised exception:

    module_name : str
        Fully-qualified name of this module.
    module_graph : PyiModuleGraph
        Current module graph. For efficiency, this attribute is technically mutable. To preserve graph integrity,
        this attribute should nonetheless _never_ be modified. While read-only `PyiModuleGraph` methods (e.g.,
        `findNode()`) are safely callable from within pre-find module path hooks, methods modifying the graph are
        _not_. If graph modifications are required, consider an alternative type of hook (e.g., pre-import module
        hooks).
    """

    search_dirs: Iterable[StrOrBytesPath]
    def __init__(self, module_graph: PyiModuleGraph, module_name: str, search_dirs: Iterable[StrOrBytesPath]) -> None: ...
    @property
    def module_graph(self) -> PyiModuleGraph:
        """
        Current module graph.
        """

    @property
    def module_name(self) -> str:
        """
        Fully-qualified name of this module.
        """

# https://pyinstaller.org/en/stable/hooks.html#the-hook-hook-api-function
class PostGraphAPI:
    """
    Metadata communicating changes made by the current **post-graph hook** (i.e., hook run for a specific module
    transitively imported by the current application _after_ the module graph of all `import` statements performed by
    this application has been constructed) back to PyInstaller.

    Post-graph hooks may optionally define a `post_graph()` function accepting an instance of this class,
    whose attributes describe the current state of the module graph and the hooked module's graph node.

    Attributes (Mutable)
    ----------
    The following attributes are **mutable** (i.e., modifiable). All changes to these attributes will be immediately
    respected by PyInstaller:

    module_graph : PyiModuleGraph
        Current module graph.
    module : Node
        Graph node for the currently hooked module.

    'With great power comes great responsibility.'

    Attributes (Immutable)
    ----------
    The following attributes are **immutable** (i.e., read-only). For safety, any attempts to change these attributes
    _will_ result in a raised exception:

    __name__ : str
        Fully-qualified name of this module (e.g., `six.moves.tkinter`).
    __file__ : str
        Absolute path of this module. If this module is:
        * A standard (rather than namespace) package, this is the absolute path of this package's directory.
        * A namespace (rather than standard) package, this is the abstract placeholder `-`. (Don't ask. Don't tell.)
        * A non-package module or C extension, this is the absolute path of the corresponding file.
    __path__ : list
        List of the absolute paths of all directories comprising this package if this module is a package _or_ `None`
        otherwise. If this module is a standard (rather than namespace) package, this list contains only the absolute
        path of this package's directory.
    co : code
        Code object compiled from the contents of `__file__` (e.g., via the `compile()` builtin).
    analysis: build_main.Analysis
        The Analysis that load the hook.

    Attributes (Private)
    ----------
    The following attributes are technically mutable but private, and hence should _never_ be externally accessed or
    modified by hooks. Call the corresponding public methods instead:

    _added_datas : list
        List of the `(name, path)` 2-tuples or TOC objects of all external data files required by the current hook,
        defaulting to the empty list. This is equivalent to the global `datas` hook attribute.
    _added_imports : list
        List of the fully-qualified names of all modules imported by the current hook, defaulting to the empty list.
        This is equivalent to the global `hiddenimports` hook attribute.
    _added_binaries : list
        List of the `(name, path)` 2-tuples or TOC objects of all external C extensions imported by the current hook,
        defaulting to the empty list. This is equivalent to the global `binaries` hook attribute.
    _module_collection_mode : dict
        Dictionary of package/module names and their corresponding collection mode strings. This is equivalent to the
        global `module_collection_mode` hook attribute.
    _bindepend_symlink_suppression : set
        A set of paths or path patterns corresponding to shared libraries for which binary dependency analysis should
        not generate symbolic links into top-level application directory.
    """

    module_graph: PyiModuleGraph
    module: Package
    def __init__(self, module_name: str, module_graph: PyiModuleGraph, analysis: Analysis) -> None: ...
    @property
    def __file__(self) -> str:
        """
        Absolute path of this module's file.
        """

    @property
    def __path__(self) -> tuple[str, ...] | None:
        """
        List of the absolute paths of all directories comprising this package if this module is a package _or_ `None`
        otherwise. If this module is a standard (rather than namespace) package, this list contains only the absolute
        path of this package's directory.
        """

    @property
    def __name__(self) -> str:
        """
        Fully-qualified name of this module (e.g., `six.moves.tkinter`).
        """
    # Compiled code. See stdlib.builtins.compile
    @property
    def co(self) -> CodeType:
        """
        Code object compiled from the contents of `__file__` (e.g., via the `compile()` builtin).
        """

    @property
    def analysis(self) -> Analysis:
        """
        build_main.Analysis that calls the hook.
        """

    @property
    def name(self) -> str:
        """
        Fully-qualified name of this module (e.g., `six.moves.tkinter`).

        **This property has been deprecated by the `__name__` property.**
        """

    @property
    def graph(self) -> PyiModuleGraph:
        """
        Current module graph.

        **This property has been deprecated by the `module_graph` property.**
        """

    @property
    def node(self) -> Package:
        """
        Graph node for the currently hooked module.

        **This property has been deprecated by the `module` property.**
        """

    @property
    def imports(self) -> Generator[Package, None, None]:
        """
        List of the graph nodes of all modules directly imported by this module.
        """

    def add_imports(self, *module_names: str) -> None:
        """
        Add all Python modules whose fully-qualified names are in the passed list as "hidden imports" upon which the
        current module depends.

        This is equivalent to appending such names to the hook-specific `hiddenimports` attribute.
        """

    def del_imports(self, *module_names: str) -> None:
        """
        Remove the named fully-qualified modules from the set of imports (either hidden or visible) upon which the
        current module depends.

        This is equivalent to appending such names to the hook-specific `excludedimports` attribute.
        """

    def add_binaries(self, binaries: TOC | Iterable[tuple[StrOrBytesPath, StrOrBytesPath]]) -> None:
        """
        Add all external dynamic libraries in the passed list of `(src_name, dest_name)` 2-tuples as dependencies of the
        current module. This is equivalent to adding to the global `binaries` hook attribute.

        For convenience, the `binaries` may also be a list of TOC-style 3-tuples `(dest_name, src_name, typecode)`.
        """

    def add_datas(self, datas: TOC | Iterable[tuple[StrOrBytesPath, StrOrBytesPath]]) -> None:
        """
        Add all external data files in the passed list of `(src_name, dest_name)` 2-tuples as dependencies of the
        current module. This is equivalent to adding to the global `datas` hook attribute.

        For convenience, the `datas` may also be a list of TOC-style 3-tuples `(dest_name, src_name, typecode)`.
        """

    def set_module_collection_mode(self, name: str | None, mode: Literal["pyz", "pyc", "py", "pyz+py", "py+pyz"] | None) -> None:
        """ "
        Set the package/module collection mode for the specified module name. If `name` is `None`, the hooked
        module/package name is used. `mode` can be one of valid mode strings (`'pyz'`, `'pyc'`, `'py'`, `'pyz+py'`,
        `'py+pyz'`) or `None`, which clears the setting for the module/package - but only  within this hook's context!
        """

    def add_bindepend_symlink_suppression_pattern(self, pattern: str) -> None:
        """
        Add the given path or path pattern to the set of patterns that prevent binary dependency analysis from creating
        a symbolic link to the top-level application directory.
        """
