"""
Create a wheel that, when installed, will make the source package 'editable'
(add it to the interpreter's path, including metadata) per PEP 660. Replaces
'setup.py develop'.

.. note::
   One of the mechanisms briefly mentioned in PEP 660 to implement editable installs is
   to create a separated directory inside ``build`` and use a .pth file to point to that
   directory. In the context of this file such directory is referred as
   *auxiliary build directory* or ``auxiliary_dir``.
"""

from _typeshed import Incomplete, StrPath, Unused
from collections.abc import Iterator, Mapping
from enum import Enum
from pathlib import Path
from types import TracebackType
from typing import ClassVar, Protocol
from typing_extensions import Self, TypeAlias

from .. import Command, errors, namespaces
from ..dist import Distribution
from ..warnings import SetuptoolsWarning

# Actually from wheel.wheelfile import WheelFile
_WheelFile: TypeAlias = Incomplete

class _EditableMode(Enum):
    """
    Possible editable installation modes:
    `lenient` (new files automatically added to the package - DEFAULT);
    `strict` (requires a new installation when files are added/removed); or
    `compat` (attempts to emulate `python setup.py develop` - DEPRECATED).
    """

    STRICT = "strict"
    LENIENT = "lenient"
    COMPAT = "compat"
    @classmethod
    def convert(cls, mode: str | None) -> _EditableMode: ...

class editable_wheel(Command):
    """Build 'editable' wheel for development.
    This command is private and reserved for internal use of setuptools,
    users should rely on ``setuptools.build_meta`` APIs.
    """

    description: str
    user_options: ClassVar[list[tuple[str, str | None, str]]]
    dist_dir: Incomplete
    dist_info_dir: Incomplete
    project_dir: Incomplete
    mode: Incomplete
    def initialize_options(self) -> None: ...
    package_dir: dict[Incomplete, Incomplete]
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...

class EditableStrategy(Protocol):
    def __call__(self, wheel: _WheelFile, files: list[str], mapping: Mapping[str, str]) -> Unused: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, _exc_type: type[BaseException] | None, _exc_value: BaseException | None, _traceback: TracebackType | None
    ) -> Unused: ...

class _StaticPth:
    dist: Distribution
    name: str
    path_entries: list[Path]
    def __init__(self, dist: Distribution, name: str, path_entries: list[Path]) -> None: ...
    def __call__(self, wheel: _WheelFile, files: list[str], mapping: Mapping[str, str]): ...
    def __enter__(self) -> Self: ...
    def __exit__(self, _exc_type: Unused, _exc_value: Unused, _traceback: Unused) -> None: ...

class _LinkTree(_StaticPth):
    """
    Creates a ``.pth`` file that points to a link tree in the ``auxiliary_dir``.

    This strategy will only link files (not dirs), so it can be implemented in
    any OS, even if that means using hardlinks instead of symlinks.

    By collocating ``auxiliary_dir`` and the original source code, limitations
    with hardlinks should be avoided.
    """

    auxiliary_dir: Path
    build_lib: Path
    def __init__(self, dist: Distribution, name: str, auxiliary_dir: StrPath, build_lib: StrPath) -> None: ...
    def __call__(self, wheel: _WheelFile, files: list[str], mapping: Mapping[str, str]): ...
    def __enter__(self) -> Self: ...
    def __exit__(self, _exc_type: Unused, _exc_value: Unused, _traceback: Unused) -> None: ...

class _TopLevelFinder:
    dist: Distribution
    name: str
    def __init__(self, dist: Distribution, name: str) -> None: ...
    def template_vars(self) -> tuple[str, str, dict[str, str], dict[str, list[str]]]: ...
    def get_implementation(self) -> Iterator[tuple[str, bytes]]: ...
    def __call__(self, wheel: _WheelFile, files: list[str], mapping: Mapping[str, str]): ...
    def __enter__(self) -> Self: ...
    def __exit__(self, _exc_type: Unused, _exc_value: Unused, _traceback: Unused) -> None: ...

class _NamespaceInstaller(namespaces.Installer):
    distribution: Incomplete
    src_root: Incomplete
    installation_dir: Incomplete
    editable_name: Incomplete
    outputs: list[str]
    dry_run: bool
    def __init__(self, distribution, installation_dir, editable_name, src_root) -> None: ...

class InformationOnly(SetuptoolsWarning):
    """Currently there is no clear way of displaying messages to the users
    that use the setuptools backend directly via ``pip``.
    The only thing that might work is a warning, although it is not the
    most appropriate tool for the job...

    See pypa/packaging-problems#558.
    """

class LinksNotSupported(errors.FileError):
    """File system does not seem to support either symlinks or hard links."""

class _DebuggingTips(SetuptoolsWarning): ...
