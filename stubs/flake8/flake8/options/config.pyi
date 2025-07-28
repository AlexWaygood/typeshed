"""Config handling logic for Flake8."""

import configparser
from logging import Logger
from typing import Any

from .manager import OptionManager

LOG: Logger

def load_config(config: str | None, extra: list[str], *, isolated: bool = False) -> tuple[configparser.RawConfigParser, str]:
    """Load the configuration given the user options.

    - in ``isolated`` mode, return an empty configuration
    - if a config file is given in ``config`` use that, otherwise attempt to
      discover a configuration using ``tox.ini`` / ``setup.cfg`` / ``.flake8``
    - finally, load any ``extra`` configuration files
    """

def parse_config(option_manager: OptionManager, cfg: configparser.RawConfigParser, cfg_dir: str) -> dict[str, Any]:
    """Parse and normalize the typed configuration options."""
