"""Extensions to the 'distutils' for large or complex distributions"""

from _typeshed import Incomplete
from abc import abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, Literal, TypedDict, TypeVar, overload, type_check_only
from typing_extensions import NotRequired

from ._distutils.cmd import Command as _Command
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
from .depends import Require as Require
from .discovery import _Finder
from .dist import Distribution as Distribution
from .extension import Extension as Extension
from .warnings import SetuptoolsDeprecationWarning as SetuptoolsDeprecationWarning

_CommandT = TypeVar("_CommandT", bound=_Command)

__all__ = [
    "setup",
    "Distribution",
    "Command",
    "Extension",
    "Require",
    "SetuptoolsDeprecationWarning",
    "find_packages",
    "find_namespace_packages",
]

__version__: str

@type_check_only
class _BuildInfo(TypedDict):
    sources: list[str] | tuple[str, ...]
    obj_deps: NotRequired[dict[str, list[str] | tuple[str, ...]]]
    macros: NotRequired[list[tuple[str] | tuple[str, str | None]]]
    include_dirs: NotRequired[list[str]]
    cflags: NotRequired[list[str]]

find_packages = _Finder.find
find_namespace_packages = _Finder.find

def setup(
    *,
    name: str = ...,
    version: str = ...,
    description: str = ...,
    long_description: str = ...,
    long_description_content_type: str = ...,
    author: str = ...,
    author_email: str = ...,
    maintainer: str = ...,
    maintainer_email: str = ...,
    url: str = ...,
    download_url: str = ...,
    packages: list[str] = ...,
    py_modules: list[str] = ...,
    scripts: list[str] = ...,
    ext_modules: Sequence[Extension] = ...,
    classifiers: list[str] = ...,
    distclass: type[Distribution] = ...,
    script_name: str = ...,
    script_args: list[str] = ...,
    options: Mapping[str, Incomplete] = ...,
    license: str = ...,
    keywords: list[str] | str = ...,
    platforms: list[str] | str = ...,
    cmdclass: Mapping[str, type[_Command]] = ...,
    data_files: list[tuple[str, list[str]]] = ...,
    package_dir: Mapping[str, str] = ...,
    obsoletes: list[str] = ...,
    provides: list[str] = ...,
    requires: list[str] = ...,
    command_packages: list[str] = ...,
    command_options: Mapping[str, Mapping[str, tuple[Incomplete, Incomplete]]] = ...,
    package_data: Mapping[str, list[str]] = ...,
    include_package_data: bool = ...,
    # libraries for `Distribution` or `build_clib`, not `Extension`, `build_ext` or `CCompiler`
    libraries: list[tuple[str, _BuildInfo]] = ...,
    headers: list[str] = ...,
    ext_package: str = ...,
    include_dirs: list[str] = ...,
    password: str = ...,
    fullname: str = ...,
    # Custom Distributions could accept more params
    **attrs: Any,
) -> Distribution:
    """The gateway to the Distutils: do everything your setup script needs
    to do, in a highly flexible and user-driven way.  Briefly: create a
    Distribution instance; find and parse config files; parse the command
    line; run each Distutils command found there, customized by the options
    supplied to 'setup()' (as keyword arguments), in config files, and on
    the command line.

    The Distribution instance might be an instance of a class supplied via
    the 'distclass' keyword argument to 'setup'; if no such class is
    supplied, then the Distribution class (in dist.py) is instantiated.
    All other arguments to 'setup' (except for 'cmdclass') are used to set
    attributes of the Distribution instance.

    The 'cmdclass' argument, if supplied, is a dictionary mapping command
    names to command classes.  Each command encountered on the command line
    will be turned into a command class, which is in turn instantiated; any
    class found in 'cmdclass' is used in place of the default, which is
    (for command 'foo_bar') class 'foo_bar' in module
    'distutils.command.foo_bar'.  The command class must provide a
    'user_options' attribute which is a list of option specifiers for
    'distutils.fancy_getopt'.  Any command-line options between the current
    and the next command are used to set attributes of the current command
    object.

    When the entire command-line has been successfully parsed, calls the
    'run()' method on each command object in turn.  This method will be
    driven entirely by the Distribution object (which each command object
    has a reference to, thanks to its constructor), and the
    command-specific options that became attributes of each command
    object.
    """

class Command(_Command):
    """
    Setuptools internal actions are organized using a *command design pattern*.
    This means that each action (or group of closely related actions) executed during
    the build should be implemented as a ``Command`` subclass.

    These commands are abstractions and do not necessarily correspond to a command that
    can (or should) be executed via a terminal, in a CLI fashion (although historically
    they would).

    When creating a new command from scratch, custom defined classes **SHOULD** inherit
    from ``setuptools.Command`` and implement a few mandatory methods.
    Between these mandatory methods, are listed:
    :meth:`initialize_options`, :meth:`finalize_options` and :meth:`run`.

    A useful analogy for command classes is to think of them as subroutines with local
    variables called "options".  The options are "declared" in :meth:`initialize_options`
    and "defined" (given their final values, aka "finalized") in :meth:`finalize_options`,
    both of which must be defined by every command class. The "body" of the subroutine,
    (where it does all the work) is the :meth:`run` method.
    Between :meth:`initialize_options` and :meth:`finalize_options`, ``setuptools`` may set
    the values for options/attributes based on user's input (or circumstance),
    which means that the implementation should be careful to not overwrite values in
    :meth:`finalize_options` unless necessary.

    Please note that other commands (or other parts of setuptools) may also overwrite
    the values of the command's options/attributes multiple times during the build
    process.
    Therefore it is important to consistently implement :meth:`initialize_options` and
    :meth:`finalize_options`. For example, all derived attributes (or attributes that
    depend on the value of other attributes) **SHOULD** be recomputed in
    :meth:`finalize_options`.

    When overwriting existing commands, custom defined classes **MUST** abide by the
    same APIs implemented by the original class. They also **SHOULD** inherit from the
    original class.
    """

    command_consumes_arguments: bool
    distribution: Distribution
    # Any: Dynamic command subclass attributes
    def __init__(self, dist: Distribution, **kw: Any) -> None:
        """
        Construct the command for dist, updating
        vars(self) with any keyword parameters.
        """
    # Note: Commands that setuptools doesn't re-expose are considered deprecated (they must be imported from distutils directly)
    # So we're not listing them here. This list comes directly from the setuptools/command folder. Minus the test command.
    @overload  # type: ignore[override]
    def get_finalized_command(self, command: Literal["alias"], create: bool | Literal[0, 1] = 1) -> alias:
        """Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """

    @overload
    def get_finalized_command(self, command: Literal["bdist_egg"], create: bool | Literal[0, 1] = 1) -> bdist_egg: ...
    @overload
    def get_finalized_command(self, command: Literal["bdist_rpm"], create: bool | Literal[0, 1] = 1) -> bdist_rpm: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["bdist_wheel"], create: bool | Literal[0, 1] = 1) -> bdist_wheel: ...
    @overload
    def get_finalized_command(self, command: Literal["build"], create: bool | Literal[0, 1] = 1) -> build: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["build_clib"], create: bool | Literal[0, 1] = 1) -> build_clib: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["build_ext"], create: bool | Literal[0, 1] = 1) -> build_ext: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["build_py"], create: bool | Literal[0, 1] = 1) -> build_py: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["develop"], create: bool | Literal[0, 1] = 1) -> develop: ...
    @overload
    def get_finalized_command(self, command: Literal["dist_info"], create: bool | Literal[0, 1] = 1) -> dist_info: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["easy_install"], create: bool | Literal[0, 1] = 1) -> easy_install: ...
    @overload
    def get_finalized_command(self, command: Literal["editable_wheel"], create: bool | Literal[0, 1] = 1) -> editable_wheel: ...
    @overload
    def get_finalized_command(self, command: Literal["egg_info"], create: bool | Literal[0, 1] = 1) -> egg_info: ...
    @overload
    def get_finalized_command(self, command: Literal["install"], create: bool | Literal[0, 1] = 1) -> install: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(
        self, command: Literal["install_egg_info"], create: bool | Literal[0, 1] = 1
    ) -> install_egg_info: ...
    @overload
    def get_finalized_command(self, command: Literal["install_lib"], create: bool | Literal[0, 1] = 1) -> install_lib: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["install_scripts"], create: bool | Literal[0, 1] = 1) -> install_scripts: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["rotate"], create: bool | Literal[0, 1] = 1) -> rotate: ...
    @overload
    def get_finalized_command(self, command: Literal["saveopts"], create: bool | Literal[0, 1] = 1) -> saveopts: ...
    @overload
    def get_finalized_command(self, command: Literal["sdist"], create: bool | Literal[0, 1] = 1) -> sdist: ...  # type: ignore[overload-overlap]
    @overload
    def get_finalized_command(self, command: Literal["setopt"], create: bool | Literal[0, 1] = 1) -> setopt: ...
    @overload
    def get_finalized_command(self, command: str, create: bool | Literal[0, 1] = 1) -> Command: ...
    @overload  # type: ignore[override] # Extra **kw param
    def reinitialize_command(self, command: Literal["alias"], reinit_subcommands: bool = False, **kw) -> alias: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_egg"], reinit_subcommands: bool = False, **kw) -> bdist_egg: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_rpm"], reinit_subcommands: bool = False, **kw) -> bdist_rpm: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_wheel"], reinit_subcommands: bool = False, **kw) -> bdist_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["build"], reinit_subcommands: bool = False, **kw) -> build: ...
    @overload
    def reinitialize_command(self, command: Literal["build_clib"], reinit_subcommands: bool = False, **kw) -> build_clib: ...
    @overload
    def reinitialize_command(self, command: Literal["build_ext"], reinit_subcommands: bool = False, **kw) -> build_ext: ...
    @overload
    def reinitialize_command(self, command: Literal["build_py"], reinit_subcommands: bool = False, **kw) -> build_py: ...
    @overload
    def reinitialize_command(self, command: Literal["develop"], reinit_subcommands: bool = False, **kw) -> develop: ...
    @overload
    def reinitialize_command(self, command: Literal["dist_info"], reinit_subcommands: bool = False, **kw) -> dist_info: ...
    @overload
    def reinitialize_command(self, command: Literal["easy_install"], reinit_subcommands: bool = False, **kw) -> easy_install: ...
    @overload
    def reinitialize_command(
        self, command: Literal["editable_wheel"], reinit_subcommands: bool = False, **kw
    ) -> editable_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["egg_info"], reinit_subcommands: bool = False, **kw) -> egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install"], reinit_subcommands: bool = False, **kw) -> install: ...
    @overload
    def reinitialize_command(
        self, command: Literal["install_egg_info"], reinit_subcommands: bool = False, **kw
    ) -> install_egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install_lib"], reinit_subcommands: bool = False, **kw) -> install_lib: ...
    @overload
    def reinitialize_command(
        self, command: Literal["install_scripts"], reinit_subcommands: bool = False, **kw
    ) -> install_scripts: ...
    @overload
    def reinitialize_command(self, command: Literal["rotate"], reinit_subcommands: bool = False, **kw) -> rotate: ...
    @overload
    def reinitialize_command(self, command: Literal["saveopts"], reinit_subcommands: bool = False, **kw) -> saveopts: ...
    @overload
    def reinitialize_command(self, command: Literal["sdist"], reinit_subcommands: bool = False, **kw) -> sdist: ...
    @overload
    def reinitialize_command(self, command: Literal["setopt"], reinit_subcommands: bool = False, **kw) -> setopt: ...
    @overload
    def reinitialize_command(self, command: str, reinit_subcommands: bool = False, **kw) -> Command: ...
    @overload
    def reinitialize_command(self, command: _CommandT, reinit_subcommands: bool = False, **kw) -> _CommandT: ...
    @abstractmethod
    def initialize_options(self) -> None:
        """
        Set or (reset) all options/attributes/caches used by the command
        to their default values. Note that these values may be overwritten during
        the build.
        """

    @abstractmethod
    def finalize_options(self) -> None:
        """
        Set final values for all options/attributes used by the command.
        Most of the time, each option/attribute/cache should only be set if it does not
        have any value yet (e.g. ``if self.attr is None: self.attr = val``).
        """

    @abstractmethod
    def run(self) -> None:
        """
        Execute the actions intended by the command.
        (Side effects **SHOULD** only take place when :meth:`run` is executed,
        for example, creating new files or writing to the terminal output).
        """

class sic(str):
    """Treat this string as-is (https://en.wikipedia.org/wiki/Sic)"""
