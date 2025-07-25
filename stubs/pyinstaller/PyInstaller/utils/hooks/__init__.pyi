# https://pyinstaller.org/en/stable/hooks.html

from _typeshed import StrOrBytesPath, StrPath
from collections.abc import Callable, Iterable
from typing import Any, Final, Literal

from PyInstaller import HOMEPATH as HOMEPATH
from PyInstaller.depend.imphookapi import PostGraphAPI
from PyInstaller.utils.hooks import conda

conda_support = conda

PY_IGNORE_EXTENSIONS: Final[set[str]]
hook_variables: dict[str, str]

def exec_statement(statement: str) -> str | int:
    """
    Execute a single Python statement in an externally-spawned interpreter, and return the resulting standard output
    as a string.

    Examples::

        tk_version = exec_statement("from _tkinter import TK_VERSION; print(TK_VERSION)")

        mpl_data_dir = exec_statement("import matplotlib; print(matplotlib.get_data_path())")
        datas = [ (mpl_data_dir, "") ]

    Notes:
        As of v5.0, usage of this function is discouraged in favour of the
        new :mod:`PyInstaller.isolated` module.

    """

def exec_statement_rc(statement: str) -> str | int:
    """
    Executes a Python statement in an externally spawned interpreter, and returns the exit code.
    """

def eval_statement(statement: str) -> Any | Literal[""]:
    """
    Execute a single Python statement in an externally-spawned interpreter, and :func:`eval` its output (if any).

    Example::

      databases = eval_statement('''
         import sqlalchemy.databases
         print(sqlalchemy.databases.__all__)
         ''')
      for db in databases:
         hiddenimports.append("sqlalchemy.databases." + db)

    Notes:
        As of v5.0, usage of this function is discouraged in favour of the
        new :mod:`PyInstaller.isolated` module.

    """

def get_pyextension_imports(module_name: str) -> list[str]:
    """
    Return list of modules required by binary (C/C++) Python extension.

    Python extension files ends with .so (Unix) or .pyd (Windows). It is almost impossible to analyze binary extension
    and its dependencies.

    Module cannot be imported directly.

    Let's at least try import it in a subprocess and observe the difference in module list from sys.modules.

    This function could be used for 'hiddenimports' in PyInstaller hooks files.
    """

def get_homebrew_path(formula: str = "") -> str | None:
    """
    Return the homebrew path to the requested formula, or the global prefix when called with no argument.

    Returns the path as a string or None if not found.
    """

def remove_prefix(string: str, prefix: str) -> str:
    """
    This function removes the given prefix from a string, if the string does indeed begin with the prefix; otherwise,
    it returns the original string.
    """

def remove_suffix(string: str, suffix: str) -> str:
    """
    This function removes the given suffix from a string, if the string does indeed end with the suffix; otherwise,
    it returns the original string.
    """

def remove_file_extension(filename: str) -> str:
    """
    This function returns filename without its extension.

    For Python C modules it removes even whole '.cpython-34m.so' etc.
    """

def can_import_module(module_name: str) -> bool:
    """
    Check if the specified module can be imported.

    Intended as a silent module availability check, as it does not print ModuleNotFoundError traceback to stderr when
    the module is unavailable.

    Parameters
    ----------
    module_name : str
        Fully-qualified name of the module.

    Returns
    ----------
    bool
        Boolean indicating whether the module can be imported or not.
    """

def get_module_attribute(module_name: str, attr_name: str) -> Any:
    """
    Get the string value of the passed attribute from the passed module if this attribute is defined by this module
    _or_ raise `AttributeError` otherwise.

    Since modules cannot be directly imported during analysis, this function spawns a subprocess importing this module
    and returning the string value of this attribute in this module.

    Parameters
    ----------
    module_name : str
        Fully-qualified name of this module.
    attr_name : str
        Name of the attribute in this module to be retrieved.

    Returns
    ----------
    str
        String value of this attribute.

    Raises
    ----------
    AttributeError
        If this attribute is undefined.
    """

def get_module_file_attribute(package: str) -> str | None:
    """
    Get the absolute path to the specified module or package.

    Modules and packages *must not* be directly imported in the main process during the analysis. Therefore, to
    avoid leaking the imports, this function uses an isolated subprocess when it needs to import the module and
    obtain its ``__file__`` attribute.

    Parameters
    ----------
    package : str
        Fully-qualified name of module or package.

    Returns
    ----------
    str
        Absolute path of this module.
    """

def get_pywin32_module_file_attribute(module_name: str) -> str | None:
    """
    Get the absolute path of the PyWin32 DLL specific to the PyWin32 module with the passed name (`pythoncom`
    or `pywintypes`).

    On import, each PyWin32 module:

    * Imports a DLL specific to that module.
    * Overwrites the values of all module attributes with values specific to that DLL. This includes that module's
      `__file__` attribute, which then provides the absolute path of that DLL.

    This function imports the module in isolated subprocess and retrieves its `__file__` attribute.
    """

def check_requirement(requirement: str) -> bool:
    """
    Check if a :pep:`0508` requirement is satisfied. Usually used to check if a package distribution is installed,
    or if it is installed and satisfies the specified version requirement.

    Parameters
    ----------
    requirement : str
        Requirement string in :pep:`0508` format.

    Returns
    ----------
    bool
        Boolean indicating whether the requirement is satisfied or not.

    Examples
    --------

    ::

        # Assume Pillow 10.0.0 is installed.
        >>> from PyInstaller.utils.hooks import check_requirement
        >>> check_requirement('Pillow')
        True
        >>> check_requirement('Pillow < 9.0')
        False
        >>> check_requirement('Pillow >= 9.0, < 11.0')
        True
    """

def is_module_satisfies(requirements: str, version: None = None, version_attr: None = None) -> bool:
    """
    A compatibility wrapper for :func:`check_requirement`, intended for backwards compatibility with existing hooks.

    In contrast to original implementation from PyInstaller < 6, this implementation only checks the specified
    :pep:`0508` requirement string; i.e., it tries to retrieve the distribution metadata, and compare its version
    against optional version specifier(s). It does not attempt to fall back to checking the module's version attribute,
    nor does it support ``version`` and ``version_attr`` arguments.

    Parameters
    ----------
    requirements : str
        Requirements string passed to the :func:`check_requirement`.
    version : None
        Deprecated and unsupported. Must be ``None``.
    version_attr : None
        Deprecated and unsupported. Must be ``None``.

    Returns
    ----------
    bool
        Boolean indicating whether the requirement is satisfied or not.

    Raises
    ----------
    ValueError
        If either ``version`` or ``version_attr`` are specified and are not None.
    """

def is_package(module_name: str) -> bool:
    """
    Check if a Python module is really a module or is a package containing other modules, without importing anything
    in the main process.

    :param module_name: Module name to check.
    :return: True if module is a package else otherwise.
    """

def get_all_package_paths(package: str) -> list[str]:
    """
    Given a package name, return all paths associated with the package. Typically, packages have a single location
    path, but PEP 420 namespace packages may be split across multiple locations. Returns an empty list if the specified
    package is not found or is not a package.
    """

def package_base_path(package_path: str, package: str) -> str:
    """
    Given a package location path and package name, return the package base path, i.e., the directory in which the
    top-level package is located. For example, given the path ``/abs/path/to/python/libs/pkg/subpkg`` and
    package name ``pkg.subpkg``, the function returns ``/abs/path/to/python/libs``.
    """

def get_package_paths(package: str) -> tuple[str, str]:
    """
    Given a package, return the path to packages stored on this machine and also returns the path to this particular
    package. For example, if pkg.subpkg lives in /abs/path/to/python/libs, then this function returns
    ``(/abs/path/to/python/libs, /abs/path/to/python/libs/pkg/subpkg)``.

    NOTE: due to backwards compatibility, this function returns only one package path along with its base directory.
    In case of PEP 420 namespace package with multiple location, only first location is returned. To obtain all
    package paths, use the ``get_all_package_paths`` function and obtain corresponding base directories using the
    ``package_base_path`` helper.
    """

def collect_submodules(
    package: str, filter: Callable[[str], bool] = ..., on_error: Literal["ignore", "warn once", "warn", "raise"] = "warn once"
) -> list[str]:
    """
    List all submodules of a given package.

    Arguments:
        package:
            An ``import``-able package.
        filter:
            Filter the submodules found: A callable that takes a submodule name and returns True if it should be
            included.
        on_error:
            The action to take when a submodule fails to import. May be any of:

            - raise: Errors are reraised and terminate the build.
            - warn: Errors are downgraded to warnings.
            - warn once: The first error issues a warning but all
              subsequent errors are ignored to minimise *stderr pollution*. This
              is the default.
            - ignore: Skip all errors. Don't warn about anything.
    Returns:
        All submodules to be assigned to ``hiddenimports`` in a hook.

    This function is intended to be used by hook scripts, not by main PyInstaller code.

    Examples::

        # Collect all submodules of Sphinx don't contain the word ``test``.
        hiddenimports = collect_submodules(
            "Sphinx", ``filter=lambda name: 'test' not in name)

    .. versionchanged:: 4.5
        Add the **on_error** parameter.

    """

def is_module_or_submodule(name: str, mod_or_submod: str) -> bool:
    """
    This helper function is designed for use in the ``filter`` argument of :func:`collect_submodules`, by returning
    ``True`` if the given ``name`` is a module or a submodule of ``mod_or_submod``.

    Examples:

        The following excludes ``foo.test`` and ``foo.test.one`` but not ``foo.testifier``. ::

            collect_submodules('foo', lambda name: not is_module_or_submodule(name, 'foo.test'))``
    """

PY_DYLIB_PATTERNS: Final[list[str]]

def collect_dynamic_libs(
    package: str, destdir: object = None, search_patterns: Iterable[str] = ["*.dll", "*.dylib", "lib*.so"]
) -> list[tuple[str, str]]:
    """
    This function produces a list of (source, dest) of dynamic library files that reside in package. Its output can be
    directly assigned to ``binaries`` in a hook script. The package parameter must be a string which names the package.

    :param destdir: Relative path to ./dist/APPNAME where the libraries should be put.
    :param search_patterns: List of dynamic library filename patterns to collect.
    """

def collect_data_files(
    package: str,
    include_py_files: bool = False,
    subdir: StrPath | None = None,
    excludes: Iterable[str] | None = None,
    includes: Iterable[str] | None = None,
) -> list[tuple[str, str]]:
    """
    This function produces a list of ``(source, dest)`` entries for data files that reside in ``package``.
    Its output can be directly assigned to ``datas`` in a hook script; for example, see ``hook-sphinx.py``.
    The data files are all files that are not shared libraries / binary python extensions (based on extension
    check) and are not python source (.py) files or byte-compiled modules (.pyc). Collection of the .py and .pyc
    files can be toggled via the ``include_py_files`` flag.
    Parameters:

    -   The ``package`` parameter is a string which names the package.
    -   By default, python source files and byte-compiled modules (files with ``.py`` and ``.pyc`` suffix) are not
        collected; setting the ``include_py_files`` argument to ``True`` collects these files as well. This is typically
        used when a package requires source .py files to be available; for example, JIT compilation used in
        deep-learning frameworks, code that requires access to .py files (for example, to check their date), or code
        that tries to extend `sys.path` with subpackage paths in a way that is incompatible with PyInstaller's frozen
        importer.. However, in contemporary PyInstaller versions, the preferred way of collecting source .py files is by
        using the **module collection mode** setting (which enables collection of source .py files in addition to or
        in lieu of collecting byte-compiled modules into PYZ archive).
    -   The ``subdir`` argument gives a subdirectory relative to ``package`` to search, which is helpful when submodules
        are imported at run-time from a directory lacking ``__init__.py``.
    -   The ``excludes`` argument contains a sequence of strings or Paths. These provide a list of
        `globs <https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob>`_
        to exclude from the collected data files; if a directory matches the provided glob, all files it contains will
        be excluded as well. All elements must be relative paths, which are relative to the provided package's path
        (/ ``subdir`` if provided).

        Therefore, ``*.txt`` will exclude only ``.txt`` files in ``package``\\ 's path, while ``**/*.txt`` will exclude
        all ``.txt`` files in ``package``\\ 's path and all its subdirectories. Likewise, ``**/__pycache__`` will exclude
        all files contained in any subdirectory named ``__pycache__``.
    -   The ``includes`` function like ``excludes``, but only include matching paths. ``excludes`` override
        ``includes``: a file or directory in both lists will be excluded.

    This function does not work on zipped Python eggs.

    This function is intended to be used by hook scripts, not by main PyInstaller code.
    """

def collect_system_data_files(path: str, destdir: StrPath | None = None, include_py_files: bool = False) -> list[tuple[str, str]]:
    """
    This function produces a list of (source, dest) non-Python (i.e., data) files that reside somewhere on the system.
    Its output can be directly assigned to ``datas`` in a hook script.

    This function is intended to be used by hook scripts, not by main PyInstaller code.
    """

def copy_metadata(package_name: str, recursive: bool = False) -> list[tuple[str, str]]:
    """
    Collect distribution metadata so that ``importlib.metadata.distribution()`` or ``pkg_resources.get_distribution()``
    can find it.

    This function returns a list to be assigned to the ``datas`` global variable. This list instructs PyInstaller to
    copy the metadata for the given package to the frozen application's data directory.

    Parameters
    ----------
    package_name : str
        Specifies the name of the package for which metadata should be copied.
    recursive : bool
        If true, collect metadata for the package's dependencies too. This enables use of
        ``importlib.metadata.requires('package')`` or ``pkg_resources.require('package')`` inside the frozen
        application.

    Returns
    -------
    list
        This should be assigned to ``datas``.

    Examples
    --------
        >>> from PyInstaller.utils.hooks import copy_metadata
        >>> copy_metadata('sphinx')
        [('c:\\python27\\lib\\site-packages\\Sphinx-1.3.2.dist-info',
          'Sphinx-1.3.2.dist-info')]


    Some packages rely on metadata files accessed through the ``importlib.metadata`` (or the now-deprecated
    ``pkg_resources``) module. PyInstaller does not collect these metadata files by default.
    If a package fails without the metadata (either its own, or of another package that it depends on), you can use this
    function in a hook to collect the corresponding metadata files into the frozen application. The tuples in the
    returned list contain two strings. The first is the full path to the package's metadata directory on the system. The
    second is the destination name, which typically corresponds to the basename of the metadata directory. Adding these
    tuples the the ``datas`` hook global variable, the metadata is collected into top-level application directory (where
    it is usually searched for).

    .. versionchanged:: 4.3.1

        Prevent ``dist-info`` metadata folders being renamed to ``egg-info`` which broke ``pkg_resources.require`` with
        *extras* (see :issue:`#3033`).

    .. versionchanged:: 4.4.0

        Add the **recursive** option.
    """

def get_installer(dist_name: str) -> str | None:
    """
    Try to find which package manager installed the specified distribution (e.g., pip, conda, rpm) by reading INSTALLER
    file from distribution's metadata.

    If the specified distribution does not exist, fall back to treating the passed name as importable package/module
    name, and attempt to look up its associated distribution name; this matches the behavior of implementation found
    in older PyInstaller versions (<= v6.12.0).

    :param dist_name: Name of distribution to look up
    :return: Name of package manager or None

    .. versionchanged:: 6.13
        The passed name is now first treated as a distribution name (direct look-up), and only if that fails, it is
        treated as importable package/module name.
    """

def collect_all(
    package_name: str,
    include_py_files: bool = True,
    filter_submodules: Callable[[str], bool] = ...,
    exclude_datas: Iterable[str] | None = None,
    include_datas: Iterable[str] | None = None,
    on_error: Literal["ignore", "warn once", "warn", "raise"] = "warn once",
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[str]]:
    """
    Collect everything for a given package name.

    Arguments:
        package_name:
            An ``import``-able package name.
        include_py_files:
            Forwarded to :func:`collect_data_files`.
        filter_submodules:
            Forwarded to :func:`collect_submodules`.
        exclude_datas:
            Forwarded to :func:`collect_data_files`.
        include_datas:
            Forwarded to :func:`collect_data_files`.
        on_error:
            Forwarded onto :func:`collect_submodules`.

    Returns:
        tuple: A ``(datas, binaries, hiddenimports)`` triplet containing:

        - All data files, raw Python files (if **include_py_files**), and distribution metadata directories (if
          applicable).
        - All dynamic libraries as returned by :func:`collect_dynamic_libs`.
        - All submodules of **package_name**.

    Typical use::

        datas, binaries, hiddenimports = collect_all('my_package_name')
    """

def collect_entry_point(name: str) -> tuple[list[tuple[str, str]], list[str]]:
    """
    Collect modules and metadata for all exporters of a given entry point.

    Args:
        name:
            The name of the entry point. Check the documentation for the library that uses the entry point to find
            its name.
    Returns:
        A ``(datas, hiddenimports)`` pair that should be assigned to the ``datas`` and ``hiddenimports``, respectively.

    For libraries, such as ``pytest`` or ``keyring``, that rely on plugins to extend their behaviour.

    Examples:
        Pytest uses an entry point called ``'pytest11'`` for its extensions.
        To collect all those extensions use::

            datas, hiddenimports = collect_entry_point("pytest11")

        These values may be used in a hook or added to the ``datas`` and ``hiddenimports`` arguments in the ``.spec``
        file. See :ref:`using spec files`.

    .. versionadded:: 4.3
    """

def get_hook_config(hook_api: PostGraphAPI, module_name: str, key: str) -> None:
    """
    Get user settings for hooks.

    Args:
        module_name:
            The module/package for which the key setting belong to.
        key:
            A key for the config.
    Returns:
        The value for the config. ``None`` if not set.

    The ``get_hook_config`` function will lookup settings in the ``Analysis.hooksconfig`` dict.

    The hook settings can be added to ``.spec`` file in the form of::

        a = Analysis(["my-app.py"],
            ...
            hooksconfig = {
                "gi": {
                    "icons": ["Adwaita"],
                    "themes": ["Adwaita"],
                    "languages": ["en_GB", "zh_CN"],
                },
            },
            ...
        )
    """

def include_or_exclude_file(
    filename: StrOrBytesPath,
    include_list: Iterable[StrOrBytesPath] | None = None,
    exclude_list: Iterable[StrOrBytesPath] | None = None,
) -> bool:
    """
    Generic inclusion/exclusion decision function based on filename and list of include and exclude patterns.

    Args:
        filename:
            Filename considered for inclusion.
        include_list:
            List of inclusion file patterns.
        exclude_list:
            List of exclusion file patterns.

    Returns:
        A boolean indicating whether the file should be included or not.

    If ``include_list`` is provided, True is returned only if the filename matches one of include patterns (and does not
    match any patterns in ``exclude_list``, if provided). If ``include_list`` is not provided, True is returned if
    filename does not match any patterns in ``exclude list``, if provided. If neither list is provided, True is
    returned for any filename.
    """

def collect_delvewheel_libs_directory(
    package_name: str,
    libdir_name: StrPath | None = None,
    datas: list[tuple[str, str]] | None = None,
    binaries: list[tuple[str, str]] | None = None,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Collect data files and binaries from the .libs directory of a delvewheel-enabled python wheel. Such wheels ship
    their shared libraries in a .libs directory that is located next to the package directory, and therefore falls
    outside the purview of the collect_dynamic_libs() utility function.

    Args:
        package_name:
            Name of the package (e.g., scipy).
        libdir_name:
            Optional name of the .libs directory (e.g., scipy.libs). If not provided, ".libs" is added to
            ``package_name``.
        datas:
            Optional list of datas to which collected data file entries are added. The combined result is retuned
            as part of the output tuple.
        binaries:
            Optional list of binaries to which collected binaries entries are added. The combined result is retuned
            as part of the output tuple.

    Returns:
        tuple: A ``(datas, binaries)`` pair that should be assigned to the ``datas`` and ``binaries``, respectively.

    Examples:
        Collect the ``scipy.libs`` delvewheel directory belonging to the Windows ``scipy`` wheel::

            datas, binaries = collect_delvewheel_libs_directory("scipy")

        When the collected entries should be added to existing ``datas`` and ``binaries`` listst, the following form
        can be used to avoid using intermediate temporary variables and merging those into existing lists::

            datas, binaries = collect_delvewheel_libs_directory("scipy", datas=datas, binaries=binaries)

    .. versionadded:: 5.6
    """
