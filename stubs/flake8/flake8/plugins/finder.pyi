"""Functions related to finding and loading plugins."""

import configparser
import importlib.metadata
from collections.abc import Generator
from logging import Logger
from typing import Any, Final, NamedTuple

LOG: Logger
FLAKE8_GROUPS: Final[frozenset[str]]
BANNED_PLUGINS: dict[str, str]

class Plugin(NamedTuple):
    """A plugin before loading."""

    package: str
    version: str
    entry_point: importlib.metadata.EntryPoint

class LoadedPlugin(NamedTuple):
    """Represents a plugin after being imported."""

    plugin: Plugin
    obj: Any
    parameters: dict[str, bool]
    @property
    def entry_name(self) -> str:
        """Return the name given in the packaging metadata."""

    @property
    def display_name(self) -> str:
        """Return the name for use in user-facing / error messages."""

class Checkers(NamedTuple):
    """Classified plugins needed for checking."""

    tree: list[LoadedPlugin]
    logical_line: list[LoadedPlugin]
    physical_line: list[LoadedPlugin]

class Plugins(NamedTuple):
    """Classified plugins."""

    checkers: Checkers
    reporters: dict[str, LoadedPlugin]
    disabled: list[LoadedPlugin]
    def all_plugins(self) -> Generator[LoadedPlugin, None, None]:
        """Return an iterator over all :class:`LoadedPlugin`s."""

    def versions_str(self) -> str:
        """Return a user-displayed list of plugin versions."""

class PluginOptions(NamedTuple):
    """Options related to plugin loading."""

    local_plugin_paths: tuple[str, ...]
    enable_extensions: frozenset[str]
    require_plugins: frozenset[str]
    @classmethod
    def blank(cls) -> PluginOptions:
        """Make a blank PluginOptions, mostly used for tests."""

def parse_plugin_options(
    cfg: configparser.RawConfigParser, cfg_dir: str, *, enable_extensions: str | None, require_plugins: str | None
) -> PluginOptions:
    """Parse plugin loading related options."""

def find_plugins(cfg: configparser.RawConfigParser, opts: PluginOptions) -> list[Plugin]:
    """Discovers all plugins (but does not load them)."""

def load_plugins(plugins: list[Plugin], opts: PluginOptions) -> Plugins:
    """Load and classify all flake8 plugins.

    - first: extends ``sys.path`` with ``paths`` (to import local plugins)
    - next: converts the ``Plugin``s to ``LoadedPlugins``
    - finally: classifies plugins into their specific types
    """
