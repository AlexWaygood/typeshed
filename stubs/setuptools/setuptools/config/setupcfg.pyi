"""
Load setuptools configuration from ``setup.cfg`` files.

**API will be made private in the future**

To read project metadata, consider using
``build.util.project_wheel_metadata`` (https://pypi.org/project/build/).
For simple scenarios, you can also try parsing the file directly
with the help of ``configparser``.
"""

from _typeshed import Incomplete, StrPath
from abc import abstractmethod
from collections.abc import Callable, Iterable
from typing import Any, ClassVar, Generic, TypeVar
from typing_extensions import TypeAlias

from .._distutils.dist import DistributionMetadata
from ..dist import Distribution
from . import expand

SingleCommandOptions: TypeAlias = dict[str, tuple[str, Any]]
AllCommandOptions: TypeAlias = dict[str, SingleCommandOptions]
Target = TypeVar("Target", Distribution, DistributionMetadata)  # noqa: Y001 # Exists at runtime

def read_configuration(
    filepath: StrPath, find_others: bool = False, ignore_option_errors: bool = False
) -> dict[Incomplete, Incomplete]:
    """Read given configuration file and returns options from it as a dict.

    :param str|unicode filepath: Path to configuration file
        to get options from.

    :param bool find_others: Whether to search for other configuration files
        which could be on in various places.

    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.

    :rtype: dict
    """

def apply_configuration(dist: Distribution, filepath: StrPath) -> Distribution:
    """Apply the configuration from a ``setup.cfg`` file into an existing
    distribution object.
    """

def configuration_to_dict(
    handlers: Iterable[ConfigHandler[Distribution] | ConfigHandler[DistributionMetadata]],
) -> dict[Incomplete, Incomplete]:
    """Returns configuration data gathered by given handlers as a dict.

    :param Iterable[ConfigHandler] handlers: Handlers list,
        usually from parse_configuration()

    :rtype: dict
    """

def parse_configuration(
    distribution: Distribution, command_options: AllCommandOptions, ignore_option_errors: bool = False
) -> tuple[ConfigMetadataHandler, ConfigOptionsHandler]:
    """Performs additional parsing of configuration options
    for a distribution.

    Returns a list of used option handlers.

    :param Distribution distribution:
    :param dict command_options:
    :param bool ignore_option_errors: Whether to silently ignore
        options, values of which could not be resolved (e.g. due to exceptions
        in directives such as file:, attr:, etc.).
        If False exceptions are propagated as expected.
    :rtype: list
    """

class ConfigHandler(Generic[Target]):
    """Handles metadata supplied in configuration files."""

    section_prefix: str
    aliases: ClassVar[dict[str, str]]
    ignore_option_errors: Incomplete
    target_obj: Target
    sections: dict[str, SingleCommandOptions]
    set_options: list[str]
    ensure_discovered: expand.EnsurePackagesDiscovered
    def __init__(
        self,
        target_obj: Target,
        options: AllCommandOptions,
        ignore_option_errors,
        ensure_discovered: expand.EnsurePackagesDiscovered,
    ) -> None: ...
    @property
    @abstractmethod
    def parsers(self) -> dict[str, Callable[..., Incomplete]]:
        """Metadata item name to parser function mapping."""

    def __setitem__(self, option_name, value): ...
    def parse_section(self, section_options) -> None:
        """Parses configuration file section.

        :param dict section_options:
        """

    def parse(self) -> None:
        """Parses configuration file items from one
        or more related sections.

        """

class ConfigMetadataHandler(ConfigHandler[DistributionMetadata]):
    section_prefix: str
    aliases: ClassVar[dict[str, str]]
    strict_mode: bool
    package_dir: dict[Incomplete, Incomplete] | None
    root_dir: StrPath | None
    def __init__(
        self,
        target_obj: DistributionMetadata,
        options: AllCommandOptions,
        ignore_option_errors: bool,
        ensure_discovered: expand.EnsurePackagesDiscovered,
        package_dir: dict[Incomplete, Incomplete] | None = None,
        root_dir: StrPath | None = ".",
    ) -> None: ...
    @property
    def parsers(self) -> dict[str, Callable[..., Incomplete]]:
        """Metadata item name to parser function mapping."""

class ConfigOptionsHandler(ConfigHandler[Distribution]):
    section_prefix: str
    root_dir: str | None
    package_dir: dict[str, str]
    def __init__(
        self,
        target_obj: Distribution,
        options: AllCommandOptions,
        ignore_option_errors: bool,
        ensure_discovered: expand.EnsurePackagesDiscovered,
    ) -> None: ...
    @property
    def parsers(self) -> dict[str, Callable[..., Incomplete]]:
        """Metadata item name to parser function mapping."""

    def parse_section_packages__find(self, section_options):
        """Parses `packages.find` configuration file section.

        To be used in conjunction with _parse_packages().

        :param dict section_options:
        """

    def parse_section_entry_points(self, section_options) -> None:
        """Parses `entry_points` configuration file section.

        :param dict section_options:
        """

    def parse_section_package_data(self, section_options) -> None:
        """Parses `package_data` configuration file section.

        :param dict section_options:
        """

    def parse_section_exclude_package_data(self, section_options) -> None:
        """Parses `exclude_package_data` configuration file section.

        :param dict section_options:
        """

    def parse_section_extras_require(self, section_options) -> None:
        """Parses `extras_require` configuration file section.

        :param dict section_options:
        """

    def parse_section_data_files(self, section_options) -> None:
        """Parses `data_files` configuration file section.

        :param dict section_options:
        """
