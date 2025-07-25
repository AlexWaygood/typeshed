"""
Additional helper methods for working specifically with Anaconda distributions are found at
:mod:`PyInstaller.utils.hooks.conda_support<PyInstaller.utils.hooks.conda>`
which is designed to mimic (albeit loosely) the `importlib.metadata`_ package. These functions find and parse the
distribution metadata from json files located in the ``conda-meta`` directory.

.. versionadded:: 4.2.0

This module is available only if run inside a Conda environment. Usage of this module should therefore be wrapped in
a conditional clause::

    from PyInstaller.compat import is_pure_conda

    if is_pure_conda:
        from PyInstaller.utils.hooks import conda_support

        # Code goes here. e.g.
        binaries = conda_support.collect_dynamic_libs("numpy")
        ...

Packages are all referenced by the *distribution name* you use to install it, rather than the *package name* you import
it with. I.e., use ``distribution("pillow")`` instead of ``distribution("PIL")`` or use ``package_distribution("PIL")``.
"""

# https://pyinstaller.org/en/stable/hooks.html#module-PyInstaller.utils.hooks.conda

from _typeshed import StrOrBytesPath
from collections.abc import Iterable
from importlib.metadata import PackagePath as _PackagePath
from pathlib import Path
from typing import Final, TypedDict

CONDA_ROOT: Final[Path]
CONDA_META_DIR: Final[Path]
PYTHONPATH_PREFIXES: Final[list[Path]]

class _RawDict(TypedDict):
    name: str
    version: str
    files: list[StrOrBytesPath]
    depends: list[str]

class Distribution:
    """
    A bucket class representation of a Conda distribution.

    This bucket exports the following attributes:

    :ivar name: The distribution's name.
    :ivar version: Its version.
    :ivar files: All filenames as :meth:`PackagePath`\\ s included with this distribution.
    :ivar dependencies: Names of other distributions that this distribution depends on (with version constraints
                        removed).
    :ivar packages: Names of importable packages included in this distribution.

    This class is not intended to be constructed directly by users. Rather use :meth:`distribution` or
    :meth:`package_distribution` to provide one for you.
    """

    raw: _RawDict
    name: str
    version: str
    files: list[PackagePath]
    dependencies: list[str]
    packages: list[str]
    def __init__(self, json_path: str) -> None: ...
    @classmethod
    def from_name(cls, name: str) -> Distribution:
        """
        Get distribution information for a given distribution **name** (i.e., something you would ``conda install``).

        :rtype: :class:`Distribution`
        """

    @classmethod
    def from_package_name(cls, name: str) -> Distribution:
        """
        Get distribution information for a **package** (i.e., something you would import).

        :rtype: :class:`Distribution`

        For example, the package ``pkg_resources`` belongs to the distribution ``setuptools``, which contains three
        packages.

        >>> package_distribution("pkg_resources")
        Distribution(name="setuptools",
                     packages=['easy_install', 'pkg_resources', 'setuptools'])
        """

# distribution and package_distribution are meant to be used and are not internal helpers
distribution = Distribution.from_name
package_distribution = Distribution.from_package_name

class PackagePath(_PackagePath):
    """
    A filename relative to Conda's root (``sys.prefix``).

    This class inherits from :class:`pathlib.PurePosixPath` even on non-Posix OSs. To convert to a :class:`pathlib.Path`
    pointing to the real file, use the :meth:`locate` method.
    """

    def locate(self) -> Path:
        """
        Return a path-like object for this path pointing to the file's true location.
        """

def walk_dependency_tree(initial: str, excludes: Iterable[str] | None = None) -> dict[str, Distribution]:
    """
    Collect a :class:`Distribution` and all direct and indirect dependencies of that distribution.

    Arguments:
        initial:
            Distribution name to collect from.
        excludes:
            Distributions to exclude.
    Returns:
        A ``{name: distribution}`` mapping where ``distribution`` is the output of
        :func:`conda_support.distribution(name) <distribution>`.
    """

def requires(name: str, strip_versions: bool = False) -> list[str]:
    """
    List requirements of a distribution.

    Arguments:
        name:
            The name of the distribution.
        strip_versions:
            List only their names, not their version constraints.
    Returns:
        A list of distribution names.
    """

def files(name: str, dependencies: bool = False, excludes: Iterable[str] | None = None) -> list[PackagePath]:
    """
    List all files belonging to a distribution.

    Arguments:
        name:
            The name of the distribution.
        dependencies:
            Recursively collect files of dependencies too.
        excludes:
            Distributions to ignore if **dependencies** is true.
    Returns:
        All filenames belonging to the given distribution.

    With ``dependencies=False``, this is just a shortcut for::

        conda_support.distribution(name).files
    """

def collect_dynamic_libs(
    name: str, dest: str = ".", dependencies: bool = True, excludes: Iterable[str] | None = None
) -> list[tuple[str, str]]:
    """
    Collect DLLs for distribution **name**.

    Arguments:
        name:
            The distribution's project-name.
        dest:
            Target destination, defaults to ``'.'``.
        dependencies:
            Recursively collect libs for dependent distributions (recommended).
        excludes:
            Dependent distributions to skip, defaults to ``None``.
    Returns:
        List of DLLs in PyInstaller's ``(source, dest)`` format.

    This collects libraries only from Conda's shared ``lib`` (Unix) or ``Library/bin`` (Windows) folders. To collect
    from inside a distribution's installation use the regular :func:`PyInstaller.utils.hooks.collect_dynamic_libs`.
    """

distributions: dict[str, Distribution]
distributions_by_package: dict[str | None, Distribution]
