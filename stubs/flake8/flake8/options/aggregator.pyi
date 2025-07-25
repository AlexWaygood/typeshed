"""Aggregation function for CLI specified options and config file options.

This holds the logic that uses the collected and merged config files and
applies the user-specified command-line configuration on top of it.
"""

import argparse
import configparser
from collections.abc import Sequence
from logging import Logger

from .manager import OptionManager

LOG: Logger

def aggregate_options(
    manager: OptionManager, cfg: configparser.RawConfigParser, cfg_dir: str, argv: Sequence[str] | None
) -> argparse.Namespace:
    """Aggregate and merge CLI and config file options."""
