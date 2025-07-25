from _typeshed import StrPath, Unused

from setuptools.dist import Distribution

from .._distutils.command import install_lib as orig

class install_lib(orig.install_lib):
    """Don't add compiled flags to filenames of non-Python files"""

    distribution: Distribution  # override distutils.dist.Distribution with setuptools.dist.Distribution
    def run(self) -> None: ...
    def get_exclusions(self):
        """
        Return a collections.Sized collections.Container of paths to be
        excluded for single_version_externally_managed installations.
        """

    def copy_tree(
        self,
        infile: StrPath,
        outfile: str,
        preserve_mode: bool = True,
        preserve_times: bool = True,
        preserve_symlinks: bool = False,
        level: Unused = 1,
    ): ...
    def get_outputs(self): ...
