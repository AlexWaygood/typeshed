from _typeshed import Incomplete, StrPath, Unused
from typing import ClassVar

from setuptools.dist import Distribution

from .._distutils.cmd import _StrPathT
from .._distutils.command import build_py as orig

def make_writable(target) -> None: ...

class build_py(orig.build_py):
    """Enhanced 'build_py' command that includes data files with packages

    The data files are specified via a 'package_data' argument to 'setup()'.
    See 'setuptools.dist.Distribution' for more details.

    Also, this version of the 'build_py' command allows you to specify both
    'py_modules' and 'packages' in the same setup operation.
    """

    distribution: Distribution  # override distutils.dist.Distribution with setuptools.dist.Distribution
    editable_mode: ClassVar[bool]
    package_data: dict[str, list[str]]
    exclude_package_data: dict[Incomplete, Incomplete]
    def finalize_options(self) -> None: ...
    def copy_file(  # type: ignore[override] # No overload, str support only
        self,
        infile: StrPath,
        outfile: _StrPathT,
        preserve_mode: bool = True,
        preserve_times: bool = True,
        link: str | None = None,
        level: Unused = 1,
    ) -> tuple[_StrPathT | str, bool]: ...
    def run(self) -> None:
        """Build modules, packages, and copy data files to build directory"""
    data_files: list[tuple[str, str, str, list[str]]]
    def __getattr__(self, attr: str):
        """lazily compute data files"""

    def get_data_files_without_manifest(self) -> list[tuple[str, str, str, list[str]]]:
        """
        Generate list of ``(package,src_dir,build_dir,filenames)`` tuples,
        but without triggering any attempt to analyze or build the manifest.
        """

    def find_data_files(self, package, src_dir) -> list[str]:
        """Return filenames for package's data files in 'src_dir'"""

    def get_outputs(self, include_bytecode: bool = True) -> list[str]:  # type: ignore[override] # Using a real boolean instead of 0|1
        """See :class:`setuptools.commands.build.SubCommand`"""

    def build_package_data(self) -> None:
        """Copy data files into build directory"""
    manifest_files: dict[str, list[str]]
    def get_output_mapping(self) -> dict[str, str]:
        """See :class:`setuptools.commands.build.SubCommand`"""

    def analyze_manifest(self) -> None: ...
    def get_data_files(self) -> None: ...
    def check_package(self, package, package_dir):
        """Check namespace packages' __init__ for declare_namespace"""

    def initialize_options(self) -> None: ...
    packages_checked: dict[Incomplete, Incomplete]
    def get_package_dir(self, package: str) -> str: ...
    def exclude_data_files(self, package, src_dir, files):
        """Filter filenames for package's data files in 'src_dir'"""

def assert_relative(path): ...
