from _typeshed import Incomplete, StrPath
from collections.abc import Iterable, Iterator, MutableMapping
from importlib import metadata
from typing import Literal, TypeVar, overload

from . import Command, SetuptoolsDeprecationWarning
from ._distutils.cmd import Command as _Command
from ._distutils.dist import Distribution as _Distribution
from .command.alias import alias
from .command.bdist_egg import bdist_egg
from .command.bdist_rpm import bdist_rpm
from .command.bdist_wheel import bdist_wheel
from .command.build import build
from .command.build_clib import build_clib
from .command.build_ext import build_ext
from .command.build_py import build_py
from .command.develop import develop
from .command.dist_info import dist_info
from .command.easy_install import easy_install
from .command.editable_wheel import editable_wheel
from .command.egg_info import egg_info
from .command.install import install
from .command.install_egg_info import install_egg_info
from .command.install_lib import install_lib
from .command.install_scripts import install_scripts
from .command.rotate import rotate
from .command.saveopts import saveopts
from .command.sdist import sdist
from .command.setopt import setopt

_CommandT = TypeVar("_CommandT", bound=_Command)

__all__ = ["Distribution"]

class Distribution(_Distribution):
    """Distribution with support for tests and package data

    This is an enhanced version of 'distutils.dist.Distribution' that
    effectively adds the following new optional keyword arguments to 'setup()':

     'install_requires' -- a string or sequence of strings specifying project
        versions that the distribution requires when installed, in the format
        used by 'pkg_resources.require()'.  They will be installed
        automatically when the package is installed.  If you wish to use
        packages that are not available in PyPI, or want to give your users an
        alternate download location, you can add a 'find_links' option to the
        '[easy_install]' section of your project's 'setup.cfg' file, and then
        setuptools will scan the listed web pages for links that satisfy the
        requirements.

     'extras_require' -- a dictionary mapping names of optional "extras" to the
        additional requirement(s) that using those extras incurs. For example,
        this::

            extras_require = dict(reST = ["docutils>=0.3", "reSTedit"])

        indicates that the distribution can optionally provide an extra
        capability called "reST", but it can only be used if docutils and
        reSTedit are installed.  If the user installs your package using
        EasyInstall and requests one of your extras, the corresponding
        additional requirements will be installed if needed.

     'package_data' -- a dictionary mapping package names to lists of filenames
        or globs to use to find data files contained in the named packages.
        If the dictionary has filenames or globs listed under '""' (the empty
        string), those names will be searched for in every package, in addition
        to any names for the specific package.  Data files found using these
        names/globs will be installed along with the package, in the same
        location as the package.  Note that globs are allowed to reference
        the contents of non-package subdirectories, as long as you use '/' as
        a path separator.  (Globs are automatically converted to
        platform-specific paths at runtime.)

    In addition to these new keywords, this class also has several new methods
    for manipulating the distribution's contents.  For example, the 'include()'
    and 'exclude()' methods can be thought of as in-place add and subtract
    commands that add or remove packages, modules, extensions, and so on from
    the distribution.
    """

    include_package_data: bool | None
    exclude_package_data: dict[str, list[str]] | None
    src_root: str | None
    dependency_links: list[str]
    setup_requires: list[str]
    def __init__(self, attrs: MutableMapping[str, Incomplete] | None = None) -> None: ...
    def parse_config_files(self, filenames: Iterable[StrPath] | None = None, ignore_option_errors: bool = False) -> None: ...
    def fetch_build_eggs(self, requires: str | Iterable[str]) -> list[metadata.Distribution]:
        """Resolve pre-setup requirements"""

    def get_egg_cache_dir(self) -> str: ...
    def fetch_build_egg(self, req):
        """Fetch an egg needed for building"""
    # NOTE: Commands that setuptools doesn't re-expose are considered deprecated (they must be imported from distutils directly)
    # So we're not listing them here. This list comes directly from the setuptools/command folder. Minus the test command.
    @overload  # type: ignore[override]
    def get_command_obj(self, command: Literal["alias"], create: Literal[1, True] = 1) -> alias:
        """Return the command object for 'command'.  Normally this object
        is cached on a previous call to 'get_command_obj()'; if no command
        object for 'command' is in the cache, then we either create and
        return it (if 'create' is true) or return None.
        """

    @overload
    def get_command_obj(self, command: Literal["bdist_egg"], create: Literal[1, True] = 1) -> bdist_egg: ...
    @overload
    def get_command_obj(self, command: Literal["bdist_rpm"], create: Literal[1, True] = 1) -> bdist_rpm: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["bdist_wheel"], create: Literal[1, True] = 1) -> bdist_wheel: ...
    @overload
    def get_command_obj(self, command: Literal["build"], create: Literal[1, True] = 1) -> build: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["build_clib"], create: Literal[1, True] = 1) -> build_clib: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["build_ext"], create: Literal[1, True] = 1) -> build_ext: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["build_py"], create: Literal[1, True] = 1) -> build_py: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["develop"], create: Literal[1, True] = 1) -> develop: ...
    @overload
    def get_command_obj(self, command: Literal["dist_info"], create: Literal[1, True] = 1) -> dist_info: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["easy_install"], create: Literal[1, True] = 1) -> easy_install: ...
    @overload
    def get_command_obj(self, command: Literal["editable_wheel"], create: Literal[1, True] = 1) -> editable_wheel: ...
    @overload
    def get_command_obj(self, command: Literal["egg_info"], create: Literal[1, True] = 1) -> egg_info: ...
    @overload
    def get_command_obj(self, command: Literal["install"], create: Literal[1, True] = 1) -> install: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["install_egg_info"], create: Literal[1, True] = 1) -> install_egg_info: ...
    @overload
    def get_command_obj(self, command: Literal["install_lib"], create: Literal[1, True] = 1) -> install_lib: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["install_scripts"], create: Literal[1, True] = 1) -> install_scripts: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["rotate"], create: Literal[1, True] = 1) -> rotate: ...
    @overload
    def get_command_obj(self, command: Literal["saveopts"], create: Literal[1, True] = 1) -> saveopts: ...
    @overload
    def get_command_obj(self, command: Literal["sdist"], create: Literal[1, True] = 1) -> sdist: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_obj(self, command: Literal["setopt"], create: Literal[1, True] = 1) -> setopt: ...
    @overload
    def get_command_obj(self, command: str, create: Literal[1, True] = 1) -> Command: ...
    # Not replicating the overloads for "Command | None", user may use "isinstance"
    @overload
    def get_command_obj(self, command: str, create: Literal[0, False]) -> Command | None: ...
    @overload
    def get_command_class(self, command: Literal["alias"]) -> type[alias]:
        """Pluggable version of get_command_class()"""

    @overload
    def get_command_class(self, command: Literal["bdist_egg"]) -> type[bdist_egg]: ...
    @overload
    def get_command_class(self, command: Literal["bdist_rpm"]) -> type[bdist_rpm]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["bdist_wheel"]) -> type[bdist_wheel]: ...
    @overload
    def get_command_class(self, command: Literal["build"]) -> type[build]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["build_clib"]) -> type[build_clib]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["build_ext"]) -> type[build_ext]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["build_py"]) -> type[build_py]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["develop"]) -> type[develop]: ...
    @overload
    def get_command_class(self, command: Literal["dist_info"]) -> type[dist_info]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["easy_install"]) -> type[easy_install]: ...
    @overload
    def get_command_class(self, command: Literal["editable_wheel"]) -> type[editable_wheel]: ...
    @overload
    def get_command_class(self, command: Literal["egg_info"]) -> type[egg_info]: ...
    @overload
    def get_command_class(self, command: Literal["install"]) -> type[install]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["install_egg_info"]) -> type[install_egg_info]: ...
    @overload
    def get_command_class(self, command: Literal["install_lib"]) -> type[install_lib]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["install_scripts"]) -> type[install_scripts]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["rotate"]) -> type[rotate]: ...
    @overload
    def get_command_class(self, command: Literal["saveopts"]) -> type[saveopts]: ...
    @overload
    def get_command_class(self, command: Literal["sdist"]) -> type[sdist]: ...  # type: ignore[overload-overlap]
    @overload
    def get_command_class(self, command: Literal["setopt"]) -> type[setopt]: ...
    @overload
    def get_command_class(self, command: str) -> type[Command]: ...
    @overload  # type: ignore[override]
    def reinitialize_command(self, command: Literal["alias"], reinit_subcommands: bool = False) -> alias:
        """Reinitializes a command to the state it was in when first
        returned by 'get_command_obj()': ie., initialized but not yet
        finalized.  This provides the opportunity to sneak option
        values in programmatically, overriding or supplementing
        user-supplied values from the config files and command line.
        You'll have to re-finalize the command object (by calling
        'finalize_options()' or 'ensure_finalized()') before using it for
        real.

        'command' should be a command name (string) or command object.  If
        'reinit_subcommands' is true, also reinitializes the command's
        sub-commands, as declared by the 'sub_commands' class attribute (if
        it has one).  See the "install" command for an example.  Only
        reinitializes the sub-commands that actually matter, ie. those
        whose test predicates return true.

        Returns the reinitialized command object.
        """

    @overload
    def reinitialize_command(self, command: Literal["bdist_egg"], reinit_subcommands: bool = False) -> bdist_egg: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_rpm"], reinit_subcommands: bool = False) -> bdist_rpm: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["bdist_wheel"], reinit_subcommands: bool = False) -> bdist_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["build"], reinit_subcommands: bool = False) -> build: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["build_clib"], reinit_subcommands: bool = False) -> build_clib: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["build_ext"], reinit_subcommands: bool = False) -> build_ext: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["build_py"], reinit_subcommands: bool = False) -> build_py: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["develop"], reinit_subcommands: bool = False) -> develop: ...
    @overload
    def reinitialize_command(self, command: Literal["dist_info"], reinit_subcommands: bool = False) -> dist_info: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["easy_install"], reinit_subcommands: bool = False) -> easy_install: ...
    @overload
    def reinitialize_command(self, command: Literal["editable_wheel"], reinit_subcommands: bool = False) -> editable_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["egg_info"], reinit_subcommands: bool = False) -> egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install"], reinit_subcommands: bool = False) -> install: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(
        self, command: Literal["install_egg_info"], reinit_subcommands: bool = False
    ) -> install_egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install_lib"], reinit_subcommands: bool = False) -> install_lib: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["install_scripts"], reinit_subcommands: bool = False) -> install_scripts: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["rotate"], reinit_subcommands: bool = False) -> rotate: ...
    @overload
    def reinitialize_command(self, command: Literal["saveopts"], reinit_subcommands: bool = False) -> saveopts: ...
    @overload
    def reinitialize_command(self, command: Literal["sdist"], reinit_subcommands: bool = False) -> sdist: ...  # type: ignore[overload-overlap]
    @overload
    def reinitialize_command(self, command: Literal["setopt"], reinit_subcommands: bool = False) -> setopt: ...
    @overload
    def reinitialize_command(self, command: str, reinit_subcommands: bool = False) -> Command: ...
    @overload
    def reinitialize_command(self, command: _CommandT, reinit_subcommands: bool = False) -> _CommandT: ...
    def include(self, **attrs) -> None:
        """Add items to distribution that are named in keyword arguments

        For example, 'dist.include(py_modules=["x"])' would add 'x' to
        the distribution's 'py_modules' attribute, if it was not already
        there.

        Currently, this method only supports inclusion for attributes that are
        lists or tuples.  If you need to add support for adding to other
        attributes in this or a subclass, you can add an '_include_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'include()'.  So, 'dist.include(foo={"bar":"baz"})'
        will try to call 'dist._include_foo({"bar":"baz"})', which can then
        handle whatever special inclusion logic is needed.
        """

    def exclude_package(self, package: str) -> None:
        """Remove packages, modules, and extensions in named package"""

    def has_contents_for(self, package: str) -> bool:
        """Return true if 'exclude_package(package)' would do something"""

    def exclude(self, **attrs) -> None:
        """Remove items from distribution that are named in keyword arguments

        For example, 'dist.exclude(py_modules=["x"])' would remove 'x' from
        the distribution's 'py_modules' attribute.  Excluding packages uses
        the 'exclude_package()' method, so all of the package's contained
        packages, modules, and extensions are also excluded.

        Currently, this method only supports exclusion from attributes that are
        lists or tuples.  If you need to add support for excluding from other
        attributes in this or a subclass, you can add an '_exclude_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'exclude()'.  So, 'dist.exclude(foo={"bar":"baz"})'
        will try to call 'dist._exclude_foo({"bar":"baz"})', which can then
        handle whatever special exclusion logic is needed.
        """

    def get_cmdline_options(self) -> dict[str, dict[str, str | None]]:
        """Return a '{cmd: {opt:val}}' map of all command-line options

        Option names are all long, but do not include the leading '--', and
        contain dashes rather than underscores.  If the option doesn't take
        an argument (e.g. '--quiet'), the 'val' is 'None'.

        Note that options provided by config files are intentionally excluded.
        """

    def iter_distribution_names(self) -> Iterator[str]:
        """Yield all packages, modules, and extension names in distribution"""

    def handle_display_options(self, option_order):
        """If there were any non-global "display-only" options
        (--help-commands or the metadata display options) on the command
        line, display the requested info and return true; else return
        false.
        """

class DistDeprecationWarning(SetuptoolsDeprecationWarning):
    """Class for warning about deprecations in dist in
    setuptools. Not ignored by default, unlike DeprecationWarning.
    """
