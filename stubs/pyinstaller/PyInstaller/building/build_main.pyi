"""
Build packages using spec files.

NOTE: All global variables, classes and imported modules create API for .spec files.
"""

from _typeshed import StrPath
from collections.abc import Iterable
from typing import Any, Literal

from PyInstaller.building import _PyiBlockCipher
from PyInstaller.building.datastruct import Target, _TOCTuple

# Referenced in: https://pyinstaller.org/en/stable/hooks.html#PyInstaller.utils.hooks.get_hook_config
# Not to be imported during runtime, but is the type reference for hooks and analysis configuration
# Also referenced in https://pyinstaller.org/en/stable/spec-files.html
# Not to be imported during runtime, but is the type reference for spec files which are executed as python code
class Analysis(Target):
    """
    Class that performs analysis of the user's main Python scripts.

    An Analysis contains multiple TOC (Table of Contents) lists, accessed as attributes of the analysis object.

    scripts
            The scripts you gave Analysis as input, with any runtime hook scripts prepended.
    pure
            The pure Python modules.
    binaries
            The extension modules and their dependencies.
    datas
            Data files collected from packages.
    zipfiles
            Deprecated - always empty.
    zipped_data
            Deprecated - always empty.
    """

    # https://pyinstaller.org/en/stable/hooks-config.html#hook-configuration-options
    hooksconfig: dict[str, dict[str, object]]
    # https://pyinstaller.org/en/stable/spec-files.html#spec-file-operation
    # https://pyinstaller.org/en/stable/feature-notes.html
    pure: list[_TOCTuple]
    zipped_data: list[_TOCTuple]
    # https://pyinstaller.org/en/stable/spec-files.html#giving-run-time-python-options
    # https://pyinstaller.org/en/stable/spec-files.html#the-splash-target
    scripts: list[_TOCTuple]
    # https://pyinstaller.org/en/stable/feature-notes.html#practical-examples
    binaries: list[_TOCTuple]
    zipfiles: list[_TOCTuple]
    datas: list[_TOCTuple]

    inputs: list[str]
    dependencies: list[_TOCTuple]
    noarchive: bool
    optimize: int
    pathex: list[StrPath]
    hiddenimports: list[str]
    hookspath: list[tuple[StrPath, int]]
    excludes: list[str]
    custom_runtime_hooks: list[StrPath]
    # https://pyinstaller.org/en/stable/hooks.html#hook-global-variables
    module_collection_mode: dict[str, str]
    def __init__(
        self,
        scripts: Iterable[StrPath],
        pathex: Iterable[StrPath] | None = None,
        binaries: Iterable[tuple[StrPath, StrPath]] | None = None,
        datas: Iterable[tuple[StrPath, StrPath]] | None = None,
        hiddenimports: Iterable[str] | None = None,
        hookspath: Iterable[StrPath] | None = None,
        hooksconfig: dict[str, dict[str, Any]] | None = None,
        excludes: Iterable[str] | None = None,
        runtime_hooks: Iterable[StrPath] | None = None,
        cipher: _PyiBlockCipher = None,
        win_no_prefer_redirects: bool = False,
        win_private_assemblies: bool = False,
        noarchive: bool = False,
        module_collection_mode: dict[str, str] | None = None,
        optimize: Literal[-1, 0, 1, 2] | None = -1,
    ) -> None:
        """
        scripts
                A list of scripts specified as file names.
        pathex
                An optional list of paths to be searched before sys.path.
        binaries
                An optional list of additional binaries (dlls, etc.) to include.
        datas
                An optional list of additional data files to include.
        hiddenimport
                An optional list of additional (hidden) modules to include.
        hookspath
                An optional list of additional paths to search for hooks. (hook-modules).
        hooksconfig
                An optional dict of config settings for hooks. (hook-modules).
        excludes
                An optional list of module or package names (their Python names, not path names) that will be
                ignored (as though they were not found).
        runtime_hooks
                An optional list of scripts to use as users' runtime hooks. Specified as file names.
        cipher
                Deprecated. Raises an error if not None.
        win_no_prefer_redirects
                Deprecated. Raises an error if not False.
        win_private_assemblies
                Deprecated. Raises an error if not False.
        noarchive
                If True, do not place source files in a archive, but keep them as individual files.
        module_collection_mode
                An optional dict of package/module names and collection mode strings. Valid collection mode strings:
                'pyz' (default), 'pyc', 'py', 'pyz+py' (or 'py+pyz')
        optimize
                Optimization level for collected bytecode. If not specified or set to -1, it is set to the value of
                `sys.flags.optimize` of the running build process.
        """
