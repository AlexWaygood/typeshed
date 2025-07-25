"""Automatic discovery of Python modules and packages (for inclusion in the
distribution) and other config values.

For the purposes of this module, the following nomenclature is used:

- "src-layout": a directory representing a Python project that contains a "src"
  folder. Everything under the "src" folder is meant to be included in the
  distribution when packaging the project. Example::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── src/
        └── mypkg/
            ├── __init__.py
            ├── mymodule.py
            └── my_data_file.txt

- "flat-layout": a Python project that does not use "src-layout" but instead
  have a directory under the project root for each package::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── mypkg/
        ├── __init__.py
        ├── mymodule.py
        └── my_data_file.txt

- "single-module": a project that contains a single Python script direct under
  the project root (no directory used)::

    .
    ├── tox.ini
    ├── pyproject.toml
    └── mymodule.py

"""

import itertools
from _typeshed import Incomplete, StrPath
from collections.abc import Iterable, Mapping
from typing import ClassVar

from . import Distribution

chain_iter = itertools.chain.from_iterable

class _Filter:
    """
    Given a list of patterns, create a callable that will be true only if
    the input matches at least one of the patterns.
    """

    def __init__(self, *patterns: str) -> None: ...
    def __call__(self, item: str) -> bool: ...
    def __contains__(self, item: str) -> bool: ...

class _Finder:
    """Base class that exposes functionality for module/package finders"""

    ALWAYS_EXCLUDE: ClassVar[tuple[str, ...]]
    DEFAULT_EXCLUDE: ClassVar[tuple[str, ...]]
    @classmethod
    def find(cls, where: StrPath = ".", exclude: Iterable[str] = (), include: Iterable[str] = ("*",)) -> list[str]:
        """Return a list of all Python items (packages or modules, depending on
        the finder implementation) found within directory 'where'.

        'where' is the root directory which will be searched.
        It should be supplied as a "cross-platform" (i.e. URL-style) path;
        it will be converted to the appropriate local path syntax.

        'exclude' is a sequence of names to exclude; '*' can be used
        as a wildcard in the names.
        When finding packages, 'foo.*' will exclude all subpackages of 'foo'
        (but not 'foo' itself).

        'include' is a sequence of names to include.
        If it's specified, only the named items will be included.
        If it's not specified, all found items will be included.
        'include' can contain shell style wildcard patterns just like
        'exclude'.
        """

class PackageFinder(_Finder):
    """
    Generate a list of all Python packages found within a directory
    """

    ALWAYS_EXCLUDE: ClassVar[tuple[str, ...]]

class PEP420PackageFinder(PackageFinder): ...

class ModuleFinder(_Finder):
    """Find isolated Python modules.
    This function will **not** recurse subdirectories.
    """

class FlatLayoutPackageFinder(PEP420PackageFinder):
    DEFAULT_EXCLUDE: ClassVar[tuple[str, ...]]

class FlatLayoutModuleFinder(ModuleFinder):
    DEFAULT_EXCLUDE: ClassVar[tuple[str, ...]]

class ConfigDiscovery:
    """Fill-in metadata and options that can be automatically derived
    (from other metadata/options, the file system or conventions)
    """

    dist: Incomplete
    def __init__(self, distribution: Distribution) -> None: ...
    def __call__(self, force: bool = False, name: bool = True, ignore_ext_modules: bool = False) -> None:
        """Automatically discover missing configuration fields
        and modifies the given ``distribution`` object in-place.

        Note that by default this will only have an effect the first time the
        ``ConfigDiscovery`` object is called.

        To repeatedly invoke automatic discovery (e.g. when the project
        directory changes), please use ``force=True`` (or create a new
        ``ConfigDiscovery`` instance).
        """

    def analyse_name(self) -> None:
        """The packages/modules are the essential contribution of the author.
        Therefore the name of the distribution can be derived from them.
        """

def remove_nested_packages(packages: list[str]) -> list[str]:
    """Remove nested packages from a list of packages.

    >>> remove_nested_packages(["a", "a.b1", "a.b2", "a.b1.c1"])
    ['a']
    >>> remove_nested_packages(["a", "b", "c.d", "c.d.e.f", "g.h", "a.a1"])
    ['a', 'b', 'c.d', 'g.h']
    """

def remove_stubs(packages: list[str]) -> list[str]:
    """Remove type stubs (:pep:`561`) from a list of packages.

    >>> remove_stubs(["a", "a.b", "a-stubs", "a-stubs.b.c", "b", "c-stubs"])
    ['a', 'a.b', 'b']
    """

def find_parent_package(packages: list[str], package_dir: Mapping[str, str], root_dir: StrPath) -> str | None:
    """Find the parent package that is not a namespace."""

def find_package_path(name: str, package_dir: Mapping[str, str], root_dir: StrPath) -> str:
    """Given a package name, return the path where it should be found on
    disk, considering the ``package_dir`` option.

    >>> path = find_package_path("my.pkg", {"": "root/is/nested"}, ".")
    >>> path.replace(os.sep, "/")
    './root/is/nested/my/pkg'

    >>> path = find_package_path("my.pkg", {"my": "root/is/nested"}, ".")
    >>> path.replace(os.sep, "/")
    './root/is/nested/pkg'

    >>> path = find_package_path("my.pkg", {"my.pkg": "root/is/nested"}, ".")
    >>> path.replace(os.sep, "/")
    './root/is/nested'

    >>> path = find_package_path("other.pkg", {"my.pkg": "root/is/nested"}, ".")
    >>> path.replace(os.sep, "/")
    './other/pkg'
    """

def construct_package_dir(packages: list[str], package_path: StrPath) -> dict[str, str]: ...
