"""A PEP 517 interface to setuptools

Previously, when a user or a command line tool (let's call it a "frontend")
needed to make a request of setuptools to take a certain action, for
example, generating a list of installation requirements, the frontend
would call "setup.py egg_info" or "setup.py bdist_wheel" on the command line.

PEP 517 defines a different method of interfacing with setuptools. Rather
than calling "setup.py" directly, the frontend should:

  1. Set the current directory to the directory with a setup.py file
  2. Import this module into a safe python interpreter (one in which
     setuptools can potentially set global variables or crash hard).
  3. Call one of the functions defined in PEP 517.

What each function does is defined in PEP 517. However, here is a "casual"
definition of the functions (this definition should not be relied on for
bug reports or API stability):

  - `build_wheel`: build a wheel in the folder and return the basename
  - `get_requires_for_build_wheel`: get the `setup_requires` to build
  - `prepare_metadata_for_build_wheel`: get the `install_requires`
  - `build_sdist`: build an sdist in the folder and return the basename
  - `get_requires_for_build_sdist`: get the `setup_requires` to build

Again, this is not a formal definition! Just a "taste" of the module.
"""

from _typeshed import Incomplete, StrPath
from collections.abc import Mapping
from contextlib import _GeneratorContextManager
from typing import NoReturn
from typing_extensions import TypeAlias

from . import dist

__all__ = [
    "get_requires_for_build_sdist",
    "get_requires_for_build_wheel",
    "prepare_metadata_for_build_wheel",
    "build_wheel",
    "build_sdist",
    "get_requires_for_build_editable",
    "prepare_metadata_for_build_editable",
    "build_editable",
    "__legacy__",
    "SetupRequirementsError",
]

_ConfigSettings: TypeAlias = Mapping[str, str | list[str] | None] | None

class SetupRequirementsError(BaseException):
    specifiers: Incomplete
    def __init__(self, specifiers) -> None: ...

class Distribution(dist.Distribution):
    def fetch_build_eggs(self, specifiers) -> NoReturn: ...
    @classmethod
    def patch(cls) -> _GeneratorContextManager[None]:
        """
        Replace
        distutils.dist.Distribution with this class
        for the duration of this context.
        """

class _BuildMetaBackend:
    def run_setup(self, setup_script: str = "setup.py") -> None: ...
    def get_requires_for_build_wheel(self, config_settings: _ConfigSettings = None) -> list[str]: ...
    def get_requires_for_build_sdist(self, config_settings: _ConfigSettings = None) -> list[str]: ...
    def prepare_metadata_for_build_wheel(self, metadata_directory: StrPath, config_settings: _ConfigSettings = None) -> str: ...
    def build_wheel(
        self, wheel_directory: StrPath, config_settings: _ConfigSettings = None, metadata_directory: StrPath | None = None
    ) -> str: ...
    def build_sdist(self, sdist_directory: StrPath, config_settings: _ConfigSettings = None) -> str: ...
    def build_editable(
        self, wheel_directory: StrPath, config_settings: _ConfigSettings = None, metadata_directory: StrPath | None = None
    ) -> str: ...
    def get_requires_for_build_editable(self, config_settings: _ConfigSettings = None) -> list[str]: ...
    def prepare_metadata_for_build_editable(
        self, metadata_directory: StrPath, config_settings: _ConfigSettings = None
    ) -> str: ...

class _BuildMetaLegacyBackend(_BuildMetaBackend):
    """Compatibility backend for setuptools

    This is a version of setuptools.build_meta that endeavors
    to maintain backwards
    compatibility with pre-PEP 517 modes of invocation. It
    exists as a temporary
    bridge between the old packaging mechanism and the new
    packaging mechanism,
    and will eventually be removed.
    """

    def run_setup(self, setup_script: str = "setup.py") -> None: ...

_BACKEND: _BuildMetaBackend
get_requires_for_build_wheel = _BACKEND.get_requires_for_build_wheel
get_requires_for_build_sdist = _BACKEND.get_requires_for_build_sdist
prepare_metadata_for_build_wheel = _BACKEND.prepare_metadata_for_build_wheel
build_wheel = _BACKEND.build_wheel
build_sdist = _BACKEND.build_sdist

get_requires_for_build_editable = _BACKEND.get_requires_for_build_editable
prepare_metadata_for_build_editable = _BACKEND.prepare_metadata_for_build_editable
build_editable = _BACKEND.build_editable

__legacy__: _BuildMetaLegacyBackend
