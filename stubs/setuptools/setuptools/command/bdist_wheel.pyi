"""
Create a wheel (.whl) distribution.

A wheel is a built archive format.
"""

from _typeshed import Incomplete
from collections.abc import Iterable
from typing import ClassVar, Final, Literal

from setuptools import Command

def safe_version(version: str) -> str:
    """
    Convert an arbitrary string to a standard version string
    """

setuptools_major_version: Final[int]

PY_LIMITED_API_PATTERN: Final[str]

def python_tag() -> str: ...
def get_platform(archive_root: str | None) -> str:
    """Return our platform name 'win32', 'linux_x86_64'"""

def get_flag(var: str, fallback: bool, expected: bool = True, warn: bool = True) -> bool:
    """Use a fallback value for determining SOABI flags if the needed config
    var is unset or unavailable.
    """

def get_abi_tag() -> str | None:
    """Return the ABI tag based on SOABI (if available) or emulate SOABI (PyPy2)."""

def safer_version(version: str) -> str: ...

class bdist_wheel(Command):
    description: ClassVar[str]
    supported_compressions: ClassVar[dict[str, int]]
    user_options: ClassVar[list[tuple[str, str | None, str]]]
    boolean_options: ClassVar[list[str]]

    bdist_dir: str | None
    data_dir: str
    plat_name: str | None
    plat_tag: str | None
    format: str
    keep_temp: bool
    dist_dir: str | None
    egginfo_dir: str | None
    root_is_pure: bool | None
    skip_build: bool
    relative: bool
    owner: Incomplete | None
    group: Incomplete | None
    universal: bool
    compression: str | int
    python_tag: str
    build_number: str | None
    py_limited_api: str | Literal[False]
    plat_name_supplied: bool

    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    @property
    def wheel_dist_name(self) -> str:
        """Return distribution full name with - replaced with _"""

    def get_tag(self) -> tuple[str, str, str]: ...
    def run(self) -> None: ...
    def write_wheelfile(self, wheelfile_base: str, generator: str = ...) -> None: ...
    @property
    def license_paths(self) -> Iterable[str]: ...
    def egg2dist(self, egginfo_path: str, distinfo_path: str) -> None:
        """Convert an .egg-info directory into a .dist-info directory"""
