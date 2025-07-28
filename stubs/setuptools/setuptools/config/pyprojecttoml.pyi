"""
Load setuptools configuration from ``pyproject.toml`` files.

**PRIVATE MODULE**: API reserved for setuptools internal usage only.

To read project metadata, consider using
``build.util.project_wheel_metadata`` (https://pypi.org/project/build/).
For simple scenarios, you can also try parsing the file directly
with the help of ``tomllib`` or ``tomli``.
"""

from _typeshed import Incomplete, StrPath
from types import TracebackType
from typing import Any
from typing_extensions import Self

from ..dist import Distribution
from ..warnings import SetuptoolsWarning
from . import expand

def load_file(filepath: StrPath) -> dict[Incomplete, Incomplete]: ...
def validate(config: dict[Incomplete, Incomplete], filepath: StrPath) -> bool: ...
def apply_configuration(dist: Distribution, filepath: StrPath, ignore_option_errors: bool = False) -> Distribution:
    """Apply the configuration from a ``pyproject.toml`` file into an existing
    distribution object.
    """

def read_configuration(
    filepath: StrPath, expand: bool = True, ignore_option_errors: bool = False, dist: Distribution | None = None
) -> dict[str, Any]:
    """Read given configuration file and returns options from it as a dict.

    :param str|unicode filepath: Path to configuration file in the ``pyproject.toml``
        format.

    :param bool expand: Whether to expand directives and other computed values
        (i.e. post-process the given configuration)

    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.

    :param Distribution|None: Distribution object to which the configuration refers.
        If not given a dummy object will be created and discarded after the
        configuration is read. This is used for auto-discovery of packages and in the
        case a dynamic configuration (e.g. ``attr`` or ``cmdclass``) is expanded.
        When ``expand=False`` this object is simply ignored.

    :rtype: dict
    """

def expand_configuration(
    config: dict[Incomplete, Incomplete],
    root_dir: StrPath | None = None,
    ignore_option_errors: bool = False,
    dist: Distribution | None = None,
) -> dict[Incomplete, Incomplete]:
    """Given a configuration with unresolved fields (e.g. dynamic, cmdclass, ...)
    find their final values.

    :param dict config: Dict containing the configuration for the distribution
    :param str root_dir: Top-level directory for the distribution/project
        (the same directory where ``pyproject.toml`` is place)
    :param bool ignore_option_errors: see :func:`read_configuration`
    :param Distribution|None: Distribution object to which the configuration refers.
        If not given a dummy object will be created and discarded after the
        configuration is read. Used in the case a dynamic configuration
        (e.g. ``attr`` or ``cmdclass``).

    :rtype: dict
    """

class _ConfigExpander:
    config: dict[Incomplete, Incomplete]
    root_dir: StrPath
    project_cfg: Incomplete
    dynamic: Incomplete
    setuptools_cfg: Incomplete
    dynamic_cfg: Incomplete
    ignore_option_errors: bool
    def __init__(
        self,
        config: dict[Incomplete, Incomplete],
        root_dir: StrPath | None = None,
        ignore_option_errors: bool = False,
        dist: Distribution | None = None,
    ) -> None: ...
    def expand(self): ...

class _EnsurePackagesDiscovered(expand.EnsurePackagesDiscovered):
    def __init__(
        self, distribution: Distribution, project_cfg: dict[Incomplete, Incomplete], setuptools_cfg: dict[Incomplete, Incomplete]
    ) -> None: ...
    def __enter__(self) -> Self:
        """When entering the context, the values of ``packages``, ``py_modules`` and
        ``package_dir`` that are missing in ``dist`` are copied from ``setuptools_cfg``.
        """

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """When exiting the context, if values of ``packages``, ``py_modules`` and
        ``package_dir`` are missing in ``setuptools_cfg``, copy from ``dist``.
        """

class _BetaConfiguration(SetuptoolsWarning): ...
class _InvalidFile(SetuptoolsWarning): ...
