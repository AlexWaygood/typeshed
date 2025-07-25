"""setuptools.command.egg_info

Create a distribution's .egg-info directory and contents
"""

from _typeshed import Incomplete
from typing import ClassVar, Final

from .. import Command, SetuptoolsDeprecationWarning
from .._distutils.filelist import FileList as _FileList
from .sdist import sdist

PY_MAJOR: Final[str]

def translate_pattern(glob):
    """
    Translate a file path glob like '*.txt' in to a regular expression.
    This differs from fnmatch.translate which allows wildcards to match
    directory separators. It also knows about '**/' which matches any number of
    directories.
    """

class InfoCommon:
    tag_build: Incomplete
    tag_date: Incomplete
    @property
    def name(self): ...
    def tagged_version(self): ...
    def tags(self): ...
    @property
    def vtags(self): ...

class egg_info(InfoCommon, Command):
    description: str
    user_options: ClassVar[list[tuple[str, str, str]]]
    boolean_options: ClassVar[list[str]]
    negative_opt: ClassVar[dict[str, str]]
    egg_base: Incomplete
    egg_name: Incomplete
    egg_info: Incomplete
    egg_version: Incomplete
    def initialize_options(self) -> None: ...
    @property
    def tag_svn_revision(self) -> int | None: ...
    @tag_svn_revision.setter
    def tag_svn_revision(self, value) -> None: ...
    def save_version_info(self, filename) -> None:
        """
        Materialize the value of date into the
        build tag. Install build keys in a deterministic order
        to avoid arbitrary reordering on subsequent builds.
        """

    def finalize_options(self) -> None: ...
    def write_or_delete_file(self, what, filename, data, force: bool = False) -> None:
        """Write `data` to `filename` or delete if empty

        If `data` is non-empty, this routine is the same as ``write_file()``.
        If `data` is empty but not ``None``, this is the same as calling
        ``delete_file(filename)`.  If `data` is ``None``, then this is a no-op
        unless `filename` exists, in which case a warning is issued about the
        orphaned file (if `force` is false), or deleted (if `force` is true).
        """

    def write_file(self, what, filename, data) -> None:
        """Write `data` to `filename` (if not a dry run) after announcing it

        `what` is used in a log message to identify what is being written
        to the file.
        """

    def delete_file(self, filename) -> None:
        """Delete `filename` (if not a dry run) after announcing it"""

    def run(self) -> None: ...
    filelist: Incomplete
    def find_sources(self) -> None:
        """Generate SOURCES.txt manifest file"""

class FileList(_FileList):
    def __init__(self, warn=None, debug_print=None, ignore_egg_info_dir: bool = False) -> None: ...
    def process_template_line(self, line) -> None: ...
    def include(self, pattern):
        """Include files that match 'pattern'."""

    def exclude(self, pattern):
        """Exclude files that match 'pattern'."""

    def recursive_include(self, dir, pattern):
        """
        Include all files anywhere in 'dir/' that match the pattern.
        """

    def recursive_exclude(self, dir, pattern):
        """
        Exclude any file anywhere in 'dir/' that match the pattern.
        """

    def graft(self, dir):
        """Include all files from 'dir/'."""

    def prune(self, dir):
        """Filter out files from 'dir/'."""

    def global_include(self, pattern):
        """
        Include all files anywhere in the current directory that match the
        pattern. This is very inefficient on large file trees.
        """

    def global_exclude(self, pattern):
        """
        Exclude all files anywhere that match the pattern.
        """

    def append(self, item) -> None: ...
    def extend(self, paths) -> None: ...

class manifest_maker(sdist):
    template: str
    use_defaults: bool
    prune: bool
    manifest_only: bool
    force_manifest: bool
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    filelist: FileList
    def run(self) -> None: ...
    def write_manifest(self) -> None:
        """
        Write the file list in 'self.filelist' to the manifest file
        named by 'self.manifest'.
        """

    def warn(self, msg) -> None: ...
    def add_defaults(self) -> None: ...
    def add_license_files(self) -> None: ...

def write_file(filename, contents) -> None:
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """

def write_pkg_info(cmd, basename, filename) -> None: ...
def warn_depends_obsolete(cmd, basename, filename) -> None:
    """
    Unused: left to avoid errors when updating (from source) from <= 67.8.
    Old installations have a .dist-info directory with the entry-point
    ``depends.txt = setuptools.command.egg_info:warn_depends_obsolete``.
    This may trigger errors when running the first egg_info in build_meta.
    TODO: Remove this function in a version sufficiently > 68.
    """

def write_requirements(cmd, basename, filename) -> None: ...
def write_setup_requirements(cmd, basename, filename) -> None: ...
def write_toplevel_names(cmd, basename, filename) -> None: ...
def overwrite_arg(cmd, basename, filename) -> None: ...
def write_arg(cmd, basename, filename, force: bool = False) -> None: ...
def write_entries(cmd, basename, filename) -> None: ...

class EggInfoDeprecationWarning(SetuptoolsDeprecationWarning):
    """Deprecated behavior warning for EggInfo, bypassing suppression."""
