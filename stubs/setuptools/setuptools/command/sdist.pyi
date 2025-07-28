from _typeshed import Incomplete
from collections.abc import Iterator
from typing import ClassVar

from setuptools.dist import Distribution

from .._distutils.command import sdist as orig

def walk_revctrl(dirname: str = "") -> Iterator[Incomplete]:
    """Find all files under revision control"""

class sdist(orig.sdist):
    """Smart sdist that finds anything supported by revision control"""

    distribution: Distribution  # override distutils.dist.Distribution with setuptools.dist.Distribution
    user_options: ClassVar[list[tuple[str, str | None, str]]]
    negative_opt: ClassVar[dict[str, str]]
    README_EXTENSIONS: ClassVar[list[str]]
    READMES: ClassVar[tuple[str, ...]]
    filelist: Incomplete
    def run(self) -> None: ...
    def initialize_options(self) -> None: ...
    def make_distribution(self) -> None:
        """
        Workaround for #516
        """

    def prune_file_list(self) -> None: ...
    def check_readme(self) -> None: ...
    def make_release_tree(self, base_dir, files) -> None: ...
    def read_manifest(self) -> None:
        """Read the manifest file (named by 'self.manifest') and use it to
        fill in 'self.filelist', the list of files to include in the source
        distribution.
        """
